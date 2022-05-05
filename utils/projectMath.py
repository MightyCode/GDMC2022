import math


def isPointInCube(point, cube):
    if cube[0] <= point[0] <= cube[3]:
        if cube[1] <= point[1] <= cube[4]:
            if cube[2] <= point[2] <= cube[5]:
                return True
    return False


def isPointInSquare(point, square):
    if square[0] <= point[0] <= square[2]:
        if square[1] <= point[1] <= square[3]:
            return True

    return False


"""
xPos = x position of reference block
zPos = z position of reference block
CornersPos = Corners of house related to referenceBlock
house = Corners of other house we want to check
"""


def isTwoRectOverlapse(position1, size1, position2, size2):
    if position1[0] + size1[2] < position2[0] + size2[0]:
        return False

    if position1[0] + size1[0] > position2[0] + size2[2]:
        return False

    if position1[1] + size1[3] < position2[1] + size2[1]:
        return False

    if position1[1] + size1[1] > position2[1] + size2[3]:
        return False

    return True


def isTwoRectOverlaps(position1, size1, position2, size2, moreSize):
    if position1[0] + size1[2] + moreSize < position2[0] + size2[0]:
        return False

    if position1[0] + size1[0] - moreSize > position2[0] + size2[2]:
        return False

    if position1[1] + size1[3] + moreSize < position2[1] + size2[1]:
        return False

    if position1[1] + size1[1] - moreSize > position2[1] + size2[3]:
        return False

    return True


def rotatePointAround(origin, point, angle):
    return [
        round(math.cos(angle) * (point[0] - origin[0]) - math.sin(angle) * (point[1] - origin[1]) + origin[0], 4),
        round(math.sin(angle) * (point[0] - origin[0]) + math.cos(angle) * (point[1] - origin[1]) + origin[1], 4),
    ]


def isInHouse(list_house: list, coord: list):
    houses_to_verify: list = list_house.copy()

    while houses_to_verify:
        house: list = houses_to_verify.pop()
        if isPointInSquare(coord,
                           [house[0] + house[3][0], house[2] + house[3][1], house[0] + house[3][2],
                            house[2] + house[3][3]]):
            return True

    return False


def euclideanDistance2D(position1, position2):
    return math.sqrt(math.pow(position1[0] - position2[0], 2) + math.pow(position1[1] - position2[1], 2))


def computeSquaredZoneWitNumber(zone_number: list, build_area: list) -> list:
    areas: list = []

    for x in range(zone_number[0]):
        for z in range(zone_number[1]):
            areas.append([
                build_area[0] + x * zone_number[0],
                build_area[1],
                build_area[2] + z * zone_number[1],
                build_area[3] if x == zone_number[0] - 1 else build_area[0] + (
                        x + 1) * zone_number[0],
                build_area[4],
                build_area[5] if z == zone_number[1] - 1 else build_area[2] + (
                        z + 1) * zone_number[1]])

    return areas


def generateCorners(position: list, offsetCorner: list) -> list:
    return [
        [position[0] + offsetCorner[0], position[1], position[2] + offsetCorner[1]],
        [position[0] + offsetCorner[2], position[1], position[2] + offsetCorner[3]],
        [position[0] + offsetCorner[2], position[1], position[2] + offsetCorner[3]],
        [position[0] + offsetCorner[2], position[1], position[2] + offsetCorner[1]],
    ]
