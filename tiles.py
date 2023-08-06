import random

class Blocks:
    AIR = 0
    STONE = 1
    GRASS_BLOCK = 2
    DIRT = 3
    COBBLESTONE = 4
    PLANKS = 5
    SAPLING = 6
    BEDROCK = 7
    FLOWING_WATER = 8
    STATIONARY_WATER = 9
    FLOWING_LAVA = 10
    STATIONARY_LAVA = 11
    SAND = 12
    GRAVEL = 13
    GOLD_ORE = 14
    IRON_ORE = 15
    COAL_ORE = 16
    WOOD = 17
    LEAVES = 18
    SPONGE = 19
    GLASS = 20
    RED_CLOTH = 21
    ORANGE_CLOTH = 22
    YELLOW_CLOTH = 23
    CHARTREUSE_CLOTH = 24
    GREEN_CLOTH = 25
    SPRING_GREEN_CLOTH = 26
    CYAN_CLOTH = 27
    CAPRI_CLOTH = 28
    ULTRAMARINE_CLOTH = 29
    VIOLET_CLOTH = 30
    PURPLE_CLOTH = 31
    MAGENTA_CLOTH = 32
    ROSE_CLOTH = 33
    DARK_GRAY_CLOTH = 34
    LIGHT_GRAY_CLOTH = 35
    WHITE_CLOTH = 36
    FLOWER = 37
    ROSE = 38
    BROWN_MUSHROOM = 39
    RED_MUSHROOM = 40
    BLOCK_OF_GOLD = 41
    BLOCK_OF_IRON = 42
    DOUBLE_SLAB = 43
    SLAB = 44
    BRICKS = 45
    TNT = 46
    BOOKSHELF = 47
    MOSSY_COBBLESTONE = 48
    OBSIDIAN = 49


def floorOf(type: int):
    return bytearray([
        Blocks.AIR, Blocks.AIR, Blocks.AIR,
        Blocks.AIR, Blocks.AIR, Blocks.AIR,
        Blocks.AIR, Blocks.AIR, Blocks.AIR,

        Blocks.AIR, Blocks.AIR, Blocks.AIR,
        Blocks.AIR, Blocks.AIR, Blocks.AIR,
        Blocks.AIR, Blocks.AIR, Blocks.AIR,

        Blocks.AIR, Blocks.AIR, Blocks.AIR,
        Blocks.AIR, Blocks.AIR, Blocks.AIR,
        Blocks.AIR, Blocks.AIR, Blocks.AIR,

        type, type, type,
        type, type, type,
        type, type, type,
    ])


def blockOf(type: int):
    return bytearray([
        type, type, type,
        type, type, type,
        type, type, type,

        type, type, type,
        type, type, type,
        type, type, type,

        type, type, type,
        type, type, type,
        type, type, type,

        type, type, type,
        type, type, type,
        type, type, type,
    ])


def sprinklesOf(base: int, top: int):
    return [
        bytearray([
            Blocks.AIR, Blocks.AIR, Blocks.AIR,
            Blocks.AIR, Blocks.AIR, Blocks.AIR,
            Blocks.AIR, Blocks.AIR, Blocks.AIR,

            Blocks.AIR, Blocks.AIR, Blocks.AIR,
            Blocks.AIR, Blocks.AIR, Blocks.AIR,
            Blocks.AIR, Blocks.AIR, Blocks.AIR,

            Blocks.AIR, Blocks.AIR, Blocks.AIR,
            Blocks.AIR, top, Blocks.AIR,
            Blocks.AIR, Blocks.AIR, Blocks.AIR,

            base, base, base,
            base, base, base,
            base, base, base,
        ]),
        bytearray([
            Blocks.AIR, Blocks.AIR, Blocks.AIR,
            Blocks.AIR, Blocks.AIR, Blocks.AIR,
            Blocks.AIR, Blocks.AIR, Blocks.AIR,

            Blocks.AIR, Blocks.AIR, Blocks.AIR,
            Blocks.AIR, Blocks.AIR, Blocks.AIR,
            Blocks.AIR, Blocks.AIR, Blocks.AIR,

            Blocks.AIR, Blocks.AIR, Blocks.AIR,
            top, Blocks.AIR, Blocks.AIR,
            Blocks.AIR, Blocks.AIR, Blocks.AIR,

            base, base, base,
            base, base, base,
            base, base, base,
        ]),
        bytearray([
            Blocks.AIR, Blocks.AIR, Blocks.AIR,
            Blocks.AIR, Blocks.AIR, Blocks.AIR,
            Blocks.AIR, Blocks.AIR, Blocks.AIR,

            Blocks.AIR, Blocks.AIR, Blocks.AIR,
            Blocks.AIR, Blocks.AIR, Blocks.AIR,
            Blocks.AIR, Blocks.AIR, Blocks.AIR,

            top, Blocks.AIR, Blocks.AIR,
            Blocks.AIR, Blocks.AIR, Blocks.AIR,
            Blocks.AIR, Blocks.AIR, Blocks.AIR,

            base, base, base,
            base, base, base,
            base, base, base,
        ]),
        bytearray([
            Blocks.AIR, Blocks.AIR, Blocks.AIR,
            Blocks.AIR, Blocks.AIR, Blocks.AIR,
            Blocks.AIR, Blocks.AIR, Blocks.AIR,

            Blocks.AIR, Blocks.AIR, Blocks.AIR,
            Blocks.AIR, Blocks.AIR, Blocks.AIR,
            Blocks.AIR, Blocks.AIR, Blocks.AIR,

            top, Blocks.AIR, Blocks.AIR,
            Blocks.AIR, Blocks.AIR, top,
            Blocks.AIR, Blocks.AIR, Blocks.AIR,

            base, base, base,
            base, base, base,
            base, base, base,
        ]),
    ]


