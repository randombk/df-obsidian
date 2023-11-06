# Load dfobsidian modules from the right location
# Append based on the current file location
import sys
from pathlib import Path
import time

from obsidian.commands import AbstractCommand, Command
from obsidian.player import Player
sys.path.append(str(Path(__file__).parent))

import io
import asyncio
import threading
from collections import defaultdict, Counter
from typing import Any, Dict, Optional, Tuple

from obsidian.module import Module, AbstractModule, Dependency
from obsidian.log import Logger
from obsidian.worldformat import WorldFormat, AbstractWorldFormat
from obsidian.world import World, WorldManager
from obsidian.errors import CommandError, WorldFormatError

from dfhack_remote import remote, connect, close
from dfhack_proto.CoreProtocol_pb2 import EmptyMessage, StringMessage
from dfhack_proto.CoreProtocol_pb2 import EmptyMessage, StringMessage
from dfhack_proto.RemoteFortressReader_pb2 import *

from .tilegen import build_tile_remappings, write_tile


@remote(plugin='RemoteFortressReader')
async def GetVersionInfo(output: VersionInfo = None): pass

@remote(plugin='RemoteFortressReader')
async def GetMapInfo(output: MapInfo = None): pass

@remote(plugin='RemoteFortressReader')
async def GetWorldMapCenter(output: WorldMap = None): pass

@remote(plugin='RemoteFortressReader')
async def GetViewInfo(output: ViewInfo = None): pass

@remote(plugin='RemoteFortressReader')
async def GetUnitList(output: UnitList = None): pass

@remote(plugin='RemoteFortressReader')
async def GetBlockList(input: BlockRequest, output: BlockList = None,): pass

@remote(plugin='RemoteFortressReader')
async def GetTiletypeList(output: TiletypeList = None): pass

@remote(plugin='RemoteFortressReader')
async def GetMaterialList(output: MaterialList = None): pass


