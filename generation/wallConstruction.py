from PIL import Image
import matplotlib.pyplot as plt

import utils.projectMath as pmath


class WallConstruction:
    def __init__(self, zone_size=16):
        self.zone_size: int = zone_size
        self.detection_grid_size: list = [0, 0]
        self.area: tuple = ()
        self.connected_area: list = []

    def setConstructionZone(self, area):
        self.detection_grid_size = [0, 0]
        self.area = area

        for i in [0, 1]:
            if area[i * 2] % self.zone_size != 0:
                self.detection_grid_size[i] += 1

            size: int = area[(i * 2) + 3] - area[i * 2]

            while size > 0:
                self.detection_grid_size[i] += 1
                size -= self.zone_size

        self.connected_area = [False] * (self.detection_grid_size[0] * self.detection_grid_size[1])

    def returnPositionPoint(self, point):
        grid_position: list = [0, 0]
        positions: float
        rest: float

        for i in [0, 1]:
            positions = point[i] - self.area[i * 2]
            rest = self.area[i * 2] % self.zone_size

            grid_position[i] = (positions - rest) // self.zone_size

            if rest < positions:
                grid_position[i] += 1

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
                    self.connected_area[x * self.detection_grid_size[0] + y] = True

    def addPoints(self, point):
        grid_position: list = [-1, -1]
        if len(point) == 3:
            grid_position = self.returnPositionPoint([point[0], point[2]])
        elif len(point) == 2:
            grid_position = self.returnPositionPoint(point)

        if 0 <= grid_position[0] < self.detection_grid_size[0] \
                and 0 <= grid_position[1] < self.detection_grid_size[1]:
            self.connected_area[grid_position[1] * self.detection_grid_size[0] + grid_position[0]] = True

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
        plt.show()
        plt.close()