def pebblesOf(base: int, top: int):
    ret = []
    for i in range(4):
        ret.append(bytearray([
            Blocks.AIR, Blocks.AIR, Blocks.AIR,
            Blocks.AIR, Blocks.AIR, Blocks.AIR,
            Blocks.AIR, Blocks.AIR, Blocks.AIR,

            Blocks.AIR, Blocks.AIR, Blocks.AIR,
            Blocks.AIR, Blocks.AIR, Blocks.AIR,
            Blocks.AIR, Blocks.AIR, Blocks.AIR,

            Blocks.AIR, Blocks.AIR, Blocks.AIR,
            Blocks.AIR, Blocks.AIR, Blocks.AIR,
            Blocks.AIR, Blocks.AIR, Blocks.AIR,

            *[top if random.random() < 0.5 else base for _ in range(9)],
        ]))
    return ret


def stairUpOf(type: int):
    return bytearray([
        Blocks.AIR, Blocks.AIR, Blocks.SLAB,
        Blocks.AIR, Blocks.AIR, type,
        Blocks.AIR, Blocks.AIR, type,

        Blocks.SLAB, type, type,
        Blocks.AIR, Blocks.AIR, Blocks.AIR,
        Blocks.AIR, Blocks.AIR, Blocks.AIR,

        type, Blocks.AIR, Blocks.AIR,
        type, Blocks.AIR, Blocks.AIR,
        Blocks.SLAB, Blocks.AIR, Blocks.AIR,

        type, type, type,
        type, type, type,
        type, type, type,
    ])


def stairDownOf(type: int):
    return bytearray([
        Blocks.AIR, Blocks.AIR, Blocks.AIR,
        Blocks.AIR, Blocks.AIR, Blocks.AIR,
        Blocks.AIR, Blocks.AIR, Blocks.AIR,

        Blocks.AIR, Blocks.AIR, Blocks.AIR,
        Blocks.AIR, Blocks.AIR, Blocks.AIR,
        Blocks.AIR, Blocks.AIR, Blocks.AIR,

        Blocks.AIR, Blocks.AIR, Blocks.AIR,
        Blocks.AIR, Blocks.AIR, Blocks.AIR,
        Blocks.AIR, Blocks.AIR, Blocks.AIR,

        Blocks.AIR, Blocks.AIR, Blocks.AIR,
        Blocks.AIR, Blocks.AIR, Blocks.AIR,
        type, type, Blocks.SLAB,
    ])


def stairUpDownOf(type: int):
    return bytearray([
        Blocks.AIR, Blocks.AIR, Blocks.SLAB,
        Blocks.AIR, Blocks.AIR, type,
        Blocks.AIR, Blocks.AIR, type,

        Blocks.SLAB, type, type,
        Blocks.AIR, Blocks.AIR, Blocks.AIR,
        Blocks.AIR, Blocks.AIR, Blocks.AIR,

        type, Blocks.AIR, Blocks.AIR,
        type, Blocks.AIR, Blocks.AIR,
        Blocks.SLAB, Blocks.AIR, Blocks.AIR,

        Blocks.AIR, Blocks.AIR, Blocks.AIR,
        Blocks.AIR, Blocks.AIR, Blocks.AIR,
        type, type, Blocks.SLAB,
    ])


