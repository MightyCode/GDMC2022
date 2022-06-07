from generation.structures.baseStructure import BaseStructure
from generation.buildingCondition import BuildingCondition
from generation.chestGeneration import ChestGeneration
import utils.projectMath as projectMath

"""
Structure using nbt
"""


class NbtStructures(BaseStructure):
    REPLACEMENTS = "replacements"

    NAME = "Name"
    PROPERTIES = "Properties"

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
        self.name = name

        # Variable used on building
        self.placeImmediately: bool = False

        self.computedOrientation: dict = {}
        self.palette = []
        self.blocks: list = []

        # Indicate for each block in palette if it should change or not and to change to what
        base_palette_block: int = 0

        counter: int = 0
        for block in nbt_file["palette"]:
            self.palette.append(self.appendBlocInPalette(block))
            if self.palette[-1][NbtStructures.NAME] == "minecraft:air":
                base_palette_block = counter

            counter += 1

        for x in range(self.size[0]):
            self.blocks.append([])
            for y in range(self.size[1]):
                self.blocks[x].append([])
                for z in range(self.size[2]):
                    self.blocks[x][y].append(base_palette_block)

        for block in nbt_file["blocks"]:
            position = [block["pos"][0].value, block["pos"][1].value, block["pos"][2].value]
            self.blocks[position[0]][position[1]][position[2]] = block["state"].value

        # Looting table
        self.lootTable = False
        if "lootTables" in self.info.keys():
            self.lootTable = len(self.info["lootTables"]) > 0

    def appendBlocInPalette(self, block):
        if NbtStructures.REPLACEMENTS in self.info.keys():
            block_name = block["Name"].value

            for replacementWord in self.info[NbtStructures.REPLACEMENTS].keys():
                # Checking for block replacement
                if replacementWord == block_name:
                    state: int = self.info[NbtStructures.REPLACEMENTS][block_name]["state"]
                    #  """AND states equals"""
                    if state == 1 or state == 0:
                        return self.createBlockPaletteChanged(
                            block,
                            self.info[NbtStructures.REPLACEMENTS][block["Name"].value]["type"],
                            block["Name"].value,
                            state,
                            replacementWord,
                            "excluded" in self.info[NbtStructures.REPLACEMENTS][replacementWord].keys()
                        )

                # Checking for substr replacement
                elif replacementWord in block_name:
                    # The replacementWord can be in unexpected blocks
                    # "oak" is on every "...dark_oak..." block
                    if replacementWord in NbtStructures.REPLACEMENTS_EXCLUSIVE:
                        if NbtStructures.REPLACEMENTS_EXCLUSIVE[replacementWord] in block_name:
                            continue

                    if replacementWord in self.info[NbtStructures.REPLACEMENTS].keys():
                        if self.info[NbtStructures.REPLACEMENTS][replacementWord]["state"] == 2:
                            return self.createBlockPaletteChanged(
                                block,
                                self.info[NbtStructures.REPLACEMENTS][replacementWord]["type"],
                                block[NbtStructures.NAME].value,
                                2,
                                replacementWord,
                                "excluded" in self.info[NbtStructures.REPLACEMENTS][replacementWord].keys()
                            )

        return self.createBlockPaletteNotChange(block)

    @staticmethod
    def createBlockPaletteNotChange(block) -> dict:
        return {
            NbtStructures.CHANGE: False,
            NbtStructures.NAME: block[NbtStructures.NAME].value,
            NbtStructures.PROPERTIES: NbtStructures.createDictProperty(block)
        }

    @staticmethod
    def createBlockPaletteChanged(block, changeTo, original, changeState, replacementWord, excludedZone):
        return {
            NbtStructures.NAME: original,
            NbtStructures.CHANGE: True,
            NbtStructures.CHANGE_ORIGINAL_BLOCK: original,
            NbtStructures.CHANGE_TO: changeTo,
            NbtStructures.CHANGE_STATE: changeState,
            NbtStructures.CHANGE_EXCLUDED_ZONES: excludedZone,
            NbtStructures.CHANGE_REPLACEMENT_WORD: replacementWord,
            NbtStructures.PROPERTIES: NbtStructures.createDictProperty(block)
        }

    @staticmethod
    def createDictProperty(block) -> dict:
        if NbtStructures.PROPERTIES not in block.keys():
            return {}

        result: dict = {}
        for key in block[NbtStructures.PROPERTIES].keys():
            result[key] = block[NbtStructures.PROPERTIES][key].value

        return result

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
        for block_palette in self.palette:
            if block_palette[NbtStructures.CHANGE]:
                change_state = block_palette[NbtStructures.CHANGE_STATE]

                if change_state == 0 or change_state == 1:
                    block_palette[NbtStructures.NAME] = building_conditions.replacements[block_palette[NbtStructures.CHANGE_TO]]

                elif change_state == 2:
                    block_palette[NbtStructures.NAME] = block_palette[NbtStructures.CHANGE_ORIGINAL_BLOCK] \
                        .replace(block_palette[NbtStructures.CHANGE_REPLACEMENT_WORD],
                                 building_conditions.replacements[block_palette[NbtStructures.CHANGE_TO]])

        # Place support underHouse
        self.placeSupportUnderStructure(world_modification, building_conditions)

        # Air zone
        # self.placeAirZones(world_modification, building_conditions)

        for x in range(self.size[0]):
            for y in range(self.size[1]):
                for z in range(self.size[2]):
                    self.computeBlockAt(building_conditions, world_modification, chest_generation, x, y, z)

        # Place sign
        if "sign" in self.info.keys() and not block_transformations[0].lore_structure.destroyed:
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

    def computeBlockAt(self, building_conditions: BuildingCondition, world_modification,
                       chest_generation: ChestGeneration, x: int, y: int, z: int) -> None:
        block_palette = self.palette[self.blocks[x][y][z]]
        self.placeImmediately = False

        # Check if the current block is in excluded zone
        should_take_original_block = False
        if block_palette[NbtStructures.CHANGE]:
            if block_palette[NbtStructures.CHANGE_EXCLUDED_ZONES]:
                for zone in self.info["replacements"][block_palette[NbtStructures.CHANGE_REPLACEMENT_WORD]]["excluded"]:
                    if projectMath.isPointInCube([x, y, z], zone):
                        should_take_original_block = True
                        break

        block_name = self.convertNbtBlockToStr(block_palette, should_take_original_block)
        # Check for block air replacement
        for air_block in NbtStructures.AIR_BLOCKS:
            """and building_conditions.replaceAirMethod != BuildingCondition.ALL_AIR_PLACEMENT"""
            if air_block in block_name:
                return

        # Compute position of block from local space to world space
        world_position = self.returnWorldPosition(
            [x, y + 1, z],
            building_conditions.flip, building_conditions.rotation,
            building_conditions.referencePoint, building_conditions.position)

        self.checkBeforePlacing(block_name)

        world_modification.setBlock(
            world_position[0], world_position[1], world_position[2],
            block_name, place_immediately=self.placeImmediately
        )

        self.checkAfterPlacing(x, y, z, block_name, world_position, chest_generation, building_conditions)

    def checkBeforePlacing(self, block_name: str) -> None:
        if "chest" in block_name or "shulker" in block_name or "lectern" in block_name or "barrel" in block_name or "banner" in block_name:
            self.placeImmediately = True

    def convertNbtBlockToStr(self, block_palette, take_original_block_name=False):
        block: str
        if take_original_block_name:
            block = block_palette[NbtStructures.CHANGE_ORIGINAL_BLOCK]
        else:
            block = block_palette[NbtStructures.NAME]

        block = self.applyBlockTransformation(block)
        part: list
        if "{" in block:
            index: int = block.index("{")
            part = [block[:index], block[index:]]
        else:
            part = [block, ""]

        properties: str = "["
        for key in block_palette[NbtStructures.PROPERTIES].keys():
            if self.propertyCompatible(block, key):
                properties += self.convertProperty(key, block_palette[NbtStructures.PROPERTIES][key]) + ","

        if len(block_palette[NbtStructures.PROPERTIES]) > 0:
            properties = properties[:-1]

        block = part[0] + properties + "]" + part[1]

        return block

    def getLastLayerBlockPosition(self):
        zones: list = []

        def computeBlockAt(x_pos, z_pos):
            block_palette = self.palette[self.blocks[x_pos][0][z_pos]]

            block_name = block_palette["Name"]
            # Check for block air replacement
            for air_block in NbtStructures.AIR_BLOCKS:
                """and building_conditions.replaceAirMethod != BuildingCondition.ALL_AIR_PLACEMENT"""
                if air_block in block_name:
                    return

            zones.append([x, z, x, z])

        for x in range(self.size[0]):
            for z in range(self.size[2]):
                computeBlockAt(x, z)

        return zones
