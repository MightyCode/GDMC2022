import math
import random

ORIENTATIONS = ["west", "north", "east", "south"]


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


def isTwoOffsetRectOverlaps(position1, size1, position2, size2):
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


def is2DPointEqual(point1: list, point2: list):
    return point1[0] == point2[0] and point1[1] == point2[1]


def is3DPointEqual(point1: list, point2: list):
    return is2DPointEqual(point1, point2) and point1[2] == point2[2]


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


def computeOrientation(p, b):
    angle: float = math.atan2((b[2] - p[2]), (b[0] - p[0]))

    if math.pi * -0.75 <= angle <= math.pi * -0.25:
        return "north"
    elif math.pi * -0.25 <= angle <= math.pi * 0.25:
        return "east"
    elif math.pi * 0.25 <= angle <= math.pi * 0.75:
        return "south"

    return "west"


def computeNewOrientation(orient: str, flip: int, rotation: int):
    result = orient

    if (flip == 1 or flip == 3) and result == "east":
        result = "west"
    elif (flip == 1 or flip == 3) and result == "west":
        result = "east"
    elif (flip == 2 or flip == 3) and result == "south":
        result = "north"
    elif (flip == 2 or flip == 3) and result == "north":
        result = "south"

    if result in ORIENTATIONS:
        result = ORIENTATIONS[(ORIENTATIONS.index(result) + rotation) % len(ORIENTATIONS)]

    return result


def makeListOrientationFrom(orient: str) -> list:
    if orient == "south":
        if random.randint(1, 2):
            return ["south", "west", "east", "north"]
        else:
            return ["south", "east", "west", "north"]

    elif orient == "west":
        if random.randint(1, 2):
            return ["west", "south", "north", "east"]
        else:
            return ["west", "north", "south", "east"]

    elif orient == "north":
        if random.randint(1, 2):
            return ["north", "west", "east", "south"]
        else:
            return ["north", "east", "west", "south"]

    if random.randint(1, 2):
        return ["east", "north", "south", "west"]
    else:
        return ["east", "south", "north", "west"]


def computeSquaredZoneWithNumber(number_zone: list, build_area: list) -> list:
    areas: list = []
    size_area: list = [build_area[3] - build_area[0] + 1, build_area[5] - build_area[2] + 1]

    for x in range(number_zone[0]):
        for z in range(number_zone[1]):
            areas.append([
                build_area[0] + x * size_area[0] // number_zone[0],
                build_area[1],
                build_area[2] + z * size_area[1] // number_zone[1],
                build_area[3] if x == number_zone[0] - 1 else build_area[0] + (x + 1) * size_area[0] // number_zone[0] - 1,
                build_area[4],
                build_area[5] if z == number_zone[1] - 1 else build_area[2] + (z + 1) * size_area[1] // number_zone[1] - 1
            ])

    return areas


def generateCorners(position: list, offsetCorner: list) -> list:
    return [
        [position[0] + offsetCorner[0], position[1], position[2] + offsetCorner[1]],
        [position[0] + offsetCorner[2], position[1], position[2] + offsetCorner[3]],
        [position[0] + offsetCorner[2], position[1], position[2] + offsetCorner[3]],
        [position[0] + offsetCorner[2], position[1], position[2] + offsetCorner[1]],
    ]


"""
Find the orientation of ordered triplet p, q, r
return 0 if p, q, r are collinear else 1 if Clockwise or 2-> CounterClockwise
"""
def orientation(p: list, q: list, r: list):
    temp: float = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])

    return 0 if temp == 0 else 1 if temp > 0 else 2


def convexHull(points):
    result: list = []

    l: int = 0
    p: int = l
    q: int

    while True:
        result.append(points[p])

        q = (p + 1) % len(points)

        for i in range(len(points)):
            if orientation(points[p], points[i], points[q]) == 2:
                q = i

        p = q

        if p == l:
            break

    return result


def rotateSquaredMatrix(matrix):
    N = len(matrix)

    # Consider all squares one by one
    for x in range(0, int(N / 2)):

        # Consider elements in group
        # of 4 in current square
        for y in range(x, N - x - 1):
            # store current cell in temp variable
            temp = matrix[x][y]

            # move values from right to top
            matrix[x][y] = matrix[y][N - 1 - x]

            # move values from bottom to right
            matrix[y][N - 1 - x] = matrix[N - 1 - x][N - 1 - y]

            # move values from left to bottom
            matrix[N - 1 - x][N - 1 - y] = matrix[N - 1 - y][x]

            # assign temp to left
            matrix[N - 1 - y][x] = temp

    return matrix


def manhattanForCoord(point: list, point2: list):
    return abs(point2[0] - point[0]) + abs(point2[1] - point[1])


def generatePlacesAmong(places: list, number: int):
    result: list = []

    i: int = 0
    while i < number and 0 < len(places):
        index: int = random.randint(1, len(places) - 1)

        result.append(places[index])
        del places[index]
        i += 1

    return result
