import collections
import numpy

from generation.structures.baseStructure import *

"""
Hand made generated quarry
"""


class GeneratedQuarry(BaseStructure):
    def __init__(self):
        super(BaseStructure, self).__init__()
        self.list_of_blocks: numpy.ndarray = numpy.array([])
        self.computed_orientation: dict = {}

        self.useless_blocks = [
            'minecraft:air', 'minecraft:cave_air', 'minecraft:water', 'minecraft:lava'
                                                                      'minecraft:oak_leaves', 'minecraft:leaves',
            'minecraft:birch_leaves', 'minecraft:spruce_leaves'
                                      'minecraft:oak_log', 'minecraft:spruce_log', 'minecraft:birch_log',
            'minecraft:jungle_log', 'minecraft:acacia_log', 'minecraft:dark_oak_log',
            'minecraft:grass', 'minecraft:snow', 'minecraft:poppy'
                                                 'minecraft:dead_bush', "minecraft:cactus", "minecraft:sugar_cane"]

        self.entry: list = []
        self.fence_type: str = "minecraft:oak_fence"
        self.fence_gate_type: str = self.fence_type + "_gate"
        self.stripped_wood_type: str = "minecraft:stripped_oak_wood"

    def setupInfoAndGetCorners(self):
        self.setSize([random.randint(7, 14), random.randint(9, 21), random.randint(7, 14)])

        self.info["mainEntry"]["position"] = [int(self.size[0] / 2), self.size[1] - 5, 0]

        return self.getCornersLocalPositionsAllFlipRotation(self.info["mainEntry"]["position"])

    def getNextBuildingInformation(self, flip: int, rotation: int) -> dict:
        self.info["mainEntry"]["facing"] = "north"

        return {
            "entry": {
                "position": self.info["mainEntry"]["position"],
                "facing": self.getFacingMainEntry(flip, rotation)
            },
            "size": self.size,
            "corner": self.getCornersLocalPositions(self.info["mainEntry"]["position"].copy(), flip, rotation)
        }

    def build(self, world_modification, building_conditions, chest_generation):
        self.setSize(building_conditions["size"])
        self.entry = building_conditions["referencePoint"].copy()
        self.computeOrientation(building_conditions["rotation"], building_conditions["flip"])

        if building_conditions["flip"] == 1 or building_conditions["flip"] == 3:
            building_conditions["referencePoint"][0] = self.size[0] - 1 - building_conditions["referencePoint"][0]
        if building_conditions["flip"] == 2 or building_conditions["flip"] == 3:
            building_conditions["referencePoint"][2] = self.size[2] - 1 - building_conditions["referencePoint"][2]

        woodType: str = "*woodType*"
        result = util.changeNameWithBalise(woodType, building_conditions["replacements"])
        if result[0] >= 0:
            woodType = result[1]
        else:
            woodType = "oak"

        self.fence_type = "minecraft:" + woodType + "_fence"
        self.fence_gate_type = self.fence_type + "_gate"
        self.stripped_wood_type = "minecraft:stripped_" + woodType + "_wood"

        self.list_of_blocks = numpy.array([])
        ## Building the quarry.
        for dy in range(self.size_y()):
            for dx in range(1, self.size_x() - 1):
                for dz in range(1, self.size_z() - 1):
                    # Get all the block we chunk
                    position = self.returnWorldPosition([dx, dy, dz], building_conditions["flip"],
                                                        building_conditions["rotation"],
                                                        building_conditions["referencePoint"],
                                                        building_conditions["position"])

                    block = world_modification.interface.getBlock(position[0], position[1], position[2])
                    if block not in self.useless_blocks:
                        self.list_of_blocks = numpy.append(self.list_of_blocks, block)

                        # Fill the area with air block

        from_block = self.returnWorldPosition([1, 0, 1], building_conditions["flip"],
                                              building_conditions["rotation"], building_conditions["referencePoint"],
                                              building_conditions["position"])
        to_block = self.returnWorldPosition([self.size_x() - 2, self.size_y() - 1, self.size_z() - 2],
                                            building_conditions["flip"],
                                            building_conditions["rotation"], building_conditions["referencePoint"],
                                            building_conditions["position"])

        world_modification.fillBlocks(from_block[0], from_block[1], from_block[2], to_block[0], to_block[1],
                                      to_block[2],
                                      "minecraft:air")

        # Add the fences
        self.addFencesToQuarry(world_modification, building_conditions)
        # Add the fence gate and the ladders
        self.addFenceGateToQuarry(world_modification, building_conditions)
        # Add the items to the chests
        self.addChestToQuarry(world_modification, building_conditions, self.list_of_blocks)

        torch_positions: list = [[1, int(self.size_z() / 2)], [int(self.size_x() / 2), self.size_z() - 2],
                                 [self.size_x() - 2, int(self.size_z() / 2)]]
        orientations: list = ["east", "north", "west"]

        for i in range(len(torch_positions)):
            position = self.returnWorldPosition(
                [torch_positions[i][0], int(self.size_y() / 3), torch_positions[i][1]],
                building_conditions["flip"], building_conditions["rotation"],
                building_conditions["referencePoint"], building_conditions["position"])
            # Set a chest
            world_modification.setBlock(position[0], position[1], position[2],
                                        "minecraft:wall_torch[" + self.convertProperty("facing", orientations[i]) + "]")

    """
    Add chest at the bottom of quarry and fill it with blocks removed by the quarry
    """

    def addChestToQuarry(self, world_modification, building_conditions, list_of_blocks: numpy.ndarray):
        position = self.returnWorldPosition(
            [1, 0, 1], building_conditions["flip"],
            building_conditions["rotation"], building_conditions["referencePoint"], building_conditions["position"])

        # Set a chest
        world_modification.setBlock(position[0], position[1], position[2],
                                    "minecraft:chest[" + self.convertProperty("facing", "south") + "]",
                                    placeImmediately=True)

        counter = collections.Counter(list_of_blocks)
        items = counter.items()
        itemsList: list_of_blocks = []
        for i in items:
            # If there is more than one stack of block (64)
            if i[1] > 64:
                x = i[1] / 64
                y = math.floor(x)
                for z in range(0, y):
                    newList: list_of_blocks = [i[0], 64]
                    itemsList.append(newList)
            else:
                sublist: list_of_blocks = [i[0], i[1]]
                itemsList.append(sublist)

        util.addItemChest(position[0], position[1], position[2], itemsList)

    def addFencesToQuarry(self, worldModif, buildingCondition):
        # Add the fences for the quarry

        fenceSideUpperPosition = self.size_y() - 3
        lengths = [self.size_x(), self.size_z(), self.size_x(), self.size_z()]
        multiplier = [[1, 0], [0, 1], [1, 0], [0, 1]]
        positions = [[0, 0], [0, 0], [0, self.size_z() - 1], [self.size_x() - 1, 0]]

        for i in [0, 1, 2, 3]:
            for j in range(lengths[i]):
                for y in range(fenceSideUpperPosition):
                    localPosition = [positions[i][0] + j * multiplier[i][0], y, positions[i][1] + j * multiplier[i][1]]
                    position = self.returnWorldPosition(
                        localPosition, buildingCondition["flip"],
                        buildingCondition["rotation"], buildingCondition["referencePoint"],
                        buildingCondition["position"])

                    block = worldModif.interface.getBlock(position[0], position[1], position[2])
                    if block in self.useless_blocks or y == fenceSideUpperPosition - 1:
                        worldModif.setBlock(position[0], position[1], position[2],
                                            self.fence_type + "[waterlogged=false]")

    def addFenceGateToQuarry(self, world_modification, building_conditions):
        # Add the fence gate
        position: list = self.returnWorldPosition(
            [self.entry[0], self.entry[1] + 2, self.entry[2]],
            building_conditions["flip"], building_conditions["rotation"], building_conditions["referencePoint"],
            building_conditions["position"])

        world_modification.setBlock(position[0], position[1], position[2], "minecraft:air")

        world_modification.setBlock(position[0], position[1] - 1, position[2],
                                    self.fence_gate_type + "[" + self.convertProperty("facing", "north") + "]")

        positions: list = [[-2, 2], [-1, 2], [-1, 3], [0, 3], [1, 3], [1, 2], [2, 2]]
        for pos in positions:
            position = self.returnWorldPosition(
                [self.entry[0] + pos[0],
                 self.entry[1] + pos[1],
                 self.entry[2]],
                building_conditions["flip"], building_conditions["rotation"], building_conditions["referencePoint"],
                building_conditions["position"])
            world_modification.setBlock(position[0], position[1], position[2], self.fence_type + "[waterlogged=false]")

        positions = [[-1, 4], [0, 4], [1, 4]]
        for pos in positions:
            position = self.returnWorldPosition(
                [self.entry[0] + pos[0],
                 self.entry[1] + pos[1],
                 self.entry[2]],
                building_conditions["flip"], building_conditions["rotation"], building_conditions["referencePoint"],
                building_conditions["position"])
            world_modification.setBlock(position[0], position[1], position[2], "minecraft:torch")

        # Add the ladders
        for wood in range(self.entry[1] + 1):
            position = self.returnWorldPosition(
                [self.entry[0], wood, self.entry[2]],
                building_conditions["flip"], building_conditions["rotation"], building_conditions["referencePoint"],
                building_conditions["position"])

            world_modification.setBlock(position[0], position[1], position[2], self.stripped_wood_type)

            position = self.returnWorldPosition(
                [self.entry[0], wood, self.entry[2] + 1],
                building_conditions["flip"], building_conditions["rotation"], building_conditions["referencePoint"],
                building_conditions["position"])

            world_modification.setBlock(position[0], position[1], position[2],
                                        "minecraft:ladder[" + self.convertProperty("facing",
                                                                                   "south") + ",waterlogged=false]")

        # print("Finish building : basicQuarry")
