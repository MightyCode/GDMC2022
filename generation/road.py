import random

from generation.data.settlementData import SettlementData
from generation.data.loreStructure import LoreStructure
from generation.structures.blockTransformation.oldStructureTransformation import OldStructureTransformation
from utils import util
from utils.worldModification import WorldModification
from generation.data.roadData import RoadData
from utils.node import Node

import utils.projectMath as projectMath
import lib.interfaceUtils as iu
import utils.projectMath as pmath


class Road:
    CORNER_PROJECTION: dict = {
        "north": [0, 1, 0, 0],
        "south": [0, 0, 0, 1],
        "west": [1, 0, 0, 0],
        "east": [0, 0, 1, 0]
    }

    def __init__(self, area: list):
        self.area = area
        self.roads: list = []
        self.lanterns: list = []
        self.square_list: list = []
        self.roadParts: list = []

    def isInRoad(self, coord: list) -> bool:
        for index in self.roads:
            if coord in index:
                return True

        return False

    def isInLantern(self, coord):
        for index in self.lanterns:
            if coord in index:
                return True

        return False

    def findClosestNodeInRoad(self, start_coordinate: list, goal_coordinate: list):
        closest_distance: int = pmath.manhattanForCoord(start_coordinate, goal_coordinate)
        coordinate_closest_distance: list = goal_coordinate

        temp: int

        for index in self.roads:
            for node in index:
                temp = pmath.manhattanForCoord(start_coordinate, node)
                if temp < closest_distance:
                    closest_distance = temp
                    coordinate_closest_distance = node

        # print(closest_distance)
        return coordinate_closest_distance

    def astar(self, start_coordinate: list, goal_coordinate: list, square_list: list):
        # the open and close set
        start: Node = Node(start_coordinate)
        goal: Node = Node(goal_coordinate)
        open_list: list = []
        closed_list: list = []
        # current point at start is the starting point
        current: Node = start
        current.H = current.manhattan(goal)
        # add it to the openset
        open_list.append(current)

        while open_list:
            # find the item in the open set with the lowest G+H score
            temp = open_list[0].H
            for i in open_list:
                if i.H <= temp:
                    temp = i.H
                    current = i
            open_list.remove(current)
            # If we are at the goal
            if current.point == goal.point:
                path = [current.point]
                while current.parent:
                    path.append(current.parent.point)
                    current = current.parent
                self.roads.append(path)

                return path[::-1]  # To reverse the path
            # For every neighbour of current node

            for node in current.children():
                # test here if the children is in a house
                # print(node.point)
                if node.point == goal_coordinate:
                    # print("TROUVE")
                    open_list.append(node)
                is_not_in_square = True
                for square_house in square_list:
                    if projectMath.isPointInSquare(node.point, square_house):
                        is_not_in_square = False
                # if abs(floodFill.getHeight(node.point[0],node.point[1],ws) - floodFill.getHeight(current.point[0],current.point[1],ws)) > 2:
                #	is_not_in_square = False

                if is_not_in_square:
                    if not (node.isInClosedList(closed_list)) and not (node.isInListWithInferiorCost(open_list)):
                        node.cost = current.cost + 1
                        node.H = node.cost + node.manhattan(goal)
                        node.parent = current
                        open_list.append(node)

            closed_list.append(current)

        print("Warning : No path found")
        return []

    def computeXEntry(self, xLocalPosition: int, facingStruct, cornerStruct):
        x: int = xLocalPosition
        x += self.CORNER_PROJECTION[facingStruct][0] * cornerStruct[0]
        x += self.CORNER_PROJECTION[facingStruct][2] * cornerStruct[2]
        x += -self.CORNER_PROJECTION[facingStruct][0] + self.CORNER_PROJECTION[facingStruct][2]

        return x

    def computeZEntry(self, zLocalPosition: int, facingStruct, cornerStruct):
        z: int = zLocalPosition
        z += self.CORNER_PROJECTION[facingStruct][1] * cornerStruct[1]
        z += self.CORNER_PROJECTION[facingStruct][3] * cornerStruct[3]
        z += -self.CORNER_PROJECTION[facingStruct][1] + self.CORNER_PROJECTION[facingStruct][3]

        return z

    @staticmethod
    def computeSquareList(list_house: list) -> list:
        result: list = []
        entry_temp: list

        for index in range(0, len(list_house)):
            entry_temp = [list_house[index][0], list_house[index][1], list_house[index][2]]

            result.append([entry_temp[0] + list_house[index][3][0], entry_temp[2] + list_house[index][3][1],
                           entry_temp[0] + list_house[index][3][2], entry_temp[2] + list_house[index][3][3]])

        return result

    def addRoad(self, start_complete: list, goal_complete: list, lore_structure_from: LoreStructure = None,
                lore_structure_to: LoreStructure = None):
        start: list = [start_complete[0], start_complete[2]]
        goal: list = self.findClosestNodeInRoad(start, [goal_complete[0], goal_complete[2]])

        roadData: RoadData = RoadData(lore_structure_from, lore_structure_to)
        roadData.setPath(self.astar(start, goal, self.square_list), start_complete[1], goal_complete[1])

        self.roadParts.append(roadData)

    def initRoad(self, list_house: list, settlement_data: SettlementData) -> list:
        self.roads.clear()
        self.lanterns.clear()
        self.roadParts.clear()

        self.square_list: list = self.computeSquareList(list_house)
        lore_structures: list = settlement_data.village_model.lore_structures

        # print(square_list)
        for indexFrom in range(0, len(lore_structures)):
            # To know if the house doesn't have parent...
            start: list
            goal: list

            indexTo: int = list_house[indexFrom][5]
            if indexTo == -1:
                continue

            # House From
            facingStructFrom = lore_structures[indexFrom].preBuildingInfo["entry"]["facing"]
            cornerStructFrom = lore_structures[indexFrom].preBuildingInfo["corner"]
            entryStructFrom = [list_house[indexFrom][0], list_house[indexFrom][1], list_house[indexFrom][2]]

            x = self.computeXEntry(entryStructFrom[0], facingStructFrom, cornerStructFrom)
            z = self.computeZEntry(entryStructFrom[2], facingStructFrom, cornerStructFrom)

            start_complete = [x, entryStructFrom[1], z]

            # House to
            facingStructTo = lore_structures[indexTo].preBuildingInfo["entry"]["facing"]
            cornerStructTo = lore_structures[indexTo].preBuildingInfo["corner"]

            entryStructTo = [list_house[indexTo][0], list_house[indexTo][1] - 1, list_house[indexTo][2]]

            x = self.computeXEntry(entryStructTo[0], facingStructTo, cornerStructTo)
            z = self.computeZEntry(entryStructTo[2], facingStructTo, cornerStructTo)

            goal_complete = [x, entryStructTo[1], z]

            self.addRoad(start_complete, goal_complete, lore_structures[indexFrom], lore_structures[indexTo])

        return self.roadParts

    """
    Generating the path among 2 houses
    """

    def generateRoad(self, world_modification: WorldModification, list_house: list,
                     settlement_data: SettlementData, terrain_modification):
        lore_structure: LoreStructure = LoreStructure()
        lore_structure.age = 1 if settlement_data.village_model.isDestroyed else 0
        old_transformation: OldStructureTransformation = OldStructureTransformation()
        old_transformation.setLoreStructure(lore_structure)

        for roadData in self.roadParts:
            if roadData is None:
                continue

            for block in roadData.path:
                y = util.getHighestNonAirBlock(block[0], block[1], block[0] - self.area[0], block[1] - self.area[2])
                material = 'minecraft:grass_path'
                # Here, we need to check if there is a tree above the path, and if yes, we want to remove it
                terrain_modification.removeRecursivelyAt(world_modification, block[0], y, block[1])
                world_modification.setBlock(block[0], y + 1, block[1], "minecraft:air")
                terrain_modification.removeRecursivelyAt(world_modification, block[0], y + 1, block[1])
                world_modification.setBlock(block[0], y + 2, block[1], "minecraft:air")
                terrain_modification.removeRecursivelyAt(world_modification, block[0], y + 2, block[1])

                if iu.getBlock(block[0], y, block[1]) == 'minecraft:water':
                    material = "minecraft:" + settlement_data.getMaterialReplacement("woodType") + "_planks"
                elif iu.getBlock(block[0], y, block[1]) == 'minecraft:lava':
                    material = "minecraft:nether_bricks"

                world_modification.setBlock(block[0], y, block[1], old_transformation.replaceBlock(material))

        for roadData in self.roadParts:
            counter = 1
            for block in roadData.path:
                y = util.getHighestNonAirBlock(block[0], block[1], block[0] - self.area[0], block[1] - self.area[2])

                if (3 + counter) % 12 != 0 or counter >= len(roadData.path) - 3:
                    counter += 1
                    continue

                diffX: list = [-1, 0, 1, 0]
                diffZ: list = [0, -1, 0, 1]
                order: list = [0, 1, 2, 3]
                random.shuffle(order)

                for i in order:
                    position = [block[0] + diffX[i], block[1] + diffZ[i]]
                    if position in roadData.path \
                        or projectMath.isInHouse(list_house, position) \
                        or self.isInRoad(position):

                        continue

                    self.lanterns.append([position[0], position[1]])

                    # Per default / Village tier 0
                    copy: dict = settlement_data.getMatRepDeepCopy()
                    block_support: str = util.changeNameWithReplacements('minecraft:*woodType*_log', copy)[1]
                    block_wall: str = util.changeNameWithReplacements('minecraft:*woodType*_fence', copy)[1]
                    light_source: str = 'minecraft:torch'

                    if settlement_data.village_model.tier >= 1:
                        block_support = 'minecraft:cobblestone'
                        block_wall = 'minecraft:cobblestone_wall'

                    if settlement_data.village_model.tier >= 2:
                        light_source = "minecraft:lantern"

                    world_modification.setBlock(position[0], y, position[1], old_transformation.replaceBlock(block_support))
                    world_modification.setBlock(position[0], y + 1, position[1], old_transformation.replaceBlock(block_wall))

                    if not settlement_data.village_model.isDestroyed:
                        world_modification.setBlock(position[0], y + 2, position[1], old_transformation.replaceBlock(light_source))
                    break

                counter += 1