def rampOf(type: int):
    # SPECIAL CASE: Simply store the material type - the ramp
    # logic is custom generated.
    return type


def treeBranch():
    return [
        bytearray([
            Blocks.LEAVES, Blocks.WOOD, Blocks.LEAVES,
            Blocks.LEAVES, Blocks.WOOD, Blocks.LEAVES,
            Blocks.LEAVES, Blocks.WOOD, Blocks.LEAVES,

            Blocks.LEAVES, Blocks.LEAVES, Blocks.LEAVES,
            Blocks.WOOD, Blocks.WOOD, Blocks.WOOD,
            Blocks.LEAVES, Blocks.LEAVES, Blocks.LEAVES,

            Blocks.LEAVES, Blocks.LEAVES, Blocks.LEAVES,
            Blocks.WOOD, Blocks.WOOD, Blocks.LEAVES,
            Blocks.LEAVES, Blocks.LEAVES, Blocks.WOOD,

            Blocks.LEAVES, Blocks.WOOD, Blocks.LEAVES,
            Blocks.LEAVES, Blocks.WOOD, Blocks.LEAVES,
            Blocks.LEAVES, Blocks.WOOD, Blocks.LEAVES,
        ]),
        bytearray([
            Blocks.LEAVES, Blocks.LEAVES, Blocks.WOOD,
            Blocks.LEAVES, Blocks.WOOD, Blocks.LEAVES,
            Blocks.WOOD, Blocks.LEAVES, Blocks.LEAVES,

            Blocks.WOOD, Blocks.WOOD, Blocks.LEAVES,
            Blocks.LEAVES, Blocks.WOOD, Blocks.LEAVES,
            Blocks.LEAVES, Blocks.LEAVES, Blocks.LEAVES,

            Blocks.LEAVES, Blocks.WOOD, Blocks.LEAVES,
            Blocks.LEAVES, Blocks.WOOD, Blocks.LEAVES,
            Blocks.WOOD, Blocks.LEAVES, Blocks.WOOD,

            Blocks.LEAVES, Blocks.LEAVES, Blocks.LEAVES,
            Blocks.WOOD, Blocks.WOOD, Blocks.WOOD,
            Blocks.LEAVES, Blocks.LEAVES, Blocks.LEAVES,
        ]),
        bytearray([
            Blocks.LEAVES, Blocks.LEAVES, Blocks.LEAVES,
            Blocks.LEAVES, Blocks.WOOD, Blocks.LEAVES,
            Blocks.WOOD, Blocks.LEAVES, Blocks.WOOD,

            Blocks.LEAVES, Blocks.LEAVES, Blocks.LEAVES,
            Blocks.LEAVES, Blocks.WOOD, Blocks.LEAVES,
            Blocks.LEAVES, Blocks.LEAVES, Blocks.LEAVES,

            Blocks.LEAVES, Blocks.LEAVES, Blocks.WOOD,
            Blocks.WOOD, Blocks.WOOD, Blocks.LEAVES,
            Blocks.LEAVES, Blocks.LEAVES, Blocks.LEAVES,

            Blocks.WOOD, Blocks.LEAVES, Blocks.LEAVES,
            Blocks.LEAVES, Blocks.WOOD, Blocks.LEAVES,
            Blocks.LEAVES, Blocks.LEAVES, Blocks.WOOD,
        ])
    ]


