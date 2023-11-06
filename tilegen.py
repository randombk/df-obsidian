from typing import Any, Dict, List, Tuple
from dfhack_proto.RemoteFortressReader_pb2 import *
from .tiles import *

ROTATION_INDEX = {
    'N': 0, 'E': 1, 'S': 2, 'W': 3,
    # 'NE': 4, 'SE': 5, 'SW': 6, 'NW': 7,
}
ROTATIONS = [
    #
    # Cardinal rotations in 90 degree increments
    #

    # North is the standard orientation
    [
         0,  1,  2,  3,  4,  5,  6,  7,  8,
         9, 10, 11, 12, 13, 14, 15, 16, 17,
        18, 19, 20, 21, 22, 23, 24, 25, 26,
        27, 28, 29, 30, 31, 32, 33, 34, 35,
    ],
    # East is a 90 degree rotation along all y axes
    [
         6,  3,  0,  7,  4,  1,  8,  5,  2,
        15, 12,  9, 16, 13, 10, 17, 14, 11,
        24, 21, 18, 25, 22, 19, 26, 23, 20,
        33, 30, 27, 34, 31, 28, 35, 32, 29,
    ],
    # South
    [
         8,  7,  6,  5,  4,  3,  2,  1,  0,
        17, 16, 15, 14, 13, 12, 11, 10,  9,
        26, 25, 24, 23, 22, 21, 20, 19, 18,
        35, 34, 33, 32, 31, 30, 29, 28, 27,
    ],
    # West
    [
         2,  5,  8,  1,  4,  7,  0,  3,  6,
        11, 14, 17, 10, 13, 16,  9, 12, 15,
        20, 23, 26, 19, 22, 25, 18, 21, 24,
        29, 32, 35, 28, 31, 34, 27, 30, 33,
    ],
]


def build_tile_remappings(df_context: Dict[str, Any]):
    tileMap = [None] * len(df_context['tileTypes'])

    for idx, tile in enumerate(df_context['tileTypes']):
        name = tile.name
        # Handle air variants
        if name in ['Void', 'Air', 'OpenSpace', 'RampTop', 'Chasm']:
            tileData = None  # Fall back to default

        # Don't do anything special with tracks for now
        # if 'Track' in name:
        #     # Handle rails separately
        #     tileData = blockOf(Blocks.SPONGE)


        # Handle floors
        elif 'Floor' in name or name == 'FurrowedSoil':
            tileData = floorOf(getMaterial(name))

        # Handle Walls
        elif 'Wall' in name or 'Pillar' in name:
            tileData = blockOf(getMaterial(name))

        # Handle Pebbles
        elif 'Pebbles' in name :
            tileData = pebblesOf(getMaterial(name), Blocks.COBBLESTONE)
        elif 'Boulder'in name:
            tileData = sprinklesOf(getMaterial(name), Blocks.COBBLESTONE)
        elif 'Sapling' in name or 'Shrub' in name:
            tileData = [
                *sprinklesOf(Blocks.DIRT, Blocks.FLOWER),
                *sprinklesOf(Blocks.DIRT, Blocks.ROSE),
            ]

        # Stairs
        elif 'StairUD' in name:
            tileData = stairUpDownOf(getMaterial(name))
        elif 'StairD' in name:
            tileData = stairDownOf(getMaterial(name))
        elif 'StairU' in name:
            tileData = stairUpOf(getMaterial(name))

        # Ramps
        elif 'Ramp' in name:
            tileData = rampOf(getMaterial(name))

        # Trees
        elif 'TreeTrunk' in name:
            tileData = treeTrunks()
        elif 'TreeBranch' in name or 'TreeCapInterior' in name:
            tileData = treeBranch()
        elif 'Twigs' in name:
            tileData = treeTwigs()
        elif 'Roots' in name:
            tileData = treeRoots()

        # Brooks & Streams
        elif name.startswith('BrookTop'):
            tileData = floorOf(Blocks.STATIONARY_WATER)
        elif name.startswith('Brook'):
            tileData = blockOf(Blocks.STATIONARY_WATER)
        elif name.startswith('MurkyPool'):
            tileData = blockOf(Blocks.STATIONARY_WATER)
        elif name.startswith('River'):
            tileData = blockOf(Blocks.STATIONARY_WATER)
        elif name in ['River', 'Waterfall']:
            tileData = blockOf(Blocks.STATIONARY_WATER)
        elif name in ['MagmaFlow', 'SemiMoltenRock', 'EeriePit']:
            tileData = blockOf(Blocks.STATIONARY_LAVA)

        elif name in COMPLEX_TILE_TO_BLOCK:
            tileData = COMPLEX_TILE_TO_BLOCK[name]
        else:
            tileData = blockOf(Blocks.SPONGE)

        tileMap[idx] = (name, tileData)

    df_context['tileMap'] = tileMap


