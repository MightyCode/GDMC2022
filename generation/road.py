import random

from generation.data.settlementData import SettlementData
from generation.data.loreStructure import LoreStructure
from generation.structures.blockTransformation.oldStructureTransformation import OldStructureTransformation
from utils.worldModification import WorldModification
from generation.data.roadData import RoadData
from utils.constants import Constants
from utils.node import Node

import utils.projectMath as projectMath
import lib.interfaceUtils as iu
import utils.projectMath as pmath

class Road:
    def __init__(self):
        self.roads: list = []
        self.lanterns: list = []

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
        raise ValueError('No Path Found')

    def computeXEntry(self, xLocalPosition: int, cornerProjection, facingStruct, cornerStruct):
        x: int = xLocalPosition
        x += cornerProjection[facingStruct][0] * cornerStruct[0]
        x += cornerProjection[facingStruct][2] * cornerStruct[2]
        x += -cornerProjection[facingStruct][0] + cornerProjection[facingStruct][2]

        return x

    def computeZEntry(self, zLocalPosition: int, cornerProjection, facingStruct, cornerStruct):
        z: int = zLocalPosition
        z += cornerProjection[facingStruct][1] * cornerStruct[1]
        z += cornerProjection[facingStruct][3] * cornerStruct[3]
        z += -cornerProjection[facingStruct][1] + cornerProjection[facingStruct][3]

        return z

    def initRoad(self, listHouse: list, settlement_data: SettlementData) -> list:
        self.roads.clear()
        self.lanterns.clear()

        cornerProjection: dict = {
            "north": [0, 1, 0, 0],
            "south": [0, 0, 0, 1],
            "west": [1, 0, 0, 0],
            "east": [0, 0, 1, 0]
        }

        square_list: list = []
        lore_structures: list = settlement_data.village_model.lore_structures

        for index in range(0, len(lore_structures)):
            entry_temp: list = [listHouse[index][0], listHouse[index][1], listHouse[index][2]]

            square_list.append([entry_temp[0] + listHouse[index][3][0], entry_temp[2] + listHouse[index][3][1],
                                entry_temp[0] + listHouse[index][3][2], entry_temp[2] + listHouse[index][3][3]])

        result: list = []

        # print(square_list)
        for indexFrom in range(0, len(lore_structures)):
            # To know if the house doesn't have parent...
            start: list
            goal: list

            indexTo: int = listHouse[indexFrom][5]
            if indexTo == -1:
                continue

            # House From
            facingStructFrom = lore_structures[indexFrom].preBuildingInfo["entry"]["facing"]
            cornerStructFrom = lore_structures[indexFrom].preBuildingInfo["corner"]
            entryStructFrom = [listHouse[indexFrom][0], listHouse[indexFrom][1], listHouse[indexFrom][2]]

            x = self.computeXEntry(entryStructFrom[0], cornerProjection, facingStructFrom, cornerStructFrom)
            y = entryStructFrom[1]
            z = self.computeZEntry(entryStructFrom[2], cornerProjection, facingStructFrom, cornerStructFrom)

            while not (Constants.is_air(x, y + 2, z)) or Constants.is_air(x, y + 1, z):
                if Constants.is_air(x, y + 1, z):
                    y -= 1

                if not (Constants.is_air(x, y + 2, z)):
                    y += 1
            start = [x, z]

            # House to
            facingStructTo = lore_structures[indexTo].preBuildingInfo["entry"]["facing"]
            cornerStructTo = lore_structures[indexTo].preBuildingInfo["corner"]

            entryStructTo = [listHouse[indexTo][0], listHouse[indexTo][1] - 1, listHouse[indexTo][2]]

            x = self.computeXEntry(entryStructTo[0], cornerProjection, facingStructTo, cornerStructTo)
            y = entryStructTo[1]
            z = self.computeZEntry(entryStructTo[2], cornerProjection, facingStructTo, cornerStructTo)

            goal = [x, z]
            goal = self.findClosestNodeInRoad(start, goal)

            while not (Constants.is_air(x, y + 2, z)) or Constants.is_air(x, y + 1, z):
                if Constants.is_air(x, y + 1, z):
                    y -= 1
                if not (Constants.is_air(x, y + 2, z)):
                    y += 1
            # print("stuck1")

            roadData: RoadData = RoadData(lore_structures[indexFrom], lore_structures[indexTo])
            roadData.setPath(self.astar(start, goal, square_list), entryStructFrom, entryStructTo)
            result.append(roadData)

        return result


    """
    Generating the path among 2 houses
    """
    def generateRoad(self, roadDataArray: list, world_modification: WorldModification, list_house: list, settlement_data: SettlementData, terrain_modification):
        lore_structure: LoreStructure = LoreStructure()
        lore_structure.age = 1 if settlement_data.village_model.isDestroyed else 0
        old_transformation: OldStructureTransformation = OldStructureTransformation()
        old_transformation.setLoreStructure(lore_structure)

        for roadData in roadDataArray:
            yTemp = roadData.yEntry1[1]
            for block in roadData.path:
                y = yTemp
                material = 'minecraft:grass_path'
                while not (Constants.is_air(block[0], y + 1, block[1])) or Constants.is_air(block[0], y, block[1]):
                    if Constants.is_air(block[0], y, block[1]):
                        y -= 1
                    if not (Constants.is_air(block[0], y + 1, block[1])):
                        y += 1

                while iu.getBlock(block[0], y, block[1]) == 'minecraft:water':
                    y = y + 1
                    material = "minecraft:" + settlement_data.getMaterialReplacement("woodType") + "_planks"
                while iu.getBlock(block[0], y, block[1]) == 'minecraft:lava':
                    y = y + 1
                    material = "minecraft:nether_bricks"

                # Here, we need to check if there is a tree above the path, and if yes, we want to remove it
                terrain_modification.removeRecursivelyAt(world_modification, block[0], y, block[1])
                terrain_modification.removeRecursivelyAt(world_modification, block[0], y + 1, block[1])
                terrain_modification.removeRecursivelyAt(world_modification, block[0], y + 2, block[1])

                world_modification.setBlock(block[0], y - 1, block[1],
                                            old_transformation.replaceBlock(material))
                yTemp = y

        temp = 1
        for roadData in roadDataArray:
            yTemp = roadData.yEntry1[1]
            for block in roadData.path:
                y = yTemp
                while not (Constants.is_air(block[0], y + 1, block[1])) or Constants.is_air(block[0], y, block[1]):
                    if Constants.is_air(block[0], y, block[1]):
                        y -= 1

                    if not (Constants.is_air(block[0], y + 1, block[1])):
                        y += 1

                while iu.getBlock(block[0], y, block[1]) == 'minecraft:water' or iu.getBlock(block[0], y,
                                                                                             block[1]) == 'minecraft:lava':
                    y = y + 1

                if (3 + temp) % 12 == 0 and temp < len(roadData.path) - 3:
                    diffX: list = [-1, 0, 1, 0]
                    diffZ: list = [0, -1, 0, 1]
                    order: list = [0, 1, 2, 3]
                    random.shuffle(order)

                    for i in order:
                        position = [block[0] + diffX[i], block[1] + diffZ[i]]
                        if position not in roadData.path and not projectMath.isInHouse(list_house, position) and not self.isInRoad(position):
                            self.lanterns.append([position[0], position[1]])

                            world_modification.setBlock(position[0], y - 1, position[1], 'minecraft:cobblestone')
                            world_modification.setBlock(position[0], y, position[1], 'minecraft:cobblestone_wall')

                            if not settlement_data.village_model.isDestroyed:
                                world_modification.setBlock(position[0], y + 1, position[1], 'minecraft:torch')
                            break

                yTemp = y
                temp += 1
