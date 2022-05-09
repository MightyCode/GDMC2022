import copy
import math

from PIL import Image

import matplotlib.pyplot as plt
import utils.projectMath as pmath


class WallConstruction:
    BOUNDING_RECTANGULAR: int = 0
    BOUNDING_CONVEX_HULL: int = 1

    MODEL_LINE: int = 0
    MODEL_CORNER: int = 1
    MODEL_CORNER_INTERIOR: int = 2

    def __init__(self, village, zone_size=15):
        self.village = village
        self.zone_size: int = zone_size
        self.detection_grid_size: list = [0, 0]
        self.area: tuple = ()
        self.connected_area: list = []

        # List of defined dict
        self.wall_list: list = []

        self.bounding_type: int = self.BOUNDING_RECTANGULAR
        # Bounding depending variables

        self.wall_simplification: list = [-1, -1, -1, -1]
        self.hull: list = []
        self.matrix: list = []

    def setConstructionZone(self, area):
        self.detection_grid_size = [0, 0]
        self.area = area

        for i in [0, 1]:
            size: int = area[(i * 2) + 3] - area[i * 2]

            while size > 0:
                self.detection_grid_size[i] += 1
                size -= self.zone_size

        self.connected_area = [False] * (self.detection_grid_size[0] * self.detection_grid_size[1])

    def returnPositionPoint(self, point):
        grid_position: list = [0, 0]
        positions: float

        for i in [0, 1]:
            positions = point[i] - self.area[i * 2]

            grid_position[i] = positions // self.zone_size

        return grid_position

    def addRectangle(self, rectangle):
        connected_rectangle: list = [-1, -1, -1, -1]

        connected_rectangle[0], connected_rectangle[1] = self.returnPositionPoint(rectangle[0:2])
        connected_rectangle[2], connected_rectangle[3] = self.returnPositionPoint(rectangle[2:])

        if connected_rectangle[0] > self.detection_grid_size[0] \
                or connected_rectangle[1] > self.detection_grid_size[1] \
                or connected_rectangle[2] < 0 \
                or connected_rectangle[3] < 0:
            return

        for x in range(connected_rectangle[0], connected_rectangle[2] + 1):
            for z in range(connected_rectangle[1], connected_rectangle[3] + 1):
                if 0 <= x < self.detection_grid_size[0] \
                        and 0 <= z < self.detection_grid_size[1]:
                    self.connected_area[z * self.detection_grid_size[0] + x] = True

    def addPoints(self, point):
        grid_position: list = [-1, -1]
        if len(point) == 3:
            grid_position = self.returnPositionPoint([point[0], point[2]])
        elif len(point) == 2:
            grid_position = self.returnPositionPoint(point)

        if 0 <= grid_position[0] < self.detection_grid_size[0] \
                and 0 <= grid_position[1] < self.detection_grid_size[1]:
            self.connected_area[grid_position[1] * self.detection_grid_size[0] + grid_position[0]] = True

    def computeWall(self, bounding_type: int = BOUNDING_RECTANGULAR):
        self.bounding_type = bounding_type

        if self.bounding_type == self.BOUNDING_RECTANGULAR:
            self.computeRectangular()
        elif self.bounding_type == self.BOUNDING_CONVEX_HULL:
            self.computeConvexFull()

    def computeRectangular(self):
        self.wall_simplification = [self.detection_grid_size[0], self.detection_grid_size[1], -1, -1]

        for z in range(self.detection_grid_size[1]):
            for x in range(self.detection_grid_size[0]):
                if self.connected_area[z * self.detection_grid_size[0] + x]:
                    if x > self.wall_simplification[2]:
                        self.wall_simplification[2] = x
                    if x < self.wall_simplification[0]:
                        self.wall_simplification[0] = x

                    if z > self.wall_simplification[3]:
                        self.wall_simplification[3] = z
                    if z < self.wall_simplification[1]:
                        self.wall_simplification[1] = z

        # generate bounding

        for x in range(self.wall_simplification[0], self.wall_simplification[2] + 1):
            zMin: int = self.wall_simplification[1] - 1
            zMax: int = self.wall_simplification[3] + 1

            # Up
            self.appendWallCell(x, zMin, self.MODEL_LINE, 0, 3)

            # Down
            self.appendWallCell(x, zMax, self.MODEL_LINE, 1, 3)

        for z in range(self.wall_simplification[1], self.wall_simplification[3] + 1):
            xMin: int = self.wall_simplification[0] - 1
            xMax: int = self.wall_simplification[2] + 1

            # Left
            self.appendWallCell(xMin, z, self.MODEL_LINE, 0, 0)

            # Right
            self.appendWallCell(xMax, z, self.MODEL_LINE, 1, 0)

        # Left Up Corner
        self.appendWallCell(self.wall_simplification[0] - 1, self.wall_simplification[1] - 1, self.MODEL_CORNER, 0, 0)

        # Right Up Corner
        self.appendWallCell(self.wall_simplification[2] + 1, self.wall_simplification[1] - 1, self.MODEL_CORNER, 0, 3)

        # Right Down Corner
        self.appendWallCell(self.wall_simplification[2] + 1, self.wall_simplification[3] + 1, self.MODEL_CORNER, 0, 2)

        # Left Down Corner
        self.appendWallCell(self.wall_simplification[0] - 1, self.wall_simplification[3] + 1, self.MODEL_CORNER, 0, 1)

    def computeConvexFull(self):
        # Compute Convex full bounding
        positions: list = []

        self.hull = []
        for x in range(self.detection_grid_size[0]):
            for z in range(self.detection_grid_size[1]):
                if self.connected_area[z * self.detection_grid_size[0] + x]:
                    positions.append([x - 1, z - 1])
                    positions.append([x + 1, z - 1])
                    positions.append([x + 1, z + 1])
                    positions.append([x - 1, z + 1])

        self.hull: list = pmath.convexHull(positions)

        pos_min = copy.copy(self.hull[0])
        pos_max = copy.copy(self.hull[0])

        for position in self.hull:
            for dim in [0, 1]:
                if pos_min[dim] > position[dim]:
                    pos_min[dim] = position[dim]

                if pos_max[dim] < position[dim]:
                    pos_max[dim] = position[dim]

        extended_size: list = [pos_max[0] - pos_min[0] + 1, pos_max[1] - pos_min[1] + 1]
        extended_offset: list = pos_min
        extended_matrix: list = [False] * (extended_size[0] * extended_size[1])
        diff: list
        distance: int
        subdivision: int

        to_visit: list = []

        self.matrix: list = [False] * (self.detection_grid_size[0] * self.detection_grid_size[1])

        # Mark
        for index in range(len(self.hull)):
            point1 = self.hull[index]
            point2 = self.hull[(index + 1) % len(self.hull)]

            diff = [point2[0] - point1[0] * 1.0, point2[1] - point1[1] * 1.0]

            distance = math.dist(point1, point2)
            subdivision = math.floor(distance) * 150

            for a in range(subdivision):
                position = [round(point1[0] + (diff[0] / subdivision * a)),
                            round(point1[1] + (diff[1] / subdivision * a))]

                extended_matrix[(position[1] - extended_offset[1]) * extended_size[0] + (position[0] - extended_offset[0])] = True

                if position not in to_visit:
                    to_visit.append(position)

        def getValue_extended(x_pos, z_pos) -> bool:
            if 0 > x_pos or x_pos >= extended_size[0] or 0 > z_pos or z_pos >= extended_size[1]:
                return False

            return extended_matrix[z_pos * extended_size[0] + x_pos]

        def isInStack(list, ref):
            for block in list:
                if pmath.is2DPointEqual(block, ref):
                    return True

            return False

        recursion_start: list
        remaining: list = []
        founded: list = []

        for x in range(extended_size[0]):
            if getValue_extended(x, 0):
                if not getValue_extended(x, 1):
                    remaining.append([x, 1])
                    break

        while len(remaining) != 0:
            x, z = remaining[0]
            founded.append([x, z])
            del remaining[0]

            if 0 <= x + extended_offset[0] <= self.detection_grid_size[0] and 0 <= z + extended_offset[1] <= \
                    self.detection_grid_size[1]:
                self.matrix[(z + extended_offset[1]) * self.detection_grid_size[0] + x + extended_offset[0]] = True

            for x_offset in range(-1, 2):
                for z_offset in range(-1, 2):
                    if getValue_extended(x + x_offset, z + z_offset):
                        continue

                    if isInStack(remaining, [x + x_offset, z + z_offset]):
                        continue

                    if isInStack(founded, [x + x_offset, z + z_offset]):
                        continue

                    remaining.append([x + x_offset, z + z_offset])

        # Fill self.matrix for is block in zone
        def getValue(x_pos, z_pos) -> bool:
            if 0 > x_pos or x_pos >= self.detection_grid_size[0] or 0 > z_pos or z_pos >= self.detection_grid_size[1]:
                return False

            return self.matrix[z_pos * self.detection_grid_size[0] + x_pos]

        info_ajustment: list = [
            [[-1, 1, -1,
              -1, -1, 2,
              -1, 1, -1], self.MODEL_LINE, 0, 0],  # Left 0
            [[-1, 1, -1,
              2, -1, -1,
              -1, 1, -1], self.MODEL_LINE, 1, 0],  # Right 1
            [[-1, -1, -1,
              1, -1, 1,
              -1, 2, -1], self.MODEL_LINE, 1, 1],  # Up 2
            [[-1, 2, -1,
              1, -1, 1,
              -1, -1, -1], self.MODEL_LINE, 0, 1],  # Down 3
            [[-1, -1, -1,
              -1, -1, 1,
              -1, 1, 2], self.MODEL_CORNER, 0, 0],  # Left Up corner 4
            [[-1, 1, -1,
              1, -1, 2,
              -1, 2, -1], self.MODEL_CORNER_INTERIOR, 0, 0],  # Left Up interior corner 5
            [[-1, -1, -1,
              1, -1, -1,
              2, 1, -1], self.MODEL_CORNER, 0, 3],  # Right Up corner 6
            [[-1, 1, -1,
              2, -1, 1,
              -1, 2, -1], self.MODEL_CORNER_INTERIOR, 0, 3],  # Right Up interior corner 7
            [[2, 1, -1,
              1, -1, -1,
              -1, -1, -1], self.MODEL_CORNER, 0, 2],  # Right Down corner 8
            [[-1, 2, -1,
              2, -1, 1,
              -1, 1, -1], self.MODEL_CORNER_INTERIOR, 0, 2],  # Right Down interior corner 9
            [[-1, 1, 2,
              -1, -1, 1,
              -1, -1, -1], self.MODEL_CORNER, 0, 1],  # Left Down corner 10
            [[-1, 2, -1,
              1, -1, 2,
              -1, 1, -1], self.MODEL_CORNER_INTERIOR, 0, 1]  # Left Down interior corner 11
        ]

        def doesTheMatrixIsRecognize(cell, info):
            for z_matrix in [0, 1, 2]:
                for x_matrix in [0, 1, 2]:
                    if z_matrix == 1 and x_matrix == 1:
                        continue

                    # Check if barrier
                    if info[0][z_matrix * 3 + x_matrix] == 1:
                        if not getValue_extended(
                                cell[0] - extended_offset[0] + x_matrix - 1,
                                cell[1] - extended_offset[1] + z_matrix - 1):
                            return False
                    # Check if interior
                    elif info[0][z_matrix * 3 + x_matrix] == 2:
                        if not getValue(
                                cell[0] + x_matrix - 1,
                                cell[1]+ z_matrix - 1):
                            return False

            return True

        for cell in to_visit:
            i: int = 0
            while i < len(info_ajustment):
                info: list = info_ajustment[i]

                if doesTheMatrixIsRecognize(cell, info):
                    print(cell[0], cell[1], i)
                    self.appendWallCell(cell[0], cell[1], info[1], info[2], info[3])
                    i = len(info_ajustment)
                else:
                    i += 1

    def placeWall(self, world_modification):
        x: int
        z: int
        model: list = []

        y = 64

        for wallCell in self.wall_list:
            x, z = wallCell["position"]
            x_real: int = x * self.zone_size + self.area[0]
            z_real: int = z * self.zone_size + self.area[2]

            if not (self.area[0] <= x_real and x_real + self.zone_size <= self.area[3]
                    and self.area[2] <= z_real and z_real + self.zone_size <= self.area[5]):
                continue

            if wallCell["type"] == self.MODEL_LINE:
                model = self.modelWallLine()
            elif wallCell["type"] == self.MODEL_CORNER:
                model = self.modelWallCorner()
            elif wallCell["type"] == self.MODEL_CORNER_INTERIOR:
                model = self.modelWallCornerInterior()

            model = self.applyOnModel(model, wallCell["flip"], wallCell["rotation"])

            for xr in range(self.zone_size):
                for zr in range(self.zone_size):
                    """while (not Constants.is_air(x_real + xr, y + 1, z_real + zr) or Constants.is_air(x_real + xr, y,
                                                                                                     z_real + zr)) and 0 <= y <= 255:
                        if Constants.is_air(x_real + xr, y, z_real + zr):
                            y -= 1
                        if not Constants.is_air(x_real + xr, y + 1, z_real + zr):
                            y += 1"""

                    for y_offset in range(len(model[zr][xr])):
                        if 0 <= y + y_offset <= 255:
                            world_modification.setBlock(x_real + xr, y + y_offset, z_real + zr, model[zr][xr][y_offset])

    def applyOnModel(self, model, flip, rotation):
        if flip == 0 and rotation == 0:
            return model

        newModel = []

        if flip == 1:
            for z in range(self.zone_size):
                newModel.append([])
                for x in range(self.zone_size):
                    newModel[z].append(model[z][self.zone_size - x - 1])

        else:
            newModel = model

        while rotation > 0:
            newModel = pmath.rotateSquaredMatrix(newModel)
            rotation -= 1

        return newModel

    def modelWallLine(self):
        result: list = []

        for z in range(self.zone_size):
            result.append([])
            for x in range(self.zone_size):

                result[z].append([])

                if self.village.status == "war":
                    if 0 == x:
                        for a in range(self.village.tier + 2):
                            result[z][x].append("minecraft:oak_planks")
                else:
                    if 0 == x:
                        result[z][x].append("minecraft:oak_fence")

        return result

    def modelWallCorner(self):
        result: list = []

        for z in range(self.zone_size):
            result.append([])
            for x in range(self.zone_size):

                result[z].append([])

                if self.village.status == "war":
                    if x == 0 or z == 0:
                        for a in range(self.village.tier + 2):
                            result[z][x].append("minecraft:oak_planks")
                else:
                    if x == 0 or z == 0:
                        result[z][x].append("minecraft:oak_fence")

        return result

    def modelWallCornerInterior(self):
        result: list = []

        for z in range(self.zone_size):
            result.append([])
            for x in range(self.zone_size):

                result[z].append([])

                if self.village.status == "war":
                    if x == 0 and z == 0:
                        for a in range(self.village.tier + 2):
                            result[z][x].append("minecraft:oak_planks")
                else:
                    if x == 0 and z == 0:
                        result[z][x].append("minecraft:oak_fence")

        return result

    def appendWallCell(self, x: int, z: int, wallType: int, flip: int, rotation: int) -> None:
        for wall in self.wall_list:
            if pmath.is2DPointEqual([x, z], wall["position"]):
                wall["type"] = wallType
                wall["flip"] = flip
                wall["rotation"] = rotation

                return

        self.wall_list.append({
            "position": [x, z],
            "type": wallType,
            "flip": flip,
            "rotation": rotation
        })

    def isBlockInEnclosure(self, x, z) -> bool:
        if self.bounding_type == self.BOUNDING_RECTANGULAR:
            return self.area[0] + self.wall_simplification[0] * self.zone_size <= x <= self.area[0] + \
                   self.wall_simplification[2] * self.zone_size and \
                   self.area[2] + self.wall_simplification[1] * self.zone_size <= z <= self.area[2] + \
                   self.wall_simplification[3] * self.zone_size

        if self.bounding_type == self.BOUNDING_CONVEX_HULL:
            pos_x: int = x - self.area[0] // self.zone_size
            pos_z: int = z - self.area[2] // self.zone_size

            if x < 0 or x >= self.detection_grid_size[0] or z < 0 or z >= self.detection_grid_size[1]:
                return False

            return self.matrix[pos_z * self.detection_grid_size[0] + pos_x]

        return False

    def showImageRepresenting(self):
        img = Image.new("RGB", (self.detection_grid_size[0], self.detection_grid_size[1]))

        pixels: list = img.load()

        counter = 0
        for y in range(self.detection_grid_size[1]):
            for x in range(self.detection_grid_size[0]):
                if self.connected_area[counter]:
                    pixels[x, y] = (255, 0, 0)

                if self.bounding_type == self.BOUNDING_CONVEX_HULL:
                    if self.matrix[counter]:
                        pixels[x, y] = (pixels[x, y][0] // 2, 0, 255)

                counter += 1
        plt.imshow(img)

        if self.bounding_type == self.BOUNDING_RECTANGULAR:
            plt.plot([self.wall_simplification[0], self.wall_simplification[2], self.wall_simplification[2],
                      self.wall_simplification[0], self.wall_simplification[0]],
                     [self.wall_simplification[1], self.wall_simplification[1], self.wall_simplification[3],
                      self.wall_simplification[3], self.wall_simplification[1]],
                     color="blue")

        elif self.bounding_type == self.BOUNDING_CONVEX_HULL:
            for i in range(len(self.hull)):
                plt.plot([self.hull[i][0], self.hull[(i + 1) % len(self.hull)][0]],
                         [self.hull[i][1], self.hull[(i + 1) % len(self.hull)][1]], color="gray")

        plt.show()
        plt.close()
