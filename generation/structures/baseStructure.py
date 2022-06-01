from utils.constants import Constants
from generation.buildingCondition import BuildingCondition

import utils.util as util
import utils.projectMath as projectMath
import lib.interfaceUtils as interfaceUtils

import random
import math

""" 
# Main class which corresponds to a buildable 
"""


class BaseStructure:
    AIR_BLOCKS = ["minecraft:air", "minecraft:void_air", "minecraft:cave_air"]

    ORIENTATIONS = ["west", "north", "east", "south"]

    LIST_ALL_FACING = ["south", "south-southwest", "southwest",
                       "west-southwest", "west", "west-northwest",
                       "northwest", "north-northwest", "north",
                       "north-northeast", "northeast", "east-northeast",
                       "east", "east-southeast", "southeast", "south-southeast"]

    AIR_FILLING_PROBLEMATIC_BLOCS = ["minecraft:sand", "minecraft:red_sand",
                                     "minecraft:gravel", "minecraft:water", "minecraft:lava"]

    """ 
    Empty constructor
    info : dictionary containing information about the structures
    """

    def __init__(self):
        self.info: dict = {}
        self.size: list = [0, 0, 0]
        self.computed_orientation: dict = {}
        self.block_transformation: list = []

    def setInfo(self, info: dict):
        self.info = info
        self.size = [0, 0, 0]
        self.computed_orientation = {}

    """
    Return a premake object required to build a structure
    Flip is applied before rotation
    """

    @staticmethod
    def createBuildingCondition() -> BuildingCondition:
        return BuildingCondition()

    """
    Return a position in the world 
    localPoint : position of the block inside the local space, [0, 0, 0]
    flip : flip applied to local space, [0|1|2|3]
    rotation : rotation applied to local space, [0|1|2|3]
    referencePoint : the origin of the local space, what should be the 0, 0, [0, 0, 0]
    worldStructurePosition : position of the structure in real world, position in relation with reference point
    """

    def returnWorldPosition(self, localPoint: list, flip: int, rotation: int,
                            referencePoint: list, world_structure_position: list) -> list:

        world_position: list = [0, 0, 0]

        # Position in building local space replacement
        if flip == 1 or flip == 3:
            world_position[0] = self.size[0] - 1 - localPoint[0]
        else:
            world_position[0] = localPoint[0]

        if flip == 2 or flip == 3:
            world_position[2] = self.size[2] - 1 - localPoint[2]
        else:
            world_position[2] = localPoint[2]

        world_position[1] = localPoint[1]

        # Take rotation into account, apply to building local positions
        world_position[0], world_position[2] = projectMath.rotatePointAround(
            [world_structure_position[0] + referencePoint[0], world_structure_position[2] + referencePoint[2]],
            [world_structure_position[0] + world_position[0], world_structure_position[2] + world_position[2]],
            rotation * math.pi / 2)

        # Position in real world
        world_position[0] = int(world_position[0]) - referencePoint[0]
        world_position[1] = world_structure_position[1] + world_position[1] - referencePoint[1]
        world_position[2] = int(world_position[2]) - referencePoint[2]

        return world_position

    """
    Convert a property using computedOrientation (left, right, north, south, east, west)
    """

    def convertProperty(self, property_name, property_value):
        result: str = property_value

        if property_value in self.computed_orientation.keys():
            result = self.computed_orientation[property_value]

        return property_name + "=" + result

    """
    Return number, depending to the rotation
    """

    def returnRotationFromFacing(self, facing):
        for i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]:
            if BaseStructure.LIST_ALL_FACING[i] == facing:
                return i

        return -1

    """
    Compute all orientation
    rotation : rotation applied to the structure, No rotation = 0, rotation 90° = 1, rotation 180° = 2, rotation 270° = 3
    flip : flip applied to the structure, No flip = 0, Flip x = 1, flip z = 2, Flip xz = 3
    """

    def computeOrientation(self, rotation, flip):
        # Construct orientation
        self.computed_orientation = {
            "left": "left",
            "right": "right",
            "x": "x",
            "y": "y",
            BaseStructure.ORIENTATIONS[0]: BaseStructure.ORIENTATIONS[0],
            BaseStructure.ORIENTATIONS[1]: BaseStructure.ORIENTATIONS[1],
            BaseStructure.ORIENTATIONS[2]: BaseStructure.ORIENTATIONS[2],
            BaseStructure.ORIENTATIONS[3]: BaseStructure.ORIENTATIONS[3]
        }

        # Apply flip to orientation
        if flip == 1 or flip == 3:
            self.computed_orientation["east"] = "west"
            self.computed_orientation["west"] = "east"

        if flip == 2 or flip == 3:
            self.computed_orientation["south"] = "north"
            self.computed_orientation["north"] = "south"

        if flip == 1 or flip == 2:
            self.computed_orientation["left"] = "right"
            self.computed_orientation["right"] = "left"

        # Apply rotation to orientation
        for orientation in self.computed_orientation.keys():
            if orientation in BaseStructure.ORIENTATIONS:
                self.computed_orientation[orientation] = BaseStructure.ORIENTATIONS[
                    (BaseStructure.ORIENTATIONS.index(self.computed_orientation[orientation]) + rotation) % len(
                        BaseStructure.ORIENTATIONS)
                    ]

        if rotation == 1 or rotation == 3:
            self.computed_orientation["x"] = "z"
            self.computed_orientation["z"] = "x"

    def parseSpecialRule(self, building_conditions: BuildingCondition, world_modification):
        if "special" not in self.info.keys():
            return

        for key in self.info["special"].keys():
            if key == "sign":
                i = 0
                for sign in self.info["special"][key]:
                    if len(building_conditions.special["sign"]) <= i * 4:
                        break

                    sign_position = self.returnWorldPosition(
                        sign["position"],
                        building_conditions.flip, building_conditions.rotation,
                        building_conditions.referencePoint, building_conditions.position
                    )

                    world_modification.setBlock(
                        sign_position[0], sign_position[1] + 1, sign_position[2],
                        "minecraft:" + building_conditions.replacements["woodType"]
                        + "_wall_sign[facing=" + self.computed_orientation[sign["orientation"]] + "]",
                        False, True)

                    if building_conditions.special["sign"][i * 4] == "" and building_conditions.special["sign"][i * 4 + 1] == "":
                        if building_conditions.special["sign"][i * 4 + 2] == "" and \
                                building_conditions.special["sign"][i * 4 + 3] == "":
                            continue

                    interfaceUtils.setSignText(
                        sign_position[0], sign_position[1] + 1, sign_position[2],
                        building_conditions.special["sign"][i * 4], building_conditions.special["sign"][i * 4 + 1],
                        building_conditions.special["sign"][i * 4 + 2],
                        building_conditions.special["sign"][i * 4 + 3])

                    i += 1

    """
    Return position where reference position is the center of the local space
    referencePosition : the origin of the local space, what should be the 0, 0,  [0, 0, 0]
    flip : flip applied to local space, [0|1|2|3]
    rotation : rotation applied to local space, [0|1|2|3]
    """

    def getCornersLocalPositions(self, reference_position, flip, rotation):
        ref_position = reference_position.copy()
        if flip == 1 or flip == 3:
            ref_position[0] = self.size[0] - 1 - ref_position[0]

        if flip == 2 or flip == 3:
            ref_position[2] = self.size[2] - 1 - ref_position[2]

        temp = projectMath.rotatePointAround([0, 0], [- ref_position[0], - ref_position[2]], math.pi / 2 * rotation)

        temp1 = projectMath.rotatePointAround([0, 0],
                                              [self.size[0] - 1 - ref_position[0], self.size[2] - 1 - ref_position[2]],
                                              math.pi / 2 * rotation)

        return [int(min(temp[0], temp1[0])),
                int(min(temp[1], temp1[1])),
                int(max(temp[0], temp1[0])),
                int(max(temp[1], temp1[1]))]

    def returnFlipRotationThatIsInZone(self, position, main_entry_position, area) -> tuple:
        flip: int = random.randint(0, 3)
        rotation: int = 0
        rotations: list = list(range(4))
        valid: bool = False

        while len(rotations) > 0 and not valid:
            valid = True
            index = random.randint(0, len(rotations) - 1)
            rotation = rotations[index]
            del rotations[index]

            corner = self.getCornersLocalPositions(main_entry_position, flip, rotation)

            for i, j in [[0, 1], [2, 1], [0, 3], [2, 3]]:
                if not projectMath.isPointInSquare(
                        [position[0] + corner[i], position[1] + corner[j]],
                        [area[0], area[2], area[3], area[5]]):
                    valid = False
                    break

        return flip, rotation

    """
    Get corners of all possible flip and rotation
    """

    def getCornersLocalPositionsAllFlipRotation(self, reference_position) -> list:
        corners: list = []
        for flip in [0, 1, 2, 3]:
            for rotation in [0, 1, 2, 3]:
                corners.append(self.getCornersLocalPositions(reference_position, flip, rotation))

        return corners

    """
    Place wall sign, which
    position : position of the upper sign
    worldModification : class used to place blocks
    woodType : type of wood for the sign
    people : people's name which should appears in the sign
    """

    def generateSignatureSign(self, position, world_modification, wood_type: str, villagers: list):
        if "sign" not in self.info.keys():
            return

        world_modification.setBlock(position[0], position[1], position[2], "minecraft:air", place_immediately=True)
        world_modification.setBlock(position[0], position[1], position[2],
                                    "minecraft:" + wood_type + "_wall_sign[facing=" + self.computed_orientation[
                                        self.info["sign"]["facing"]] + "]",
                                    place_immediately=True)

        lines = ["", "", "", "", "", "", "", ""]
        lines[0] = "Tier " + str(self.info["sign"]["tier"])
        lines[1] = self.info["sign"]["name"]

        names: list = []
        for villager in villagers:
            names.append(villager.name)

        util.parseVillagerNameInLines(names, lines, 2)

        interfaceUtils.setSignText(
            position[0], position[1], position[2],
            lines[0], lines[1], lines[2], lines[3])

        if len(lines[4]) > 0:
            world_modification.setBlock(position[0], position[1] - 1, position[2], "minecraft:air",
                                        place_immediately=True)
            world_modification.setBlock(position[0], position[1] - 1, position[2],
                                        "minecraft:" + wood_type + "_wall_sign[facing=" + self.computed_orientation[
                                            self.info["sign"]["facing"]] + "]",
                                        place_immediately=True)

            interfaceUtils.setSignText(
                position[0], position[1] - 1, position[2],
                lines[4], lines[5], lines[6], lines[7])

    """
    Place ground under the structure at given position
    worldModification : class used to place blocks
    buildingCondition : condition used to build a structures
    """

    def placeSupportUnderStructure(self, world_modification, building_conditions: BuildingCondition) -> None:
        if "ground" not in self.info.keys():
            return

        zones: list = []
        if "info" in self.info["ground"].keys():
            if "all" == self.info["ground"]["info"]:
                zones.append([0, 0, self.size[0] - 1, self.size[2] - 1])
        elif "zones" in self.info["ground"].keys():
            zones = self.info["ground"]["zones"]

        for zone in zones:
            for x in range(zone[0], zone[2] + 1):
                for z in range(zone[1], zone[3] + 1):
                    position = self.returnWorldPosition(
                        [x, 0, z],
                        building_conditions.flip, building_conditions.rotation,
                        building_conditions.referencePoint, building_conditions.position
                    )

                    if interfaceUtils.getBlock(position[0], position[1],
                                               position[2]) in Constants.IGNORED_BLOCKS:
                        i = -2
                        while interfaceUtils.getBlock(position[0], position[1] + i,
                                                      position[2]) in Constants.IGNORED_BLOCKS:
                            i -= 1

                        world_modification.fillBlocks(position[0], position[1], position[2], position[0],
                                                      position[1] + i,
                                                      position[2], "minecraft:stone")
                        """building_conditions.replacements["ground2"]"""

    """
    Place air at given position
    worldModification : class used to place blocks
    buildingCondition : condition used to build a structures
    """

    def placeAirZones(self, world_modification, building_conditions: BuildingCondition, terrainModification):
        building_conditions.referencePoint = building_conditions.referencePoint.copy()
        self.computeOrientation(building_conditions.rotation, building_conditions.flip)

        if building_conditions.flip == 1 or building_conditions.flip == 3:
            building_conditions.referencePoint[0] = self.size[0] - 1 - building_conditions.referencePoint[0]
        if building_conditions.flip == 2 or building_conditions.flip == 3:
            building_conditions.referencePoint[2] = self.size[2] - 1 - building_conditions.referencePoint[2]

        if building_conditions.replaceAirMethod == BuildingCondition.FILE_PREFERENCE_AIR_PLACEMENT:
            building_conditions.replaceAirMethod = self.info["air"]["preferredAirMode"]

        zone_to_remove: list = []

        if building_conditions.replaceAirMethod == BuildingCondition.CHOSEN_AIR_PLACEMENT:
            for zones in self.info["air"]["replacements"]:
                block_from = self.returnWorldPosition([zones[0], zones[1] + 1, zones[2]],
                                                      building_conditions.flip, building_conditions.rotation,
                                                      building_conditions.referencePoint,
                                                      building_conditions.position)
                block_to = self.returnWorldPosition([zones[3], zones[4] + 1, zones[5]],
                                                    building_conditions.flip, building_conditions.rotation,
                                                    building_conditions.referencePoint,
                                                    building_conditions.position)

                zone_to_remove.append([block_from, block_to])
        elif building_conditions.replaceAirMethod == BuildingCondition.ALL_AIR_PLACEMENT:
            zone_to_remove.append([
                self.returnWorldPosition([0, 1, 0],
                                         building_conditions.flip, building_conditions.rotation,
                                         building_conditions.referencePoint,
                                         building_conditions.position),

                self.returnWorldPosition([self.size[0] - 1, self.size[1] + 1, self.size[2] - 1],
                                         building_conditions.flip, building_conditions.rotation,
                                         building_conditions.referencePoint,
                                         building_conditions.position)
            ])

        for zone in zone_to_remove:
            for x in range(min(zone[0][0], zone[1][0]), max(zone[0][0], zone[1][0]) + 1):
                for z in range(min(zone[0][2], zone[1][2]), max(zone[0][2], zone[1][2]) + 1):
                    for y in range(zone[0][1], zone[1][1] + 1):
                        terrainModification.removeRecursivelyAt(world_modification, x, y, z)

                    if interfaceUtils.getBlock(x, zone[1][1] + 1, z) in BaseStructure.AIR_FILLING_PROBLEMATIC_BLOCS:
                        world_modification.setBlock(x, zone[1][1] + 1, z, "minecraft:stone", place_immediately=True)

            world_modification.fillBlocks(zone[0][0], zone[0][1], zone[0][2], zone[1][0], zone[1][1],
                                          zone[1][2],
                                          BaseStructure.AIR_BLOCKS[0])

    def applyBlockTransformation(self, block: str):
        return util.applyBlockTransformation(block, self.block_transformation)

    def applyBlockTransformationThenPlace(self, world_modification, position_x: int, position_y: int, position_z: int,
                                          block: str) -> None:
        util.applyBlockTransformationThenPlace(world_modification, position_x, position_y, position_z,
                                               block, self.block_transformation)

    def applyBlockTransformationThenFill(self, world_modification, from_x: int, from_y: int, from_z: int,
                                         to_x: int, to_y: int, to_z: int, block: str):
        util.applyBlockTransformationThenFill(world_modification, from_x, from_y, from_z,
                                              to_x, to_y, to_z, block, self.block_transformation)

    def checkAfterPlacing(self, x, y, z, block_name, world_position, chestGeneration,
                          building_conditions: BuildingCondition):
        # If structure has loot tables and chest encounter
        if "chest" in block_name or "barrel" in block_name:
            additional_objects: list = []

            if "special" in self.info.keys():
                if "additionalItem" in self.info["special"].keys():
                    position: list
                    for key in self.info["special"]["additionalItem"]:
                        position = self.info["special"]["additionalItem"][key]

                        if x == position[0] and y == position[1] and z == position[2]:
                            if key in building_conditions.special.keys():
                                for item in building_conditions.special[key]:
                                    additional_objects.append(item)

            if self.lootTable or len(additional_objects) > 0:
                chosen_loot_table: str = "empty"
                if self.lootTable:
                    for lootTable in self.info["lootTables"]:
                        if len(lootTable) == 1:
                            chosen_loot_table = lootTable[0]
                        elif projectMath.isPointInCube([x, y, z], lootTable[1]):
                            chosen_loot_table = lootTable[0]

                chestGeneration.generate(world_position[0], world_position[1], world_position[2], chosen_loot_table,
                                         building_conditions.replacements, additional_objects)

        if "lectern" in block_name:
            if "lectern" not in self.info:
                return

            for key in self.info["lectern"].keys():
                if [x, y, z] == self.info["lectern"][key]:
                    result = util.changeNameWithReplacements(key, building_conditions.replacements)
                    if result[0] >= 0:
                        util.addBookToLectern(world_position[0], world_position[1], world_position[2], result[1])
                    else:
                        print("Can't add a book to a lectern at pos : " + str(world_position))
                    break

    """
    Get the facing of the main entry depending of the flip and rotation
    flip : flip applied to local space, [0|1|2|3]
    rotation : rotation applied to local space, [0|1|2|3]
    """

    def getFacingMainEntry(self, flip: int, rotation: int) -> str:
        self.computeOrientation(rotation, flip)
        return self.computed_orientation[self.info["mainEntry"]["facing"]]

    """
    Base function 
    Get all corners and setup variables
    """

    def setupInfoAndGetCorners(self) -> list:
        return []

    """
    Base function 
    Setup all variables which requires flip and rotation
    Return a dict with ["size"] of structure and ["entry]["position], ["entry]["facing"]
    flip : flip applied to local space, [0|1|2|3]
    rotation : rotation applied to local space, [0|1|2|3]
    """

    def getNextBuildingInformation(self, flip, rotation) -> dict:
        return {}

    """
    Protected method
    Set size of structure
    """

    def setSize(self, size) -> None:
        self.size = size

    """
    Get size of structure
    Work for structure
    Work sometimes depending when called in hand made (generated) structure.
    """

    def getSize(self) -> list:
        return self.size

    """
    Get size x
    """

    def size_x(self) -> int:
        return self.size[0]

    """
    Get size y
    """

    def size_y(self) -> int:
        return self.size[1]

    """
    Get size z
    """

    def size_z(self) -> int:
        return self.size[2]

    """
    Get size of structure when rotated 90° or 270°
    """

    def getRotatedSize(self) -> list:
        return [self.size[2], self.size[1], self.size[0]]

    """
    Indicates if property is valid with a block
    blockName : name of the block
    property : property which should be applied with blockName
    """

    @staticmethod
    def propertyCompatible(block_name, block_property):
        if block_property == "snowy":
            if block_name != "minecraft:grass_block":
                return False

        if block_name == "minecraft:air" \
                or block_name == "minecraft:cave_air" \
                or block_name == "minecraft:void_air" \
                or block_name == "minecraft:coarse_dirt" \
                or "coal" in block_name \
                or "cobweb" in block_name:
            return False

        return True
