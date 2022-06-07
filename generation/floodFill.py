from utils.constants import Constants
from generation.data.settlementData import SettlementData
import lib.interfaceUtils as Iu
import utils.projectMath as projectMath

import random


class FloodFill:
    def __init__(self, world_modification, settlement_data):
        self.numberOfDecoration = 0
        self.world_modification = world_modification
        self.set_number_of_houses(settlement_data.structure_number_goal)
        self.structures = []
        # random.seed(None, 2)
        self.startPosRange = [0.73, 0.73]

        self.distanceFirstHouse = 40
        self.distanceFirstHouseIncrease = 3

        self.buildArea = settlement_data.area
        self.size = settlement_data.size
        coef: int = 6
        self.validHouseFloodFillPosition = [self.buildArea[0] + self.size[0] / coef,
                                            self.buildArea[2] + self.size[1] / coef,
                                            self.buildArea[3] - self.size[0] / coef,
                                            self.buildArea[5] - self.size[1] / coef]
        self.minDistanceHouse = 4
        self.floodfillHouseSpace = random.randint(4, 7)

        self.previous_structure = -1

    def set_number_of_houses(self, number_house: int):
        self.numberOfDecoration: int = int(number_house * 1.5)  # 150

    def is_ground(self, x: int, y: int, z: int):
        y1: int = y + 1
        y2: int = y - 1

        # print(is_air(x,y2+1,z,ws) and not(is_air(x,y2,z,ws)))
        """ and not(ws.getBlockAt(x, y2, z)=='minecraft:water') """
        if Iu.getBlock(x, y, z) == 'minecraft:lava':
            self.world_modification.setBlock(x, y, z, 'minecraft:obsidian')
        if Iu.getBlock(x, y1, z) == 'minecraft:lava':
            self.world_modification.setBlock(x, y1, z, 'minecraft:obsidian')
        if Iu.getBlock(x, y2, z) == 'minecraft:lava':
            self.world_modification.setBlock(x, y2, z, 'minecraft:obsidian')

        if Constants.is_air(x, y2 + 1, z) and not (Constants.is_air(x, y2, z)):
            return y2
        elif Constants.is_air(x, y1 + 1, z) and not (Constants.is_air(x, y1, z)):
            return y1
        elif Constants.is_air(x, y + 1, z) and not (Constants.is_air(x, y, z)):
            return y
        else:
            return -1

    def computeCenter(self) -> list:
        mean: list = [0, 0, 0]

        for structure in self.structures:
            mean[0] += structure[0]
            mean[1] += structure[1]
            mean[2] += structure[2]

        mean[0] /= len(self.structures)
        mean[1] /= len(self.structures)
        mean[2] /= len(self.structures)

        return mean

    def floodfill(self, xi, yi, zi, size):
        valid_positions = []
        # if floodfill start is in building area
        if not projectMath.isPointInCube([xi, yi, zi], self.buildArea):
            print("Out of build area i ", xi, yi, zi)
            return valid_positions

        stack = [(xi, yi, zi)]

        to_add = [[1, 0], [0, 1], [-1, 0], [0, -1]]
        flood_fill_area = [xi - size, 0, zi - size, xi + size, 255, zi + size]

        while stack:
            node = stack.pop()
            valid_positions.append(node)
            # iu.setBlock(Node[0],Node[1]-1,Node[2],"minecraft:bricks")
            for add in to_add:
                x = node[0] + add[0]
                z = node[2] + add[1]
                y = node[1]
                if projectMath.isPointInCube([x, y, z], self.buildArea):
                    ground_height: int = -1

                    try:
                        ground_height = self.is_ground(x, y, z)
                    except IndexError:
                        pass
                        # print("index error")
                        # print(x,y,z)

                    if ground_height != -1 \
                            and (x, ground_height, z) not in valid_positions \
                            and projectMath.isPointInCube([x, y, z], flood_fill_area):
                        stack.append((x, ground_height, z))

        return valid_positions

    def verifCornersHouse(self, pos_x, pos_y, pos_z, corner_positions):
        if not projectMath.isPointInCube([pos_x, pos_y, pos_z], self.buildArea):
            return False

        for i, j in [[0, 1], [2, 1], [0, 3], [2, 3]]:
            if projectMath.isPointInSquare([pos_x + corner_positions[i], pos_z + corner_positions[j]],
                                           [self.buildArea[0], self.buildArea[2], self.buildArea[3],
                                            self.buildArea[5]]):
                if self.is_ground(pos_x + corner_positions[i], pos_y, pos_z + corner_positions[j]) == -1:
                    return False
            else:
                return False

        return True

    def takeRandomPosition(self, structure_size):
        x_range = 1 - self.startPosRange[0]
        z_range = 1 - self.startPosRange[1]

        lower_limit = int(self.buildArea[0] + self.size[0] * x_range + structure_size)
        upper_limit = int(self.buildArea[3] - self.size[0] * x_range - structure_size)
        x_pos = random.randint(lower_limit, upper_limit)

        lower_limit = int(self.buildArea[2] + self.size[1] * z_range + structure_size)
        upper_limit = int(self.buildArea[5] - self.size[1] * z_range - structure_size)
        z_pos = random.randint(lower_limit, upper_limit)

        return x_pos, z_pos

    def takeNewPositionForHouse(self, size_struct):
        indices = list(range(0, len(self.structures)))

        while len(indices) > 0:
            index = random.randint(0, len(indices) - 1)

            # Test if new houses position is in build Area
            if projectMath.isPointInSquare([self.structures[indices[index]][0], self.structures[indices[index]][2]],
                                           [self.buildArea[0] + size_struct, self.buildArea[2] + size_struct,
                                            self.buildArea[3] - size_struct, self.buildArea[5] - size_struct]):
                index_place = random.randint(0, len(self.structures[indices[index]][4]) - 1)

                if not isinstance(self.structures[indices[index]][4][index_place], int):
                    self.previous_structure = indices[index]
                    return self.structures[indices[index]][4][index_place]

            del indices[index]

        return 0, 0, 0

    def isOverlapAnyHouse(self, debug, position, chosen_corner):
        verif_corners = True
        verif_houses: list = self.structures.copy()
        verif_overlaps_house = True

        while verif_houses and verif_corners:
            house = verif_houses.pop()

            if not projectMath.isTwoRectOverlaps(position, chosen_corner, [house[0], house[2]], house[3], self.minDistanceHouse):
                verif_overlaps_house = True
            else:
                """print("N " + str(xPos) + " " + str(zPos) + " " + str(chosenCorner) +  " : flip " + str(rand1) + 
                ", rot " + str(rand2) + " ::" + str(house[0]) + " " + str(house[2]))"""
                verif_overlaps_house = False
                verif_corners = False
                debug -= 1

        return verif_overlaps_house, verif_corners, debug

    def findPosHouse(self, corner_pos, base_facing="north"):
        size_struct = max(abs(corner_pos[0][0]) + abs(corner_pos[0][2]) + 1,
                          abs(corner_pos[0][1]) + abs(corner_pos[0][3]) + 1)
        if len(self.structures) % 4 == 0:
            self.floodfillHouseSpace += 1

        not_found = True
        debug = 250 * 16
        debug_no_house = 250 * 16
        verif_corners = False
        # print("there is already", len(self.listHouse), "placed")

        x_pos: int = -1
        y_pos: int = -1
        z_pos: int = -1
        chosen_flip: int = -1
        chosen_rotation: int = -1
        chosen_corner: list = [0, 0, 0]
        flood_fill_value = [-1, -1, -1]

        while not_found and (debug > 0) and (debug_no_house > 0) and not verif_corners:
            if len(self.structures) == 0:
                x_pos, z_pos = self.takeRandomPosition(size_struct)

                y_pos = Constants.getHeight(x_pos, z_pos)
                if Iu.getBlock(x_pos, y_pos, z_pos) == 'minecraft:water':
                    continue

                # print("starting position :" ,x_pos, y_pos, z_pos)

                list_all_flips = [0, 1, 2, 3]
                while list_all_flips and not_found:
                    chosen_flip = list_all_flips[random.randint(0, len(list_all_flips) - 1)]

                    list_all_flips.remove(chosen_flip)
                    list_all_rotation = [0, 1, 2, 3]
                    while list_all_rotation and not_found:
                        chosen_rotation = list_all_rotation[random.randint(0, len(list_all_rotation) - 1)]
                        list_all_rotation.remove(chosen_rotation)

                        chosen_corner = corner_pos[chosen_flip * 4 + chosen_rotation]

                        if self.verifCornersHouse(x_pos, y_pos, z_pos, chosen_corner):
                            not_found = False
                            # To be sure the place is large enough to build the village
                            flood_fill_value = self.floodfill(x_pos, y_pos, z_pos, self.distanceFirstHouse)

                            if len(flood_fill_value) > 5000:
                                flood_fill_value = self.floodfill(x_pos, y_pos, z_pos,
                                                                  size_struct + self.floodfillHouseSpace)
                            else:
                                not_found = True
                                debug_no_house -= 1
            else:
                verif_corners = False

                while not verif_corners and debug > 0:
                    x_pos, y_pos, z_pos = self.takeNewPositionForHouse(size_struct)
                    # to get a random flip and rotation and to test if one is possible
                    if Iu.getBlock(x_pos, y_pos, z_pos) == 'minecraft:water':
                        continue

                    facing: str = projectMath.computeOrientation([x_pos, y_pos, z_pos], self.computeCenter())
                    priority: list = projectMath.makeListOrientationFrom(facing)
                    list_flip_rotation: list = [[], [], [], []]
                    compositions: list = []

                    for flip in range(4):
                        for rotation in range(4):
                            result: str = projectMath.computeNewOrientation(base_facing, flip, rotation)
                            list_flip_rotation[priority.index(result)].append([flip, rotation])

                    for index in range(4):
                        random.shuffle(list_flip_rotation[index])
                        compositions.extend(list_flip_rotation[index])

                    while compositions and not_found:
                        chosen_flip, chosen_rotation = compositions[0]
                        del compositions[0]

                        chosen_corner = corner_pos[chosen_flip * 4 + chosen_rotation]

                        if self.verifCornersHouse(x_pos, y_pos, z_pos, chosen_corner):
                            verif_overlaps_house, verif_corners, debug = self.isOverlapAnyHouse(debug, [x_pos, z_pos], chosen_corner)

                            if verif_corners and verif_overlaps_house:
                                """print("Y " + str(x_pos) + " " + str(z_pos) + " " + str(chosen_corner) + " : flip " + str(chosen_flip) + 
                                    ", rot " + str(chosen_rotation) + " ::" + str(house[0]) + " " + str(house[2]))"""
                                not_found = False

                                # If house is valid to create a floodfill
                                if projectMath.isPointInSquare([x_pos, z_pos], self.validHouseFloodFillPosition):
                                    flood_fill_value = self.floodfill(x_pos, y_pos, z_pos, size_struct // 2 + self.floodfillHouseSpace)
                                else:
                                    flood_fill_value = [x_pos, y_pos, z_pos]
                        else:
                            verif_corners = False
                            debug -= 1

        if debug <= 0:
            dictionary = {"position": [x_pos, y_pos, z_pos], "validPosition": False, "flip": chosen_flip,
                          "rotation": chosen_rotation,
                          "corner": chosen_corner}

            # self.listHouse.append((x_pos, y_pos - 1, z_pos, chosen_corner, flood_fill_value, -1, False))

            # print("debug failed")
        else:
            self.structures.append((x_pos, y_pos, z_pos, chosen_corner, flood_fill_value, self.previous_structure))

            dictionary = {"position": [x_pos, y_pos - 1, z_pos], "validPosition": True, "flip": chosen_flip,
                          "rotation": chosen_rotation,
                          "corner": chosen_corner}
        return dictionary

    def decideMinMax(self):
        houses_to_verify: list = self.structures.copy()

        x_min = 0
        x_max = 0
        z_min = 0
        z_max = 0

        if houses_to_verify:
            house = houses_to_verify.pop()
            x_min = house[0]
            x_max = x_min
            z_min = house[2]
            z_max = z_min
        while houses_to_verify:
            house = houses_to_verify.pop()
            if house[0] < x_min:
                x_min = house[0]
            if house[2] < z_min:
                z_min = house[2]
            if house[0] > x_max:
                x_max = house[0]
            if house[2] > z_max:
                z_max = house[2]
        # print("range of the village is : ", x_min, x_max, z_min, z_max)
        return x_min, x_max, z_min, z_max

    def placeDecorations(self, settlement_data: SettlementData, road, wallConstruction):
        x_min, x_max, z_min, z_max = self.decideMinMax()
        decorations_coord: list = []

        for i in range(self.numberOfDecoration):
            should_place_decoration = True
            debug = 5
            rand = random.randint(1, 10)
            while should_place_decoration and debug > 0:
                debug -= 1

                x_rand = random.randint(x_min, x_max)
                z_rand = random.randint(z_min, z_max)
                height = Constants.getHeight(x_rand, z_rand)
                if Iu.getBlock(x_rand, height, z_rand) == 'minecraft:water':
                    #print("Exit water")
                    continue

                if projectMath.isInHouse(self.structures, [x_rand, z_rand]):
                    #print("Exit house")
                    continue

                if road.isInRoad([x_rand, z_rand]):
                    #print("Exit In road")
                    continue

                if road.isInLantern([x_rand, z_rand]):
                    #print("Exit In lantern")
                    continue

                if [x_rand, z_rand] in decorations_coord:
                    #print("Exit In decoration")
                    continue

                if not wallConstruction.isBlockInEnclosure(x_rand, z_rand):
                    #print("Exit outside walls")
                    continue

                if rand == 1:
                    decorations_coord.append([x_rand, z_rand])
                    self.world_modification.setBlock(x_rand, height, z_rand,
                                                     "minecraft:" + settlement_data.getMaterialReplacement(
                                                         "woodType") + "_fence")

                    random_bloc = random.randint(0, len(Constants.DOUBLE_BLOC) - 1)
                    block_to_place = Constants.DOUBLE_BLOC[random_bloc]
                    if block_to_place == 'minecraft:skeleton_skull' \
                            or block_to_place == 'minecraft:zombie_head' \
                            or block_to_place == 'minecraft:creeper_head':
                        orientation = random.randint(0, 15)
                        block_to_place = block_to_place + '[rotation=' + str(orientation) + ']'

                        self.world_modification.setBlock(x_rand, height + 1, z_rand, block_to_place)

                    elif rand == 2 or rand == 3:
                        decorations_coord.append([x_rand, z_rand])
                        random_bloc = random.randint(0, len(Constants.SINGLE_BLOC) - 1)
                        self.world_modification.setBlock(x_rand, height, z_rand, Constants.SINGLE_BLOC[random_bloc])
                    elif rand == 4 or rand == 5:
                        decorations_coord.append([x_rand, z_rand])
                        random_bloc = random.randint(0, len(Constants.LIGHT_BLOC) - 1)
                        self.world_modification.setBlock(x_rand, height, z_rand, Constants.LIGHT_BLOC[random_bloc])
                    else:
                        decorations_coord.append([x_rand, z_rand])
                        random_bloc = random.randint(0, len(Constants.FLOWERS) - 1)
                        self.world_modification.setBlock(x_rand, height, z_rand,
                                                         'minecraft:potted_' + Constants.FLOWERS[random_bloc])
