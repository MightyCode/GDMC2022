import lib.interface as iu


class Constants:
    # Ignored block value is the list of block that we want to ignore when we read the field

    IGNORED_BLOCKS = [
        'minecraft:void_air', 'minecraft:air', 'minecraft:cave_air', 'minecraft:water', 'minecraft:dark_oak_leaves',
        'minecraft:redstone_lamp', 'minecraft:cobblestone_wall', 'minecraft:lilac', 'minecraft:allium',
        'minecraft:white_tulip', 'minecraft:pink_tulip',
        'minecraft:oak_leaves', 'minecraft:leaves', 'minecraft:birch_leaves', 'minecraft:spruce_leaves',
        'minecraft:vine', 'minecraft:peony', 'minecraft:pumpkin', 'minecraft:blue_orchid', 'minecraft:lily_pad',
        'minecraft:orange_tulip', 'minecraft:azure_bluet',
        'minecraft:oak_log', 'minecraft:spruce_log', 'minecraft:birch_log', 'minecraft:jungle_log',
        'minecraft:acacia_log', 'minecraft:dark_oak_log', 'minecraft:red_tulip', 'minecraft:cornflower',
        'minecraft:grass', 'minecraft:snow', 'minecraft:acacia_leaves', 'minecraft:tall_grass', 'minecraft:poppy',
        'minecraft:dandelion', 'minecraft:brown_mushroom_block', 'minecraft:mushroom_stem', 'minecraft:rose_bush',
        'minecraft:red_mushroom_block',
        'minecraft:dead_bush', 'minecraft:cactus', 'minecraft:bamboo', 'minecraft:red_mushroom',
        'minecraft:brown_mushroom', 'minecraft:oxeye_daisy']

    FLOWERS = ['allium', 'white_tulip', 'pink_tulip', 'blue_orchid', 'orange_tulip', 'oxeye_daisy',
               'azure_bluet', 'red_tulip', 'dandelion', 'cactus', 'poppy', 'bamboo', 'red_mushroom', 'brown_mushroom',
               'cornflower']
    SINGLE_BLOC = ['minecraft:cobweb', 'minecraft:bell', 'minecraft:note_block', 'minecraft:hay_block',
                   'minecraft:melon', 'minecraft:carved_pumpkin']
    LIGHT_BLOC = ['minecraft:campfire', 'minecraft:lantern', 'minecraft:sea_lantern', 'minecraft:jack_o_lantern',
                  'minecraft:shroomlight']
    DOUBLE_BLOC = ['minecraft:bee_nest', 'minecraft:torch', 'minecraft:redstone_torch', 'minecraft:target',
                   'minecraft:skeleton_skull', 'minecraft:zombie_head', 'minecraft:creeper_head']

    """
    To get the height of a x,z position
    """

    @staticmethod
    def getHeight(x: int, z: int):
        y: int = 255

        while Constants.is_air(x, y, z) and y > 0:
            y -= 1

        return y

    """
    to get the height of a x,z position and taking water and lava in it
    """

    @staticmethod
    def getHeightRoad(x: int, z: int):
        y = 255
        while Constants.is_air(x, y, z) and y > 0 and not (
                iu.getBlock(x, y - 1, z) == "minecraft:water" or iu.getBlock(x, y - 1, z) == "minecraft:lava"):
            y -= 1

        return y

    """
    To know if it's a air block (or leaves and stuff)
    """

    @staticmethod
    def is_air(x: int, y: int, z: int):
        block = iu.getBlock(x, y - 1, z)
        if block in Constants.IGNORED_BLOCKS:
            # print("its air")
            return True
        else:
            # print("itsnotair")
            return False
