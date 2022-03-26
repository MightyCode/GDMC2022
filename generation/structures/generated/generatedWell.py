from generation.structures.baseStructure import BaseStructure
from generation.buildingCondition import BuildingCondition
import utils.util as util


class GeneratedWell(BaseStructure):
    def __init__(self):
        super(BaseStructure, self).__init__()
        self.plankType = "minecraft:acacia_planks"
        self.entry = None
        self.uselessBlocks = [
            'minecraft:air', 'minecraft:cave_air', 'minecraft:water', 'minecraft:lava'
                                                                      'minecraft:oak_leaves', 'minecraft:leaves',
            'minecraft:birch_leaves', 'minecraft:spruce_leaves'
                                      'minecraft:oak_log', 'minecraft:spruce_log', 'minecraft:birch_log',
            'minecraft:jungle_log', 'minecraft:acacia_log', 'minecraft:dark_oak_log',
            'minecraft:grass', 'minecraft:snow', 'minecraft:poppy'
                                                 'minecraft:dead_bush', "minecraft:cactus", "minecraft:sugar_cane"]

    def setupInfoAndGetCorners(self):
        self.setSize([6, 9, 6])
        self.info["mainEntry"]["position"] = [int(self.size[0] / 2), self.size[1] - 5, 0]

        return self.getCornersLocalPositionsAllFlipRotation(self.info["mainEntry"]["position"])

    def getNextBuildingInformation(self, flip, rotation):
        info = {
            "size": self.size,
            "mainEntry": {
                "facing": "north"
            },
            "entry": {
                "position": self.info["mainEntry"]["position"],
                "facing": self.getFacingMainEntry(flip, rotation)
            },
            "corner": self.getCornersLocalPositions(self.info["mainEntry"]["position"].copy(), flip, rotation)
        }

        return info

    def build(self, world_modifications, building_conditions: BuildingCondition, chest_generation, block_transformations: list):
        self.setSize(building_conditions.size)
        self.entry = building_conditions.referencePoint.copy()
        self.computeOrientation(building_conditions.rotation, building_conditions.flip)
        self.block_transformation = block_transformations

        if building_conditions.flip == 1 or building_conditions.flip == 3:
            building_conditions.referencePoint[0] = self.size[0] - 1 - building_conditions.referencePoint[0]
        if building_conditions.flip == 2 or building_conditions.flip == 3:
            building_conditions.referencePoint[2] = self.size[2] - 1 - building_conditions.referencePoint[2]

        woodType = "*woodType*"
        result = util.changeNameWithBalise(woodType, building_conditions.replacements)
        if result[0] >= 0:
            woodType = result[1]
        else:
            woodType = "oak"

        self.plankType = "minecraft:" + woodType + "_planks"

        self.addStoneBricks(world_modifications, building_conditions)
        self.addStoneBrickStairs(world_modifications, building_conditions)
        self.addWoodAroundTheWell(world_modifications, building_conditions)

        # Add water
        fromBlock = self.returnWorldPosition(
            [2, int(self.size_y()), 2], building_conditions.flip,
            building_conditions.rotation, building_conditions.referencePoint, building_conditions.position)

        toBlock = self.returnWorldPosition(
            [3, int(self.size_y()), 3], building_conditions.flip,
            building_conditions.rotation, building_conditions.referencePoint, building_conditions.position)

        world_modifications.fillBlocks(fromBlock[0], fromBlock[1] - 3, fromBlock[2], toBlock[0], toBlock[1] - 7, toBlock[2],
                              "minecraft:air")

        self.addStoneBricks(world_modifications, building_conditions)
        self.addStoneBrickStairs(world_modifications, building_conditions)
        self.addWoodAroundTheWell(world_modifications, building_conditions)

        world_modifications.fillBlocks(fromBlock[0], fromBlock[1] - 6, fromBlock[2], toBlock[0], toBlock[1] - 5,
                                       toBlock[2], "minecraft:water")

        self.applyBlockTransformationThenFill(world_modifications, fromBlock[0], fromBlock[1] - 8, fromBlock[2], toBlock[0],
                                              toBlock[1] - 9,
                                              toBlock[2],
                                              "minecraft:stone_bricks")

    def addWoodAroundTheWell(self, world_modification, building_conditions: BuildingCondition):
        positions = [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [1, 5], [2, 5], [3, 5], [4, 5], [5, 5],
                     [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [5, 1], [5, 2], [5, 3], [5, 4]]
        # Add wood plank
        for i in range(len(positions)):
            localPosition = [positions[i][0], self.size_y() - 5, positions[i][1]]
            position = self.returnWorldPosition(
                localPosition, building_conditions.flip,
                building_conditions.rotation, building_conditions.referencePoint, building_conditions.position)

            self.applyBlockTransformationThenPlace(world_modification, position[0], position[1], position[2],
                                                   self.plankType)

    def addStoneBrickStairs(self, world_modification, building_conditions: BuildingCondition):
        # Add stairs
        positions = [[2, 4], [3, 4], [1, 2], [1, 3], [2, 1], [3, 1], [4, 2], [4, 3]]
        orientations = ["north", "north", "east", "east", "south", "south", "west", "west"]
        for i in range(len(positions)):
            localPosition = positions[i][0], self.size_y() - 4, positions[i][1]
            position = self.returnWorldPosition(
                localPosition, building_conditions.flip,
                building_conditions.rotation, building_conditions.referencePoint, building_conditions.position)

            self.applyBlockTransformationThenPlace(world_modification, position[0], position[1], position[2],
                                                   "minecraft:stone_brick_stairs[" + self.convertProperty('facing',
                                                                                                          orientations[
                                                                                                              i]) + "]")

            for k in range(1, 4):
                self.applyBlockTransformationThenPlace(world_modification, position[0], position[1] - k, position[2],
                                                       "minecraft:stone_bricks")

            for j in range(1, 3):
                self.applyBlockTransformationThenPlace(world_modification, position[0], position[1] + 3, position[2],
                                                       "minecraft:stone_brick_slab")

    def addStoneBricks(self, world_modification, building_conditions: BuildingCondition):
        # Add stones to the corner
        positions = [[1, 1], [1, 4], [4, 1], [4, 4]]
        for i in range(len(positions)):
            localPosition = positions[i][0], self.size_y() - 4, positions[i][1]
            position = self.returnWorldPosition(
                localPosition, building_conditions.flip,
                building_conditions.rotation, building_conditions.referencePoint, building_conditions.position)

            self.applyBlockTransformationThenPlace(world_modification, position[0], position[1], position[2],
                                                   "minecraft:chiseled_stone_bricks")
            self.applyBlockTransformationThenPlace(world_modification, position[0], position[1] - 1, position[2],
                                                   "minecraft:stone_bricks")

            j = 3
            for j in range(1, 3):
                # Add cobblestone walls
                self.applyBlockTransformationThenPlace(world_modification, position[0], position[1] + j, position[2],
                                                       "minecraft:cobblestone_wall")

            # Add stone brick slabs
            self.applyBlockTransformationThenPlace(world_modification, position[0], position[1] + j + 1, position[2],
                                                   "minecraft:stone_brick_slab")

            # Add stones upside the well
        positions = [[2, 2], [2, 3], [3, 2], [3, 3]]
        for i in range(len(positions)):
            localPosition = positions[i][0], self.size_y() - 1, positions[i][1]
            position = self.returnWorldPosition(
                localPosition, building_conditions.flip,
                building_conditions.rotation, building_conditions.referencePoint, building_conditions.position)

            self.applyBlockTransformationThenPlace(world_modification, position[0], position[1], position[2],
                                                   "minecraft:chiseled_stone_bricks")
