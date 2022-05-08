from PIL import Image
from utils.constants import Constants

import matplotlib.pyplot as plt
import utils.projectMath as pmath


class WallConstruction:
    BOUNDING_RECTANGULAR: int = 0
    BOUNDING_CONVEX_HULL: int = 1

    MODEL_LINE: int = 0
    MODEL_CORNER: int = 1

    def __init__(self, village, zone_size=16):
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

            self.wall_list.append(self.createWallCell(x, zMin, self.MODEL_LINE, 0, 3))
            self.wall_list.append(self.createWallCell(x, zMax, self.MODEL_LINE, 1, 3))

        for z in range(self.wall_simplification[1], self.wall_simplification[3] + 1):
            xMin: int = self.wall_simplification[0] - 1
            xMax: int = self.wall_simplification[2] + 1

            self.wall_list.append(self.createWallCell(xMin, z, self.MODEL_LINE, 0, 0))
            self.wall_list.append(self.createWallCell(xMax, z, self.MODEL_LINE, 1, 0))

        self.wall_list.append(
            self.createWallCell(self.wall_simplification[0] - 1, self.wall_simplification[1] - 1, self.MODEL_CORNER, 0,
                                0))
        self.wall_list.append(
            self.createWallCell(self.wall_simplification[2] + 1, self.wall_simplification[1] - 1, self.MODEL_CORNER, 0,
                                3))
        self.wall_list.append(
            self.createWallCell(self.wall_simplification[2] + 1, self.wall_simplification[3] + 1, self.MODEL_CORNER, 0,
                                2))
        self.wall_list.append(
            self.createWallCell(self.wall_simplification[0] - 1, self.wall_simplification[3] + 1, self.MODEL_CORNER, 0,
                                1))

    def computeConvexFull(self):
        positions: list = []

        lower_left_most_positions = -1

        self.hull = []
        for x in range(self.detection_grid_size[0]):
            for y in range(self.detection_grid_size[1]):
                if self.connected_area[y * self.detection_grid_size[0] + x]:
                    if lower_left_most_positions == -1:
                        lower_left_most_positions = len(positions)

                    positions.append([x, y])

        self.hull = pmath.convexHull(positions)

    def placeWall(self, world_modification):
        x: int
        z: int
        model: list = []

        y = 64

        for wallCell in self.wall_list:
            x, z = wallCell["position"]
            x_real: int = x * self.zone_size + self.area[0]
            z_real: int = z * self.zone_size + self.area[2]

            print(self.area, x_real, z_real)
            if not (self.area[0] <= x_real and x_real + self.zone_size <= self.area[3]
                    and self.area[2] <= z_real and z_real + self.zone_size <= self.area[5]):
                continue

            if wallCell["type"] == self.MODEL_LINE:
                model = self.modelWallLine()
            elif wallCell["type"] == self.MODEL_CORNER:
                model = self.modelWallCorner()

            model = self.applyOnModel(model, wallCell["flip"], wallCell["rotation"])

            for xr in range(self.zone_size):
                for zr in range(self.zone_size):
                    while (not Constants.is_air(x_real + xr, y + 1, z_real + zr) or Constants.is_air(x_real + xr, y,
                                                                                                     z_real + zr)) and 0 <= y <= 255:
                        if Constants.is_air(x_real + xr, y, z_real + zr):
                            y -= 1
                        if not Constants.is_air(x_real + xr, y + 1, z_real + zr):
                            y += 1

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
                    if x == 0:
                        for a in range(self.village.tier + 2):
                            result[z][x].append("minecraft:oak_planks")
                else:
                    if x == 0:
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

    @staticmethod
    def createWallCell(x: int, z: int, wallType: int, flip: int, rotation: int) -> dict:
        return {
            "position": [x, z],
            "type": wallType,
            "flip": flip,
            "rotation": rotation
        }

    def isBlockInEnclosure(self, x, z) -> bool:
        if self.bounding_type == self.BOUNDING_RECTANGULAR:
            return self.area[0] + self.wall_simplification[0] * self.zone_size <= x <= self.area[0] + \
                   self.wall_simplification[2] * self.zone_size and \
                   self.area[2] + self.wall_simplification[1] * self.zone_size <= z <= self.area[2] + \
                   self.wall_simplification[3] * self.zone_size

        return True

    def showImageRepresenting(self):
        img = Image.new("RGB", (self.detection_grid_size[0], self.detection_grid_size[1]))

        pixels = img.load()

        counter = 0
        for y in range(self.detection_grid_size[1]):
            for x in range(self.detection_grid_size[0]):
                if self.connected_area[counter]:
                    pixels[x, y] = (255, 0, 0)

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
                         [self.hull[i][1], self.hull[(i + 1) % len(self.hull)][1]], color="blue")

        plt.show()
        plt.close()
