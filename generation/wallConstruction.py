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

    def addPoints(self, point):
        if not pmath.isPointInCube(point, self.area):
            return

        grid_position: list = [0, 0]
        positions: list = [0, 0]
        rest: list = [0, 0]

        for i in [0, 1]:
            positions[i] = self.area[i * 2 + 3] - point[i * 2]
            rest[i] = point[i * 2] % self.zone_size

            if rest[i] > positions[i]:
                grid_position[i] = 0
            else:
                grid_position[i] = (positions[i] - rest[i]) // self.zone_size

            print(rest[i], positions[i], grid_position[i])

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
