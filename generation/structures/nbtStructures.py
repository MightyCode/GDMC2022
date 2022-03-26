from generation.structures.baseStructure import BaseStructure
from generation.buildingCondition import BuildingCondition
from generation.chestGeneration import ChestGeneration
import utils.projectMath as projectMath
import utils.util as util

from nbt import nbt

"""
Structure using nbt
"""


class NbtStructures(BaseStructure):
    REPLACEMENTS = "replacements"
    CHANGE = "Change"
    CHANGE_TO = "ChangeTo"
    CHANGE_STATE = "ChangeState"
    CHANGE_ORIGINAL_BLOCK = "OriginalBlock"
    CHANGE_REPLACEMENT_WORD = "ReplacementWord"
    CHANGE_EXCLUDED_ZONES = "ExcludedZone"

    REPLACEMENTS_EXCLUSIVE = {
        "oak": "dark_oak"
    }

    """
    Constructor of the class
    It will use the nbt file and mark it to indicate if the block in palette should change with replacements in building condition
    """

    def __init__(self, nbt_file, info, name):
        super(BaseStructure, self).__init__()
        self.setInfo(info)

        self.setSize([nbt_file["size"][0].value, nbt_file["size"][1].value, nbt_file["size"][2].value])
        self.file = nbt_file
        self.name = name

        # Variable used on building
        self.placeImmediately: bool = False

        self.computedOrientation: dict = {}
        # Indicate for each block in palette if it should change or not and to change to what
        for block in self.file["palette"]:
            if NbtStructures.REPLACEMENTS in self.info.keys():
                block_name = block["Name"].value.split("[")[0]

                for replacementWord in self.info[NbtStructures.REPLACEMENTS].keys():
                    # Checking for block replacement
                    if replacementWord == block_name:
                        block.tags.append(nbt.TAG_Int(name=NbtStructures.CHANGE_STATE,
                                                      value=self.info[NbtStructures.REPLACEMENTS][block_name]["state"]))
                        #  """AND states equals"""
                        if block[NbtStructures.CHANGE_STATE].value == 1 or (
                                block[NbtStructures.CHANGE_STATE].value == 0):
                            block.tags.append(nbt.TAG_Byte(name=NbtStructures.CHANGE, value=True))

                            block.tags.append(nbt.TAG_String(name=NbtStructures.CHANGE_TO,
                                                             value=self.info[NbtStructures.REPLACEMENTS][block["Name"].value]["type"]))
                            block.tags.append(
                                nbt.TAG_String(name=NbtStructures.CHANGE_ORIGINAL_BLOCK, value=block["Name"].value))
                            block.tags.append(
                                nbt.TAG_String(name=NbtStructures.CHANGE_REPLACEMENT_WORD, value=replacementWord))
                            block.tags.append(nbt.TAG_Byte(name=NbtStructures.CHANGE_EXCLUDED_ZONES,
                                                           value=("excluded" in self.info[NbtStructures.REPLACEMENTS][
                                                               replacementWord].keys())))
                            break

                    # Checking for substr replacement 
                    elif replacementWord in block_name:
                        # The replacementWord can be in unexpected blocks
                        # "oak" is on every "...dark_oak..." block
                        if replacementWord in NbtStructures.REPLACEMENTS_EXCLUSIVE:
                            if NbtStructures.REPLACEMENTS_EXCLUSIVE[replacementWord] in block_name:
                                continue

                        if replacementWord in self.info[NbtStructures.REPLACEMENTS].keys():
                            if self.info[NbtStructures.REPLACEMENTS][replacementWord]["state"] == 2:
                                block.tags.append(nbt.TAG_Byte(name=NbtStructures.CHANGE, value=True))
                                block.tags.append(nbt.TAG_String(name=NbtStructures.CHANGE_TO,
                                                                 value=self.info[NbtStructures.REPLACEMENTS][replacementWord]["type"]))

                                block.tags.append(nbt.TAG_Int(name=NbtStructures.CHANGE_STATE, value=2))
                                block.tags.append(
                                    nbt.TAG_String(name=NbtStructures.CHANGE_ORIGINAL_BLOCK,
                                                   value=block["Name"].value))
                                block.tags.append(
                                    nbt.TAG_String(name=NbtStructures.CHANGE_REPLACEMENT_WORD, value=replacementWord))

                                # True or False
                                block.tags.append(nbt.TAG_Byte(name=NbtStructures.CHANGE_EXCLUDED_ZONES,
                                                               value=("excluded" in
                                                                      self.info[NbtStructures.REPLACEMENTS][
                                                                          replacementWord].keys())))
                                break

            block.tags.append(nbt.TAG_Byte(name=NbtStructures.CHANGE, value=False))

        # Looting table
        self.lootTable = False
        if "lootTables" in self.info.keys():
            self.lootTable = len(self.info["lootTables"]) > 0

    """
    Just return corners
    """

    def setupInfoAndGetCorners(self):
        return self.getCornersLocalPositionsAllFlipRotation(self.info["mainEntry"]["position"])

    """ 
    Fill dict with mandatory informations
    flip : flip applied to localspace, [0|1|2|3]
    rotation : rotation applied to localspace, [0|1|2|3]
    """

    def getNextBuildingInformation(self, flip: int, rotation: int) -> dict:
        return {
            "entry": {
                "position": self.info["mainEntry"]["position"].copy(),
                "facing": self.getFacingMainEntry(flip, rotation)},
            "size": self.size,
            "corner": self.getCornersLocalPositions(self.info["mainEntry"]["position"].copy(), flip, rotation)
        }

    def build(self, world_modification, building_conditions: BuildingCondition, chest_generation: ChestGeneration,
              block_transformations: list) -> None:

        ## Pre computing :
        building_conditions.referencePoint = building_conditions.referencePoint.copy()
        self.computeOrientation(building_conditions.rotation, building_conditions.flip)
        self.block_transformation = block_transformations

        if building_conditions.flip == 1 or building_conditions.flip == 3:
            building_conditions.referencePoint[0] = self.size[0] - 1 - building_conditions.referencePoint[0]
        if building_conditions.flip == 2 or building_conditions.flip == 3:
            building_conditions.referencePoint[2] = self.size[2] - 1 - building_conditions.referencePoint[2]

            # Replace bloc by these given
        for block_palette in self.file["palette"]:
            if block_palette[NbtStructures.CHANGE].value:
                change_state = block_palette[NbtStructures.CHANGE_STATE].value

                if change_state == 0 or change_state == 1:
                    block_palette["Name"].value = \
                        building_conditions.replacements[block_palette[NbtStructures.CHANGE_TO].value].split("[")[0]
                elif change_state == 2:
                    block_palette["Name"].value = block_palette[NbtStructures.CHANGE_ORIGINAL_BLOCK].value.replace(
                        block_palette[NbtStructures.CHANGE_REPLACEMENT_WORD].value,
                        building_conditions.replacements[block_palette[NbtStructures.CHANGE_TO].value].split("[")[0])

        # Place support underHouse
        self.placeSupportUnderStructure(world_modification, building_conditions)

        # Air zone
        self.placeAirZones(world_modification, building_conditions)

        ## Computing : Modify from blocks
        for block in self.file["blocks"]:
            block_palette = self.file["palette"][block["state"].value]
            self.placeImmediately = False

            # Check if the current block is in excluded zone
            should_take_original_block = False
            block_name = block_palette["Name"].value
            if block_palette[NbtStructures.CHANGE].value:
                if block_palette[NbtStructures.CHANGE_EXCLUDED_ZONES].value:
                    for zone in self.info["replacements"][block_palette[NbtStructures.CHANGE_REPLACEMENT_WORD].value]["excluded"]:
                        if projectMath.isPointInSquare(
                                [block["pos"][0].value, block["pos"][1].value, block["pos"][2].value], zone):
                            should_take_original_block = True
                            block_name = block_palette[NbtStructures.CHANGE_ORIGINAL_BLOCK].value
                            break

            # Check for block air replacement
            if block_name in NbtStructures.AIR_BLOCKS and building_conditions.replaceAirMethod != 1:
                continue

            # Compute position of block from local space to world space
            block_position = self.returnWorldPosition(
                [block["pos"][0].value, block["pos"][1].value + 1, block["pos"][2].value],
                building_conditions.flip, building_conditions.rotation,
                building_conditions.referencePoint, building_conditions.position)

            self.checkBeforePlacing(block_name)
            new_block_id = self.convertNbtBlockToStr(
                self.file["palette"][block["state"].value],
                block_transformations,
                should_take_original_block
            )

            world_modification.setBlock(
                block_position[0], block_position[1], block_position[2],
                new_block_id, placeImmediately=self.placeImmediately
            )

            self.checkAfterPlacing(block, block_name, block_position, chest_generation, building_conditions)

        # Place sign
        if "sign" in self.info.keys():
            sign_position = self.returnWorldPosition(
                self.info["sign"]["position"],
                building_conditions.flip, building_conditions.rotation,
                building_conditions.referencePoint, building_conditions.position
            )
            sign_position[1] += 1

            self.generateSignatureSign(sign_position, world_modification,
                                       building_conditions.replacements["woodType"],
                                       building_conditions.loreStructure.villagers)

        self.parseSpecialRule(building_conditions, world_modification)

    def checkBeforePlacing(self, block_name: str) -> None:
        if "chest" in block_name or "shulker" in block_name or "lectern" in block_name or "barrel" in block_name:
            self.placeImmediately = True

    def checkAfterPlacing(self, block, block_name, blockPosition, chestGeneration, building_conditions: BuildingCondition):
        # If structure has loot tables and chest encounter
        if "chest" in block_name or "barrel" in block_name:
            if "lootTables" not in self.info:
                return

            if self.lootTable:
                chosen_loot_table = ""
                for lootTable in self.info["lootTables"]:
                    if len(lootTable) == 1:
                        chosen_loot_table = lootTable[0]
                    elif projectMath.isPointInCube(
                            [block["pos"][0].value, block["pos"][1].value, block["pos"][2].value], lootTable[1]):
                        chosen_loot_table = lootTable[0]

                if chosen_loot_table != "":
                    additional_objects = []
                    if chosen_loot_table in building_conditions.special.keys():
                        additional_objects = building_conditions.special[chosen_loot_table]

                    chestGeneration.generate(blockPosition[0], blockPosition[1], blockPosition[2], chosen_loot_table,
                                             building_conditions.replacements, additional_objects)

        if "lectern" in block_name:
            if "lectern" not in self.info:
                return

            for key in self.info["lectern"].keys():
                position = self.info["lectern"][key]
                if block["pos"][0].value == position[0] and block["pos"][1].value == position[1] and block["pos"][2].value == position[2]:
                    result = util.changeNameWithBalise(key, building_conditions.replacements)
                    if result[0] >= 0:
                        util.addBookToLectern(blockPosition[0], blockPosition[1], blockPosition[2], result[1])
                    else:
                        print("Can't add a book to a lectern at pos : " + str(blockPosition))
                    break

    def convertNbtBlockToStr(self, block_palette, block_transformations: list, take_original_block_name=False):
        if take_original_block_name:
            block = block_palette[NbtStructures.CHANGE_ORIGINAL_BLOCK].value
        else:
            block = block_palette["Name"].value

        block = self.applyBlockTransformation(block)

        properties = "["
        if "Properties" in block_palette.keys():
            for key in block_palette["Properties"].keys():
                if self.propertyCompatible(block, key):
                    properties += self.convertProperty(key, block_palette["Properties"][key].value) + ","

            properties = properties[:-1]
        block = block + properties + "]"
        return block
