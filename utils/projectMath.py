import math


def isPointInCube(point, cube):
    if (cube[0] <= point[0] and cube[3] >= point[0]):
        if (cube[1] <= point[1] and cube[4] >= point[1]):
            if (cube[2] <= point[2] and cube[5] >= point[2]):
                return True
    return False


def isPointInSquare(point, square):
    if (square[0] <= point[0] and square[2] >= point[0]):
        if (square[1] <= point[1] and square[3] >= point[1]):
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


def isTwoRectOverlapse(position1, size1, position2, size2, moreSize):
    if position1[0] + size1[2] + moreSize < position2[0] + size2[0]:
        return False

    if position1[0] + size1[0] - moreSize > position2[0] + size2[2]:
        return False 

    if position1[1] + size1[3] + moreSize < position2[1] + size2[1]:
        return False

    if position1[1] + size1[1] - moreSize > position2[1] + size2[3]:
        return False

    return True


def rotatePointAround(origin, point, angle) :
    return [  
        round(math.cos(angle) * (point[0] - origin[0]) - math.sin(angle) * (point[1] - origin[1]) + origin[0], 4),
        round(math.sin(angle) * (point[0] - origin[0]) + math.cos(angle) * (point[1] - origin[1]) + origin[1], 4),
    ]
      