def treeTwigs():
    return [
        bytearray([
            Blocks.AIR, Blocks.LEAVES, Blocks.AIR,
            Blocks.LEAVES, Blocks.LEAVES, Blocks.LEAVES,
            Blocks.LEAVES, Blocks.LEAVES, Blocks.AIR,

            Blocks.AIR, Blocks.LEAVES, Blocks.LEAVES,
            Blocks.LEAVES, Blocks.WOOD, Blocks.AIR,
            Blocks.LEAVES, Blocks.LEAVES, Blocks.LEAVES,

            Blocks.LEAVES, Blocks.LEAVES, Blocks.LEAVES,
            Blocks.AIR, Blocks.WOOD, Blocks.LEAVES,
            Blocks.LEAVES, Blocks.LEAVES, Blocks.LEAVES,

            Blocks.LEAVES, Blocks.AIR, Blocks.LEAVES,
            Blocks.LEAVES, Blocks.WOOD, Blocks.LEAVES,
            Blocks.AIR, Blocks.AIR, Blocks.LEAVES,
        ]),
        bytearray([
            Blocks.AIR, Blocks.LEAVES, Blocks.AIR,
            Blocks.LEAVES, Blocks.WOOD, Blocks.LEAVES,
            Blocks.AIR, Blocks.LEAVES, Blocks.LEAVES,

            Blocks.LEAVES, Blocks.AIR, Blocks.LEAVES,
            Blocks.LEAVES, Blocks.WOOD, Blocks.LEAVES,
            Blocks.LEAVES, Blocks.LEAVES, Blocks.AIR,

            Blocks.LEAVES, Blocks.AIR, Blocks.LEAVES,
            Blocks.LEAVES, Blocks.WOOD, Blocks.LEAVES,
            Blocks.LEAVES, Blocks.LEAVES, Blocks.AIR,

            Blocks.LEAVES, Blocks.LEAVES, Blocks.LEAVES,
            Blocks.AIR, Blocks.WOOD, Blocks.AIR,
            Blocks.LEAVES, Blocks.LEAVES, Blocks.LEAVES,
        ]),
        bytearray([
            Blocks.AIR, Blocks.LEAVES, Blocks.LEAVES,
            Blocks.LEAVES, Blocks.WOOD, Blocks.AIR,
            Blocks.AIR, Blocks.LEAVES, Blocks.LEAVES,

            Blocks.LEAVES, Blocks.LEAVES, Blocks.LEAVES,
            Blocks.LEAVES, Blocks.WOOD, Blocks.LEAVES,
            Blocks.LEAVES, Blocks.LEAVES, Blocks.LEAVES,

            Blocks.LEAVES, Blocks.LEAVES, Blocks.AIR,
            Blocks.AIR, Blocks.WOOD, Blocks.LEAVES,
            Blocks.LEAVES, Blocks.LEAVES, Blocks.LEAVES,

            Blocks.LEAVES, Blocks.LEAVES, Blocks.LEAVES,
            Blocks.AIR, Blocks.WOOD, Blocks.LEAVES,
            Blocks.AIR, Blocks.LEAVES, Blocks.AIR,
        ])
    ]


def treeTrunks():
    return [
        bytearray([
            Blocks.AIR, Blocks.AIR, Blocks.AIR,
            Blocks.AIR, Blocks.WOOD, Blocks.AIR,
            Blocks.AIR, Blocks.AIR, Blocks.AIR,

            Blocks.AIR, Blocks.AIR, Blocks.AIR,
            Blocks.AIR, Blocks.WOOD, Blocks.AIR,
            Blocks.AIR, Blocks.AIR, Blocks.AIR,

            Blocks.AIR, Blocks.AIR, Blocks.AIR,
            Blocks.AIR, Blocks.WOOD, Blocks.AIR,
            Blocks.AIR, Blocks.AIR, Blocks.AIR,

            Blocks.AIR, Blocks.AIR, Blocks.AIR,
            Blocks.AIR, Blocks.WOOD, Blocks.WOOD,
            Blocks.AIR, Blocks.WOOD, Blocks.WOOD,
        ]),
        bytearray([
            Blocks.AIR, Blocks.AIR, Blocks.AIR,
            Blocks.AIR, Blocks.WOOD, Blocks.WOOD,
            Blocks.AIR, Blocks.WOOD, Blocks.WOOD,

            Blocks.AIR, Blocks.AIR, Blocks.AIR,
            Blocks.AIR, Blocks.WOOD, Blocks.WOOD,
            Blocks.AIR, Blocks.WOOD, Blocks.WOOD,

            Blocks.AIR, Blocks.AIR, Blocks.AIR,
            Blocks.AIR, Blocks.WOOD, Blocks.WOOD,
            Blocks.AIR, Blocks.WOOD, Blocks.WOOD,

            Blocks.AIR, Blocks.AIR, Blocks.AIR,
            Blocks.AIR, Blocks.WOOD, Blocks.WOOD,
            Blocks.AIR, Blocks.WOOD, Blocks.WOOD,
        ]),
        bytearray([
            Blocks.WOOD, Blocks.AIR, Blocks.AIR,
            Blocks.AIR, Blocks.AIR, Blocks.AIR,
            Blocks.AIR, Blocks.AIR, Blocks.AIR,

            Blocks.WOOD, Blocks.AIR, Blocks.AIR,
            Blocks.AIR, Blocks.AIR, Blocks.AIR,
            Blocks.AIR, Blocks.AIR, Blocks.AIR,

            Blocks.WOOD, Blocks.AIR, Blocks.AIR,
            Blocks.AIR, Blocks.AIR, Blocks.AIR,
            Blocks.AIR, Blocks.AIR, Blocks.AIR,

            Blocks.AIR, Blocks.AIR, Blocks.AIR,
            Blocks.AIR, Blocks.WOOD, Blocks.WOOD,
            Blocks.AIR, Blocks.WOOD, Blocks.WOOD,
        ]),
    ]


