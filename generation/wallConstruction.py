from PIL import Image
import matplotlib.pyplot as plt
from utils.constants import Constants


class WallConstruction:
    def __init__(self, zone_size=16):
        self.zone_size: int = zone_size
        self.detection_grid_size: list = [0, 0]
        self.area: tuple = ()
        self.connected_area: list = []
        self.wall_simplification = [-1, -1, -1, -1]
        self.wall_zone = []

    def setConstructionZone(self, area):
        self.detection_grid_size = [0, 0]
        self.area = area

        for i in [0, 1]:
            size: int = area[(i * 2) + 3] - area[i * 2]

            while size > 0:
                self.detection_grid_size[i] += 1
                size -= self.zone_size

        self.connected_area = [False] * (self.detection_grid_size[0] * self.detection_grid_size[1])
        self.wall_zone = [""] * len(self.connected_area)

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
            for y in range(connected_rectangle[1], connected_rectangle[3] + 1):
                if 0 <= x < self.detection_grid_size[0] \
                        and 0 <= y < self.detection_grid_size[1]:
                    self.connected_area[y * self.detection_grid_size[0] + x] = True

    def addPoints(self, point):
        grid_position: list = [-1, -1]
        if len(point) == 3:
            grid_position = self.returnPositionPoint([point[0], point[2]])
        elif len(point) == 2:
            grid_position = self.returnPositionPoint(point)

        if 0 <= grid_position[0] < self.detection_grid_size[0] \
                and 0 <= grid_position[1] < self.detection_grid_size[1]:
            self.connected_area[grid_position[1] * self.detection_grid_size[0] + grid_position[0]] = True

    def computeWall(self):
        self.wall_simplification = [self.detection_grid_size[0], self.detection_grid_size[1], -1, -1]

        for y in range(self.detection_grid_size[1]):
            for x in range(self.detection_grid_size[0]):
                if self.connected_area[y * self.detection_grid_size[0] + x]:
                    if x > self.wall_simplification[2]:
                        self.wall_simplification[2] = x
                    if x < self.wall_simplification[0]:
                        self.wall_simplification[0] = x

                    if y > self.wall_simplification[3]:
                        self.wall_simplification[3] = y
                    if y < self.wall_simplification[1]:
                        self.wall_simplification[1] = y

        # generate
        for x in range(self.wall_simplification[0], self.wall_simplification[2] + 1):
            yMin: int = self.wall_simplification[1] - 1
            yMax: int = self.wall_simplification[3] + 1

            self.wall_zone[yMin * self.detection_grid_size[0] + x] = "up"
            self.wall_zone[yMax * self.detection_grid_size[0] + x] = "down"

        for y in range(self.wall_simplification[1], self.wall_simplification[3] + 1):
            xMin: int = self.wall_simplification[0] - 1
            xMax: int = self.wall_simplification[2] + 1

            self.wall_zone[y * self.detection_grid_size[0] + xMin] = "left"
            self.wall_zone[y * self.detection_grid_size[0] + xMax] = "right"

    def placeWall(self, world_modification):
        for z in range(self.detection_grid_size[1]):
            for x in range(self.detection_grid_size[0]):
                position: str = self.wall_zone[z * self.detection_grid_size[0] + x]
                if position == "":
                    continue

                flip = 0
                rotation = 0

                # Composed position
                if position == "right":
                    flip = 1
                elif position == "up":
                    rotation = 1
                elif position == "down":
                    flip = 1
                    rotation = 1

                self.placeModel(world_modification, x, z, self.applyOnModel(self.modelWallLine(), flip, rotation),)

    def placeModel(self, world_modification, x_zone, z_zone, model):
        x_real: int = x_zone * self.zone_size + self.area[0]
        z_real: int = z_zone * self.zone_size + self.area[2]

        y = 200

        for xr in range(self.zone_size):
            for zr in range(self.zone_size):

                while not Constants.is_air(x_real + xr, y + 1, z_real + zr) or Constants.is_air(x_real + xr, y, z_real + zr) and 0 <= y <= 255:
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

        newModel2 = []

        if rotation == 1:
            for x in range(self.zone_size):
                newModel2.append([])

                for z in range(self.zone_size):
                    newModel2[x].append(newModel[z][x])

        else:
            newModel2 = newModel

        return newModel2

    def modelWallLine(self):
        result: list = []

        for z in range(self.zone_size):
            result.append([])
            for x in range(self.zone_size):

                result[z].append([])

                if x == (self.zone_size - 1):
                    result[z][x].append("minecraft:oak_fence")

        return result

    def isBlockInEnclosure(self, x, z):
        return self.wall_simplification[0] <= x <= self.wall_simplification[2] and self.wall_simplification[1] <= z <= \
               self.wall_simplification[3]

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
        plt.plot([self.wall_simplification[0], self.wall_simplification[2], self.wall_simplification[2],
                  self.wall_simplification[0], self.wall_simplification[0]],
                 [self.wall_simplification[1], self.wall_simplification[1], self.wall_simplification[3],
                  self.wall_simplification[3], self.wall_simplification[1]],
                 color="blue")

        plt.show()
        plt.close()