@Module(
    "DFObsidian",
    description="DFObsidian Dwarf Fortress Live World Viewer",
    author="RandomBK",
    version="1.0.0",
    dependencies=[Dependency("core")]
)
class DFObsidianModule(AbstractModule):
    def __init__(self, *args):
        super().__init__(*args)


    @WorldFormat(
        "DFObsidian",
        description="DFObsidian World Format",
        version="v1.0.0",
    )
    class DFObsidianFormat(AbstractWorldFormat["DFObsidianModule"]):
        def __init__(self, *args):
            super().__init__(*args, EXTENSIONS=["df"], METADATA_SUPPORT=False)


        def loadWorld(self, fileIO: io.BufferedRandom, worldManager: WorldManager, persistent: bool = True):
            # This hacky setup is required to get around the fact that
            # loadWorld is not async yet is running in an event loop.
            #
            # This starts a dedicated thread to run the async code in
            # while the main (event loop) thread waits for it to finish.
            #
            # Blame RHydra for this mess (running a non-async function in an event loop)
            result = None
            def run_init():
                nonlocal result
                result = asyncio.run(self.loadFromDF(worldManager, fileIO))
            thr = threading.Thread(target=run_init, name="DFObsidian World Loader", daemon=True)
            thr.start()
            thr.join()

            return result


        def saveWorld(self, world: World, fileIO: io.BufferedRandom, worldManager: WorldManager):
            Logger.warn("This world cannot be saved!", module="DFObsidian")


        async def loadFromDF(
            self: World,
            worldManager: WorldManager,
            fileIO: io.BufferedRandom,
        ):
            # Try to close the previous connection
            # This is needed because there's no 'unloadWorld' hook
            try:
                await close()
            except:
                pass

            df_context = {}

            # Read host and port from the world file
            uri = fileIO.readline().decode('utf-8').strip()
            Logger.info(f"Attempting connection to DFHack at {uri}...", module="DFObsidian")
            host, port = uri.split(':')

            # Connect to DF and fetch the versions
            await connect(host, int(port))
            version = await GetVersionInfo()
            Logger.info(f"Connected to Dwarf Fortress v{version.dwarf_fortress_version} " +
                        f"Running DFHack v{version.dfhack_version}", module="DFObsidian")
            df_context['version'] = version

            #
            # Dwarven Coordinate System
            #
            # DF coordinates use (X, Y) for the horizontal plane and Z for the vertical plane.
            # (0, 0) is the top left corner of the map.
            #
            # Terminology:
            #  - In DF, the map is divided into 'blocks' of 16x16x1 'tiles'.
            #  - We then translate each 'tile' into 3x3x4 Obsidian 'blocks'.
            # To avoid confusion, we will refer to DF 'blocks' as 'chunks'.
            #
            # The DF map lives in multiple 16x16-tile chunks per z-level. Thus, a GetMapInfo result of
            # 12x12x192 means that the map is 192 z-levels tall, and each z-level is 12x12 chunks
            # with each chunk being 16x16 tiles. This means that the map is 192x192x192 tiles in total.
            #
            # To translate to Obsidian blocks, each DF tile is 3x3 wide and 4 tall (3 walkable and 1 floor).
            # As Obsidian uses (X, Z) for the horizontal plane and Y for the vertical plane, we need to
            # translate the DF coordinates to Obsidian coordinates.
            #
            # We will use keep X the same, but map DF-Y to Obsidian-Z and DF-Z to Obsidian-Y.
            #
            # THE CONVENTION FOR THIS CODE IS TO SWAP TO OBSIDIAN COORDINATES AS SOON AS POSSIBLE.
            # Thus, assume that all coordinates are in Obsidian coordinates unless otherwise specified.
            #

            # Get the world size
            map_info = await GetMapInfo()
            df_tiles = (map_info.block_size_x * 16, map_info.block_size_z, map_info.block_size_y * 16)
            df_context['df_tiles'] = df_tiles
            Logger.info(f"DF World Size: {df_tiles[0]}x{df_tiles[2]} wide, {df_tiles[1]} tall", module="DFObsidian")

            # Obsidian blocks
            obsidian_size = (df_tiles[0] * 3, df_tiles[1] * 4, df_tiles[2] * 3)
            blocks = bytearray(obsidian_size[0] * obsidian_size[1] * obsidian_size[2])
            Logger.info(f"Obsidian Size: {obsidian_size[0]}x{obsidian_size[1]}x{obsidian_size[2]}", module="DFObsidian")

            # Fetch the tile and material database
            df_context['tileTypes'] = (await GetTiletypeList()).tiletype_list
            df_context['materialList'] = await GetMaterialList()
            build_tile_remappings(df_context)

            # Pick the spawn point to be the location of one of our dwarves
            units = await GetUnitList()
            # TODO: 573 is NOT safe to hard-code - use GetMaterialList to find the material ID of "DWARF"
            spawn_next_to = [i for i in units.creature_list if i.race.mat_type == 573][0]
            spawn = (spawn_next_to.pos_x * 3 + 2, spawn_next_to.pos_z * 4 + 2, spawn_next_to.pos_y * 3 + 2)
            Logger.info(f"Spawn Point: {spawn} (Next to {spawn_next_to.name})", module="DFObsidian")

            # Keep track of the most common tile types to inform development prioritization
            df_context['tile_ctr'] = Counter()
            df_context['tile_unknown'] = Counter()

            # Fetch the world and translate the tiles - Process one z-layer at a time
            Logger.info("Fetching world data...", module="DFObsidian")
            startTime = time.time()
            df_context['tile_map'] = {}
            for z in range(df_tiles[1]):
                await self.loadWorldZLayer(blocks, z, df_tiles, obsidian_size, df_context)
            endTime = time.time()
            Logger.info(f"World data processed in {endTime - startTime} seconds", module="DFObsidian")
            Logger.info(f"Most common tile types encountered: {df_context['tile_ctr'].most_common(50)}", module="DFObsidian")
            Logger.info(f"Most common unknown tiles encountered: {df_context['tile_unknown'].most_common(50)}", module="DFObsidian")

            # Create and Return New World Data
            world = World(
                worldManager,  # Pass In World Manager
                'Test World',
                obsidian_size[0], obsidian_size[1], obsidian_size[2],
                blocks,
                spawnX=spawn[0] * 32,
                spawnY=spawn[1] * 32,
                spawnZ=spawn[2] * 32,
                worldFormat=self,
                persistent=False,  # Pass In Persistent Flag
                fileIO=fileIO,  # Pass In File Reader/Writer
                canEdit=False,
            )
            world.df_context = df_context
            return world


        async def loadWorldZLayer(
            self,
            blocks: bytearray,
            df_z: int,
            df_tiles: Tuple[int, int, int],
            obsidian_size: Tuple[int, int, int],
            df_context: Dict[str, Any],
        ):
            Logger.info(f"  => Processing Z-level {df_z}...", module="DFObsidian")
            start_time = time.time()
            request = BlockRequest()
            request.force_reload = True
            request.min_x = 0
            request.min_y = 0
            request.min_z = df_z
            request.max_x = df_tiles[0] // 16
            request.max_y = df_tiles[2] // 16
            request.max_z = df_z + 1
            df_blocks = await GetBlockList(request)
            Logger.info(f"    => Received {len(df_blocks.map_blocks)} chunks", module="DFObsidian")

            # Used to save the blocks to disk for debugging
            # with open(f"/ram/df/df_blocks_{df_z}.out", "wb") as f:
            #     f.write(df_blocks.SerializeToString())

            # # df_blocks = BlockList()
            # # with open(f"/ram/df/df_blocks_{df_z}.out", "rb") as f:
            # #     df_blocks.ParseFromString(f.read())
            # Logger.info(f"    => Received {len(df_blocks.map_blocks)} chunks", module="DFObsidian")

            # Compact the original tilemap into a single bytearray
            Logger.info(f"    => Generating tile fillmap...", module="DFObsidian")
            orig_tilemap = [None] * (df_tiles[0] * df_tiles[2])
            for chunk in df_blocks.map_blocks:
                # The top left corner of the chunk in DF Tile coordinates
                mapX = chunk.map_x
                mapY = chunk.map_y

                for i in range(16 * 16):
                    # The target block in DF Tile coordinates
                    tileX = mapX + (i % 16)
                    tileY = mapY + (i // 16)

                    # The top left corner of the chunk in DF Tile coordinates
                    fillmap_idx = tileX + tileY * df_tiles[0]
                    orig_tilemap[fillmap_idx] = (
                        chunk.tiles[i],
                        df_context['tileMap'][chunk.tiles[i]],
                        # chunk.materials[i],
                        # chunk.vein_materials[i],
                        # chunk.base_materials[i],
                    )
            df_context['tile_map'][df_z] = orig_tilemap

            Logger.info(f"    => Begin processing chunks...", module="DFObsidian")
            mapMaxXTiles = df_tiles[0]
            mapMaxYTiles = df_tiles[2]
            mapWidthObsX = obsidian_size[0]
            mapWidthObsZ = obsidian_size[2]
            for chunk in df_blocks.map_blocks:
                # The top left corner of the chunk in DF Tile coordinates
                mapX = chunk.map_x
                mapY = chunk.map_y

                # The top left corner of the chunk in Obsidian coordinates
                baseX = mapX * 3
                baseZ = mapY * 3
                baseY = df_z * 4

                # Loop through each tile in the chunk
                for i in range(16 * 16):
                    # The target block in DF Tile coordinates
                    tileX = mapX + (i % 16)
                    tileY = mapY + (i // 16)

                    # The target block in Obsidian coordinates
                    blockX = baseX + (i % 16) * 3
                    blockZ = baseZ + (i // 16) * 3
                    blockY = baseY

                    write_tile(
                        df_context,
                        blocks, mapWidthObsX, mapWidthObsZ,
                        blockX=blockX, blockY=blockY, blockZ=blockZ,
                        orig_tilemap=orig_tilemap,
                        tile=chunk.tiles[i],
                        map_max_x_tiles=mapMaxXTiles, map_max_y_tiles=mapMaxYTiles,
                        material=chunk.materials[i],
                        layer_material=chunk.layer_materials[i],
                        vein_material=chunk.vein_materials[i],
                        base_material=chunk.base_materials[i],
                        water=chunk.water[i],
                        magma=chunk.magma[i],
                    )

            end_type = time.time()
            Logger.info(f"    => Z-level {df_z} processed in {end_type - start_time} seconds", module="DFObsidian")


    # Lookup by block
    @Command(
        "DFObsidian Inspection Tools",
        description="Prints the history of a given player",
        version="v1.0.0"
    )
    class FBICommand(AbstractCommand["DFObsidianModule"]):
        def __init__(self, *args):
            super().__init__(*args, ACTIVATORS=["dfo"], OP=True)

        async def execute(self, ctx: Player, mode: str = "help", param1: Optional[str] = None):
            if ctx.worldPlayerManager is not None:
                world = ctx.worldPlayerManager.world
            else:
                raise CommandError("You are not in a world!")

            if not hasattr(world, 'df_context'):
                raise CommandError("You are not in a DFObsidian world!")

            if mode == "help":
                await self.handleHelp(ctx)
            elif mode == "lookup":
                await self.handleLookup(world, ctx)
            else:
                await self.handleInvalidSubcommand(ctx, mode)

        async def handleHelp(self, ctx: Player):
            await ctx.sendMessage([
                "&eDF Obsidian - Explore your DF world in Minecraft!",
                "&a    /dfo lookup &f- &bPrints info about the selected block",
            ])

        async def handleInvalidSubcommand(self, ctx: Player, subcommand: str):
            await ctx.sendMessage(f"&cInvalid subcommand: {subcommand}")

        async def handleLookup(self, world: World, ctx: Player):
            # Get coordinates
            await ctx.sendMessage("&aPlease select the block")
            x, y, z, _ = await ctx.getNextBlockUpdate()

            # Convert the block to DF coordinates
            tileX = x // 3
            tileY = z // 3
            tileZ = y // 4

            if (tileX >= world.df_context['df_tiles'][0]
                or tileY >= world.df_context['df_tiles'][1]
                or tileZ >= world.df_context['df_tiles'][2]
            ):
                await ctx.sendMessage(f"&aNo info found for ({x}, {y}, {z}): Out of Bounds")

            # Get the block info
            tiletypes = world.df_context['tileTypes']
            block = world.df_context['tile_map'][tileZ][tileX + tileY * world.df_context['df_tiles'][0]]
            if block is None:
                await ctx.sendMessage(f"&aNo info found for ({x}, {y}, {z}): Unknown Block")
            else:
                await ctx.sendMessage(f"&aType: {block[0]} - {tiletypes[block[0]].name}")