def treeRoots():
    return [
        bytearray([
            Blocks.DIRT, Blocks.DIRT, Blocks.DIRT,
            Blocks.DIRT, Blocks.WOOD, Blocks.WOOD,
            Blocks.WOOD, Blocks.WOOD, Blocks.WOOD,

            Blocks.DIRT, Blocks.DIRT, Blocks.DIRT,
            Blocks.DIRT, Blocks.WOOD, Blocks.WOOD,
            Blocks.WOOD, Blocks.DIRT, Blocks.DIRT,

            Blocks.DIRT, Blocks.DIRT, Blocks.DIRT,
            Blocks.WOOD, Blocks.WOOD, Blocks.DIRT,
            Blocks.DIRT, Blocks.DIRT, Blocks.DIRT,

            Blocks.DIRT, Blocks.DIRT, Blocks.DIRT,
            Blocks.WOOD, Blocks.WOOD, Blocks.DIRT,
            Blocks.DIRT, Blocks.WOOD, Blocks.DIRT,
        ]),
        bytearray([
            Blocks.DIRT, Blocks.DIRT, Blocks.DIRT,
            Blocks.DIRT, Blocks.WOOD, Blocks.WOOD,
            Blocks.DIRT, Blocks.WOOD, Blocks.WOOD,

            Blocks.DIRT, Blocks.DIRT, Blocks.WOOD,
            Blocks.DIRT, Blocks.WOOD, Blocks.WOOD,
            Blocks.WOOD, Blocks.WOOD, Blocks.WOOD,

            Blocks.WOOD, Blocks.DIRT, Blocks.DIRT,
            Blocks.DIRT, Blocks.WOOD, Blocks.WOOD,
            Blocks.DIRT, Blocks.WOOD, Blocks.WOOD,

            Blocks.DIRT, Blocks.DIRT, Blocks.DIRT,
            Blocks.WOOD, Blocks.WOOD, Blocks.WOOD,
            Blocks.DIRT, Blocks.WOOD, Blocks.WOOD,
        ]),
        bytearray([
            Blocks.WOOD, Blocks.DIRT, Blocks.DIRT,
            Blocks.DIRT, Blocks.WOOD, Blocks.WOOD,
            Blocks.DIRT, Blocks.WOOD, Blocks.WOOD,

            Blocks.WOOD, Blocks.DIRT, Blocks.DIRT,
            Blocks.DIRT, Blocks.DIRT, Blocks.WOOD,
            Blocks.WOOD, Blocks.DIRT, Blocks.DIRT,

            Blocks.WOOD, Blocks.DIRT, Blocks.DIRT,
            Blocks.DIRT, Blocks.WOOD, Blocks.DIRT,
            Blocks.WOOD, Blocks.DIRT, Blocks.DIRT,

            Blocks.WOOD, Blocks.DIRT, Blocks.WOOD,
            Blocks.DIRT, Blocks.WOOD, Blocks.DIRT,
            Blocks.DIRT, Blocks.DIRT, Blocks.WOOD,
        ]),
    ]


def getMaterial(name: str) -> int:
    if name.startswith('Grass'):
        return Blocks.GRASS_BLOCK
    elif name.startswith('Stone') and 'Smooth' in name:
        return Blocks.DOUBLE_SLAB
    elif name.startswith('Stone'):
        return Blocks.STONE
    elif 'Soil' in name:
        return Blocks.DIRT
    elif name.startswith('Mineral'):
        return Blocks.IRON_ORE
    elif name.startswith('Constructed'):
        return Blocks.DOUBLE_SLAB
    elif name.startswith('Feature'):
        return Blocks.OBSIDIAN
    elif name.startswith('Lava'):
        return Blocks.STATIONARY_LAVA
    elif name.startswith('Tree'):
        return Blocks.WOOD
    elif name.startswith('BurningTree'):
        return Blocks.WOOD
    elif name.startswith('River'):
        return Blocks.STATIONARY_WATER
    elif name.startswith('Frozen'):
        return Blocks.STATIONARY_WATER
    elif name.startswith('UnderworldGate'):
        return Blocks.BEDROCK
    elif name.startswith('MurkyPool'):
        return Blocks.STATIONARY_WATER
    elif name.startswith('GlowingFloor'):
        return Blocks.YELLOW_CLOTH
    else:
        return Blocks.SPONGE


COMPLEX_TILE_TO_BLOCK = {

}