def hasBlock(
    x: int, y: int,
    orig_tilemap: List[Tuple[int, Any]],
    map_max_x_tiles: int, map_max_y_tiles: int,
) -> bool:
    if x < 0 or x >= map_max_x_tiles:
        return False
    if y < 0 or y >= map_max_y_tiles:
        return False

    # Check if the tile is solid by checking if the top middle is solid
    orig_tile = orig_tilemap[x + map_max_x_tiles * y]
    if orig_tile is None:
        return False
    
    value = orig_tile[1]
    tileData = value[1]
    if tileData is None or type(tileData) == int:
        return False

    if type(tileData) == list:
        tileData = tileData[0]

    return tileData[4] != Blocks.AIR


def write_tile(
    df_context: Dict[str, Any],
    blocks: bytearray, obsidian_size_x: int, obsidian_size_z: int,
    blockX: int, blockY: int, blockZ: int,
    tile: int, map_max_x_tiles: int, map_max_y_tiles: int,
    orig_tilemap: List[Tuple[int, Any]],
    material: MatPair,
    layer_material: MatPair,
    vein_material: MatPair,
    base_material: MatPair,
    water: int,
    magma: int,
):
    # Translate the tile
    (tileName, tileData) = df_context['tileMap'][tile]

    # Custom remapping logic before passing into the remap table
    df_context['tile_ctr'][tileName] += 1

    # Fetch and apply the tile-to-block mapping
    if tileData is None:
        pass
    else:
        # Support randomization
        if type(tileData) == list:
            h = hash(blockX + 7 * blockY + 13 * blockZ)
            tileData = tileData[h % len(tileData)]

            # Apply a random rotation as well to spice things up
            tileData = [tileData[i] for i in ROTATIONS[h % 4]]

        # Special case for ramps as we need to deal with rotation and inner/outer corners
        if 'Ramp' in tileName and type(tileData) == int:
            tileX = blockX // 3
            tileY = blockZ // 3
            layer_material = tileData

            # Check if there's anything in the eight cardinal directions
            dirs = [
                hasBlock(tileX + dX, tileY + dY, orig_tilemap, map_max_x_tiles, map_max_y_tiles)
                # eight directions, clockwise from north
                for (dX, dY) in [(0, -1), (1, -1), (1, 0), (1, 1),
                                 (0, 1), (-1, 1), (-1, 0), (-1, -1)]
            ]

            # Index of Dirs:
            # (true if there's a block in that direction)
            #
            # 7   0   1
            #  \  |  /
            #   * * *
            # 6-* * *-2
            #   * * *
            #  /  |  \
            # 5   4   3
            topLayer = [
                dirs[6] or dirs[7] or dirs[0],  dirs[0],    dirs[0] or dirs[1] or dirs[2],
                dirs[6],                        False,      dirs[2],
                dirs[4] or dirs[5] or dirs[6],  dirs[4],    dirs[2] or dirs[3] or dirs[4],
            ]
            shouldFill = [
                *topLayer,

                # The 2nd to top layer depends on the top layer
                topLayer[0],                topLayer[0] or topLayer[2], topLayer[2],
                topLayer[0] or topLayer[6], True,                       topLayer[2] or topLayer[8],
                topLayer[6],                topLayer[6] or topLayer[8], topLayer[8],

                # Always fill one higher than the floor
                True, True, True,
                True, True, True,
                True, True, True,

                # Always fill floor
                True, True, True,
                True, True, True,
                True, True, True,
            ]
            tileData = [layer_material if i else Blocks.AIR for i in shouldFill]

        for i in range(3*3*4):
            obX = blockX + (i % 3)
            obZ = blockZ + ((i // 3) % 3)
            obY = blockY + (3 - (i // (3*3)))

            blocks[obX + obsidian_size_x * (obZ + obsidian_size_z * obY)] = tileData[i]

    # Handle water and magma by filling in empty space
    targetHeight = 0
    targetFluid = Blocks.AIR
    if water > 0:
        targetHeight = int(water / 7 * 3) + 1
        targetFluid = Blocks.STATIONARY_WATER
    if magma > 0:
        targetHeight = int(magma / 7 * 3) + 1
        targetFluid = Blocks.STATIONARY_LAVA
    if targetHeight > 0:
        for i in range(targetHeight * 3 * 3):
            obX = blockX + (i % 3)
            obZ = blockZ + ((i // 3) % 3)
            obY = blockY + (3 - (i // (3*3)))
            if blocks[obX + obsidian_size_x * (obZ + obsidian_size_z * obY)] == Blocks.AIR:
                blocks[obX + obsidian_size_x * (obZ + obsidian_size_z * obY)] = targetFluid
