from generation.data.settlementData import SettlementData
from utils.worldModification import WorldModification

import utils.projectMath as projectMath
import lib.interfaceUtils as iu
from utils.constants import Constants

NODE_IN_ROAD: list = []
POSITION_OF_LANTERN: list = []


class Node:
    def __init__(self, point: list):
        self.point: list = point
        self.parent: Node = None
        self.cost: int = 0
        self.H: int = 0

    def move_cost(self, other):
        return 1


class LogNode:
    def __init__(self, point: list):
        self.point: list = point
        self.child = None


def manhattan(point: Node, point2: Node) -> int:
    return abs(point2.point[0] - point.point[0]) + abs(point2.point[1] - point.point[1])


def manhattanForCoord(point: list, point2: list):
    return abs(point2[0] - point[0]) + abs(point2[1] - point[1])


def children(point) -> list:
    x, z = point.point
    links: list = []

    for d in [(x - 1, z), (x, z - 1), (x, z + 1), (x + 1, z)]:
        links.append(Node([d[0], d[1]]))

    return links


def compareNode(node1: Node, node2: Node) -> int:
    if node1.H < node2.H:
        return 1
    elif node1.H == node2.H:
        return 0
    else:
        return -1


def isInClosedList(node: Node, closed_list: list) -> bool:
    for i in closed_list:
        if node.point == i.point:
            return True

    return False


def isInListWithInferiorCost(node: Node, node_list: list) -> bool:
    for i in node_list:
        if node.point == i.point:
            if i.H < node.H:
                return True
    return False


def isInRoad(coord: list) -> bool:
    for index in NODE_IN_ROAD:
        if coord in index:
            return True

    return False


def isInLantern(coord):
    for index in POSITION_OF_LANTERN:
        if coord in index:
            return True
    return False


def findClosestNodeInRoad(start_coordinate: list, goal_coordinate: list):
    closest_distance: int = manhattanForCoord(start_coordinate, goal_coordinate)
    coordinate_closest_distance: list = goal_coordinate

    temp: int

    for index in NODE_IN_ROAD:
        for node in index:
            temp = manhattanForCoord(start_coordinate, node)
            if temp < closest_distance:
                closest_distance = temp
                coordinate_closest_distance = node

    # print(closest_distance)
    return coordinate_closest_distance


def astar(start_coordinate: list, goal_coordinate: list, square_list: list):
    # the open and close set
    start: Node = Node(start_coordinate)
    goal: Node = Node(goal_coordinate)
    open_list: list = []
    closed_list: list = []
    # current point at start is the starting point
    current: Node = start
    current.H = manhattan(current, goal)
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
            NODE_IN_ROAD.append(path)

            return path[::-1]  # To reverse the path
        # For every neighbour of current node

        for node in children(current):
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
                if not (isInClosedList(node, closed_list)) and not (isInListWithInferiorCost(node, open_list)):
                    node.cost = current.cost + 1
                    node.H = node.cost + manhattan(node, goal)
                    node.parent = current
                    open_list.append(node)

        closed_list.append(current)
    raise ValueError('No Path Found')


def computeXEntry(xLocalPosition: int, cornerProjection, facingStruct, cornerStruct):
    x: int = xLocalPosition
    x += cornerProjection[facingStruct][0] * cornerStruct[0]
    x += cornerProjection[facingStruct][2] * cornerStruct[2]
    x += -cornerProjection[facingStruct][0] + cornerProjection[facingStruct][2]

    return x


def computeZEntry(zLocalPosition: int, cornerProjection, facingStruct, cornerStruct):
    z: int = zLocalPosition
    z += cornerProjection[facingStruct][1] * cornerStruct[1]
    z += cornerProjection[facingStruct][3] * cornerStruct[3]
    z += -cornerProjection[facingStruct][1] + cornerProjection[facingStruct][3]

    return z


def initRoad(listHouse: list, settlement_data: SettlementData, world_modification: WorldModification):
    NODE_IN_ROAD.clear()
    POSITION_OF_LANTERN.clear()

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

    # print(square_list)
    for indexFrom in range(0, len(lore_structures)):
        # To know if the house doesn't have parent...
        start: list = [0, 0]
        goal: list = [0, 0]

        indexTo: int = listHouse[indexFrom][5]
        if indexTo == -1:
            continue

        # House From
        facingStructFrom = lore_structures[indexFrom].preBuildingInfo["entry"]["facing"]
        cornerStructFrom = lore_structures[indexFrom].preBuildingInfo["corner"]
        entryStructFrom = [listHouse[indexFrom][0], listHouse[indexFrom][1], listHouse[indexFrom][2]]

        x = computeXEntry(entryStructFrom[0], cornerProjection, facingStructFrom, cornerStructFrom)
        y = entryStructFrom[1]
        z = computeZEntry(entryStructFrom[2], cornerProjection, facingStructFrom, cornerStructFrom)

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

        x = computeXEntry(entryStructTo[0], cornerProjection, facingStructTo, cornerStructTo)
        y = entryStructTo[1]
        z = computeZEntry(entryStructTo[2], cornerProjection, facingStructTo, cornerStructTo)

        goal = [x, z]
        goal = findClosestNodeInRoad(start, goal)

        while not (Constants.is_air(x, y + 2, z)) or Constants.is_air(x, y + 1, z):
            if Constants.is_air(x, y + 1, z):
                y -= 1
            if not (Constants.is_air(x, y + 2, z)):
                y += 1
        # print("stuck1")

        try:
            generateRoad(world_modification, start, goal, listHouse, square_list, settlement_data, entryStructFrom)
        except ValueError:
            print("ValueError, path can't be implemented there")


"""
Generating the path among 2 houses
"""


def generateRoad(world_modification: WorldModification, start: list, goal: list, list_house: list,
                 square_list: list, settlement_data: SettlementData, entryStructFrom):
    path = astar(start, goal, square_list)
    temp = 1

    yTemp = entryStructFrom[1]
    for block in path:
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
        world_modification.setBlock(block[0], y, block[1], "minecraft:air")
        world_modification.setBlock(block[0], y + 1, block[1], "minecraft:air")
        world_modification.setBlock(block[0], y + 2, block[1], "minecraft:air")
        world_modification.setBlock(block[0], y - 1, block[1], material)
        yTemp = y

    yTemp = entryStructFrom[1]
    for block in path:
        y = yTemp
        while not (Constants.is_air(block[0], y + 1, block[1])) or Constants.is_air(block[0], y, block[1]):
            if Constants.is_air(block[0], y, block[1]):
                y -= 1

            if not (Constants.is_air(block[0], y + 1, block[1])):
                y += 1

        while iu.getBlock(block[0], y, block[1]) == 'minecraft:water' or iu.getBlock(block[0], y,
                                                                                     block[1]) == 'minecraft:lava':
            y = y + 1

        if temp % 12 == 0 and temp < len(path) - 3:
            diffX = [-1, 0, 1, 0]
            diffZ = [0, -1, 0, 1]

            for i in [0, 1, 2, 3]:
                position = [block[0] + diffX[i], block[1] + diffZ[i]]
                if position not in path and not projectMath.isInHouse(list_house, position) and not isInRoad(position):
                    POSITION_OF_LANTERN.append([block[0], block[1]])
                    world_modification.setBlock(position[0], y - 1, position[1], 'minecraft:cobblestone')
                    world_modification.setBlock(position[0], y, position[1], 'minecraft:cobblestone_wall')
                    world_modification.setBlock(position[0], y + 1, position[1], 'minecraft:torch')
                    break

        temp += 1
        yTemp = y
