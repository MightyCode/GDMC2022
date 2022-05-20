import random

from generation.data.loreStructure import LoreStructure
from generation.data.settlementData import SettlementData
from generation.resources import Resources
from utils import util
from utils.constants import Constants
import generation.generator as generator

import copy
import math

from PIL import Image

import matplotlib.pyplot as plt
import utils.projectMath as pmath
from utils.worldModification import WorldModification

class WallPart:
    def __init__(self):
        self.position: list = [0, 0]
        self.wall_type: int = 0
        self.flip: int = 0
        self.rotation: int = 0

        self.height: int = 0
        self.augmented_height: int = 0

        self.sided_wall_1 = None
        self.sided_wall_2 = None

    def setInfo(self, x: int, z: int, wallType: int, flip: int, rotation: int):
        self.position = [x, z]
        self.wall_type = wallType
        self.flip = flip
        self.rotation = rotation

class WallConstruction:
    BOUNDING_RECTANGULAR: int = 0
    BOUNDING_CONVEX_HULL: int = 1

    MODEL_LINE: int = 0
    MODEL_CORNER: int = 1
    MODEL_CORNER_INTERIOR: int = 2
    MODEL_DOOR = 3
    MODEL_STAIRS = 4

    WALL_PARTS = ["line", "externcorner", "innercorner", "door", "stairs"]

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
        print("Extended size", extended_size, "Extended offset", extended_offset)

        extended_matrix: list = [False] * (extended_size[0] * extended_size[1])
        diff: list
        distance: int
        subdivision: int

        to_visit: list = []

        def add_border_cell(x_real, z_real):
            if x_real < 0 or x_real >= self.detection_grid_size[0] or z_real < 0 or z_real >= self.detection_grid_size[1]:
                return

            if z_real - extended_offset[1] < 0 or z_real - extended_offset[1] >= extended_size[1] or \
                    x_real - extended_offset[0] < 0 or x_real - extended_offset[0] >= extended_size[0]:
                return

            extended_matrix[(z_real - extended_offset[1]) * extended_size[0] + (x_real - extended_offset[0])] = True

            if [x_real, z_real] not in to_visit:
                to_visit.append([x_real, z_real])

        self.matrix: list = [False] * (self.detection_grid_size[0] * self.detection_grid_size[1])

        # Mark border on an extended matrix
        for index in range(len(self.hull)):
            point1 = self.hull[index]
            point2 = self.hull[(index + 1) % len(self.hull)]

            diff = [point2[0] - point1[0] * 1.0, point2[1] - point1[1] * 1.0]

            distance = math.dist(point1, point2)
            subdivision = math.floor(distance) * 40

            for a in range(subdivision):
                position = [round(point1[0] + (diff[0] / subdivision * a)),
                            round(point1[1] + (diff[1] / subdivision * a))]

                add_border_cell(position[0], position[1])

        def getValue_extended(x_pos, z_pos) -> bool:
            if 0 > x_pos or x_pos >= extended_size[0] or 0 > z_pos or z_pos >= extended_size[1]:
                return False

            return extended_matrix[z_pos * extended_size[0] + x_pos]

        def getValue(x_pos, z_pos) -> bool:
            if 0 > x_pos or x_pos >= self.detection_grid_size[0] or 0 > z_pos or z_pos >= self.detection_grid_size[1]:
                return False

            return self.matrix[z_pos * self.detection_grid_size[0] + x_pos]

        remaining: list = []
        founded: list = []

        # Detect where start recursion to compute inner wall zon
        for x in range(1, extended_size[0] - 1):
            if getValue_extended(x, 0):
                if not getValue_extended(x, 1):
                    remaining.append([x, 1])
                    break

        # Make the recursion
        while len(remaining) != 0:
            x, z = remaining[0]
            founded.append([x, z])
            del remaining[0]

            if 0 <= x + extended_offset[0] < self.detection_grid_size[0] and 0 <= z + extended_offset[1] < self.detection_grid_size[1]:
                self.matrix[(z + extended_offset[1]) * self.detection_grid_size[0] + (x + extended_offset[0])] = True

            for x_offset, z_offset in [[-1, 0], [1, 0], [0, -1], [0, 1]]:
                if getValue_extended(x + x_offset, z + z_offset):
                    continue

                if [x + x_offset, z + z_offset] in remaining:
                    continue

                if [x + x_offset, z + z_offset] in founded:
                    continue

                remaining.append([x + x_offset, z + z_offset])

        # Complete diagonal border
        for z in range(self.detection_grid_size[1]):
            for x in range(self.detection_grid_size[0]):
                if not getValue(x, z):
                    continue

                if getValue_extended(x - extended_offset[0], z - extended_offset[1] - 1):
                    if getValue_extended(x - extended_offset[0] - 1, z - extended_offset[1]):
                        add_border_cell(x - 1, z - 1)

                    if getValue_extended(x - extended_offset[0] + 1, z - extended_offset[1]):
                        add_border_cell(x + 1, z - 1)

                if getValue_extended(x - extended_offset[0], z - extended_offset[1] + 1):
                    if getValue_extended(x - extended_offset[0] - 1, z - extended_offset[1]):
                        add_border_cell(x - 1, z + 1)

                    if getValue_extended(x - extended_offset[0] + 1, z - extended_offset[1]):
                        add_border_cell(x + 1, z + 1)

        # Display status of border
        for y in range(extended_size[1]):
            print("")
            for x in range(extended_size[0]):
                print("1" if getValue_extended(x, y) else "2" if getValue(x + extended_offset[0],
                                                                          y + extended_offset[1]) else "0", end="")

        info_adjustment: list = [
            [[-1, 1, -1,
              -1, -1, 2,
              -1, 1, -1], self.MODEL_LINE, 2, 3],  # Left 0
            [[-1, 1, -1,
              2, -1, -1,
              -1, 1, -1], self.MODEL_LINE, 2, 1],  # Right 1
            [[-1, -1, -1,
              1, -1, 1,
              -1, 2, -1], self.MODEL_LINE, 2, 0],  # Up 2
            [[-1, 2, -1,
              1, -1, 1,
              -1, -1, -1], self.MODEL_LINE, 2, 2],  # Down 3
            [[-1, -1, -1,
              -1, -1, 1,
              -1, 1, 2], self.MODEL_CORNER, 0, 2],  # Left Up corner 4
            [[-1, 1, -1,
              1, -1, 2,
              -1, 2, -1], self.MODEL_CORNER_INTERIOR, 3, 0],  # Left Up interior corner 5
            [[-1, -1, -1,
              1, -1, -1,
              2, 1, -1], self.MODEL_CORNER, 0, 3],  # Right Up corner 6
            [[-1, 1, -1,
              2, -1, 1,
              -1, 2, -1], self.MODEL_CORNER_INTERIOR, 3, 1],  # Right Up interior corner 7
            [[2, 1, -1,
              1, -1, -1,
              -1, -1, -1], self.MODEL_CORNER, 0, 0],  # Right Down corner 8
            [[-1, 2, -1,
              2, -1, 1,
              -1, 1, -1], self.MODEL_CORNER_INTERIOR, 3, 2],  # Right Down interior corner 9
            [[-1, 1, 2,
              -1, -1, 1,
              -1, -1, -1], self.MODEL_CORNER, 0, 1],  # Left Down corner 10
            [[-1, 2, -1,
              1, -1, 2,
              -1, 1, -1], self.MODEL_CORNER_INTERIOR, 3, 3]  # Left Down interior corner 11
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
                                cell[1] + z_matrix - 1):
                            return False

            return True

        for cell in to_visit:
            i: int = 0
            while i < len(info_adjustment):
                info: list = info_adjustment[i]

                if doesTheMatrixIsRecognize(cell, info):
                    self.appendWallCell(cell[0], cell[1], info[1], info[2], info[3])
                    i = len(info_adjustment)
                else:
                    i += 1

    def computeWallHeight(self):
        # Connect wall cell
        wall = self.wall_list[0]
        while wall != None:
            next = None
            for wall_sub in self.wall_list:
                if wall_sub == wall:
                    continue

                if (wall.position[0] - 1 == wall_sub.position[0] and wall.position[1] == wall_sub.position[1]) \
                        or (wall.position[0] + 1 == wall_sub.position[0] and wall.position[1] == wall_sub.position[1]) \
                        or (wall.position[0] == wall_sub.position[0] and wall.position[1] - 1 == wall_sub.position[1]) \
                        or (wall.position[0] == wall_sub.position[0] and wall.position[1] + 1 == wall_sub.position[1]):

                    if wall.sided_wall_1 == None and wall_sub != wall.sided_wall_2:
                        wall.sided_wall_1 = wall_sub
                        wall_sub.sided_wall_2 = wall
                        next = wall_sub
                    elif wall.sided_wall_2 == None and wall_sub != wall.sided_wall_1:
                        wall.sided_wall_2 = wall_sub
                        wall_sub.sided_wall_1 = wall

            wall = next

        local_maximum: list = []

        # Compute height for
        for wallCell in self.wall_list:
            x, z = wallCell.position
            # Centered on zone
            x_real: int = x * self.zone_size + self.area[0] + self.zone_size // 2 + 1
            z_real: int = z * self.zone_size + self.area[2] + self.zone_size // 2 + 1

            if not (self.area[0] <= x_real and x_real + self.zone_size <= self.area[3]
                    and self.area[2] <= z_real and z_real + self.zone_size <= self.area[5]):
                continue

            wallCell.height = util.getHighestNonAirBlock(x_real, z_real, x_real - self.area[0], z_real - self.area[2])
            wallCell.augmented_height = wallCell.height

        for wallCell in self.wall_list:
            if (
                    wallCell.sided_wall_1.height < wallCell.height - 1 and wallCell.sided_wall_1.height - 1 <= wallCell.height) \
                    or (
                    wallCell.sided_wall_2.height < wallCell.height - 1 and wallCell.sided_wall_2.height - 1 <= wallCell.height):
                local_maximum.append(wallCell)

        for wall in local_maximum:

            old = wall
            side_1 = wall.sided_wall_1
            while side_1 not in local_maximum:
                if side_1.augmented_height < old.augmented_height - 3:
                    if side_1.wall_type == WallConstruction.MODEL_LINE:
                        side_1.augmented_height = old.augmented_height - 3
                        side_1.wall_type = WallConstruction.MODEL_STAIRS
                    else:
                        side_1.augmented_height = old.augmented_height

                    old = side_1
                    side_1 = old.sided_wall_1
                else:
                    break

            old = wall
            side_2 = wall.sided_wall_2
            while side_2 not in local_maximum:
                if side_2.augmented_height < old.augmented_height - 3:
                    if side_1.wall_type == WallConstruction.MODEL_LINE:
                        side_2.augmented_height = old.augmented_height - 3
                        side_2.wall_type = WallConstruction.MODEL_STAIRS
                    else:
                        side_2.augmented_height = old.augmented_height

                    old = side_2
                    side_2 = old.sided_wall_2
                else:
                    break

    def placeAirZone(self, settlement_data: SettlementData, resources: Resources, world_modification: WorldModification):


    def placeWall(self, settlement_data: SettlementData, resources: Resources,
                  world_modification: WorldModification, block_transformations: list):
        # Choose door
        door_candidate: list = []
        for wallCell in self.wall_list:
            if wallCell.wall_type == self.MODEL_LINE:
                door_candidate.append(wallCell)

        for i in range(random.randint(1, 3)):
            index: int = random.randint(0, len(door_candidate) - 1)
            door_candidate[index].wall_type = self.MODEL_DOOR
            del door_candidate[index]

        x: int
        z: int

        for wallCell in self.wall_list:
            x, z = wallCell.position
            # Centered on zone
            x_real: int = x * self.zone_size + self.area[0] + self.zone_size // 2 + 1
            z_real: int = z * self.zone_size + self.area[2] + self.zone_size // 2 + 1

            if not (self.area[0] <= x_real and x_real + self.zone_size <= self.area[3]
                    and self.area[2] <= z_real and z_real + self.zone_size <= self.area[5]):
                continue

            y = wallCell.augmented_height

            tier: str = "basic" if self.village.tier == 0 else "medium" if self.village.tier == 1 else "advanced"

            lore_structure: LoreStructure = LoreStructure()
            lore_structure.name = tier + "wall" + self.WALL_PARTS[wallCell.wall_type]
            lore_structure.position = [x_real, y - 1, z_real]
            lore_structure.flip = wallCell.flip
            lore_structure.rotation = wallCell.rotation
            lore_structure.age = settlement_data.village_model.age

            if settlement_data.village_model.isDestroyed:
                lore_structure.destroyed = True
                for one_cause in util.selectNWithChanceForOther(["burned", "damaged", "abandoned"], [0.4, 0.3, 0.3], 1):
                    lore_structure.causeDestroy[one_cause] = settlement_data.village_model.destroyCause

            lore_structure.preBuildingInfo = resources.structures[lore_structure.name].getNextBuildingInformation(
                lore_structure.flip, lore_structure.rotation
            )

            generator.generateStructure(lore_structure, settlement_data, resources, world_modification, None,
                                        block_transformations)

    def returnWallEntries(self) -> list:
        result: list = []

        for wallCell in self.wall_list:
            if wallCell.wall_type != self.MODEL_DOOR:
                continue

            half: int = self.zone_size // 2 + 1

            position: list = [
                self.area[0] + wallCell.position[0] * self.zone_size + half,
                self.area[2] + wallCell.position[1] * self.zone_size + half
            ]

            if wallCell.rotation == 0:
                position[1] += half
            elif wallCell.rotation == 1:
                position[0] -= half
            elif wallCell.rotation == 2:
                position[1] -= half
            elif wallCell.rotation == 3:
                position[0] += half

            result.append([position[0], wallCell.height, position[1]])

        return result

    def appendWallCell(self, x: int, z: int, wallType: int, flip: int, rotation: int) -> None:
        for wall in self.wall_list:
            if pmath.is2DPointEqual([x, z], wall.position):
                wall.type = wallType
                wall.flip = flip
                wall.rotation = rotation

                return

        current: WallPart = WallPart()
        current.setInfo(x, z, wallType, flip, rotation)

        self.wall_list.append(current)

    def isBlockInEnclosure(self, x, z) -> bool:
        if self.bounding_type == self.BOUNDING_RECTANGULAR:
            return self.area[0] + self.wall_simplification[0] * self.zone_size <= x <= self.area[0] + \
                   self.wall_simplification[2] * self.zone_size and \
                   self.area[2] + self.wall_simplification[1] * self.zone_size <= z <= self.area[2] + \
                   self.wall_simplification[3] * self.zone_size

        if self.bounding_type == self.BOUNDING_CONVEX_HULL:
            pos_x: int = (x - self.area[0]) // self.zone_size
            pos_z: int = (z - self.area[2]) // self.zone_size

            if pos_x < 0 or pos_x >= self.detection_grid_size[0] or pos_z < 0 or pos_z >= self.detection_grid_size[1]:
                #print("Out side", pos_x, pos_z)
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
