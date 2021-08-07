import utils.projectMath as projectMath
import utils.util as util
from generation.structures.baseStructure import *

from nbt import nbt

"""
Structure using nbt
"""
class Structures(BaseStructure):
    REPLACEMENTS = "replacements"
    CHANGE = "Change"
    CHANGE_TO = "ChangeTo"
    CHANGE_STATE = "ChangeState"
    CHANGE_ORIGINAL_BLOCK = "OriginalBlock"
    CHANGE_REPLACEMENT_WORD = "ReplacementWord"
    CHANGE_EXCLUDED_ZONES = "ExcludedZone"

    REPLACEMENTS_EXCLUSIF = {
        "oak" : "dark_oak"
    }

    """
    Constructor of the class
    It will use the nbt file and mark it to indicate if the block in palette should change with replacements in building condition
    """
    def __init__(self, nbtfile, info, name):
        super(BaseStructure, self).__init__()
        self.setInfo(info)

        self.setSize([nbtfile["size"][0].value, nbtfile["size"][1].value, nbtfile["size"][2].value])
        self.file = nbtfile
        self.name = name

        # Variable used on building
        self.placeImmediately = False

        self.computedOrientation = {}
        # Indicate for each block in palette if it should change or not and to change to what
        for block in self.file["palette"]:
            if Structures.REPLACEMENTS in self.info.keys():
                blockName = block["Name"].value.split("[")[0]

                for replacementWord in self.info[Structures.REPLACEMENTS].keys():
                    # Checking for block replacement
                    if replacementWord == blockName:
                        block.tags.append(nbt.TAG_Int(name=Structures.CHANGE_STATE, value=self.info[Structures.REPLACEMENTS][blockName]["state"]))
                                                                        #  """AND states equals"""
                        if block[Structures.CHANGE_STATE].value == 1 or (block[Structures.CHANGE_STATE].value == 0):
                            block.tags.append(nbt.TAG_Byte(name=Structures.CHANGE, value=True))
                            block.tags.append(nbt.TAG_String(name=Structures.CHANGE_TO, value=self.info[Structures.REPLACEMENTS][block["Name"].value]["type"]))   
                            block.tags.append(nbt.TAG_String(name=Structures.CHANGE_ORIGINAL_BLOCK, value=block["Name"].value))
                            block.tags.append(nbt.TAG_String(name=Structures.CHANGE_REPLACEMENT_WORD, value=replacementWord))
                            block.tags.append(nbt.TAG_Byte(name=Structures.CHANGE_EXCLUDED_ZONES, 
                                value=("excluded" in self.info[Structures.REPLACEMENTS][replacementWord].keys())))
                            break
                        
                    # Checking for substr replacement 
                    elif replacementWord in blockName:
                        # The replacementWord can be in unexpected blocks
                        # "oak" is on every "...dark_oak..." block
                        if replacementWord in Structures.REPLACEMENTS_EXCLUSIF:
                            if Structures.REPLACEMENTS_EXCLUSIF[replacementWord] in blockName:
                                continue

                        if replacementWord in self.info[Structures.REPLACEMENTS].keys():
                            if self.info[Structures.REPLACEMENTS][replacementWord]["state"] == 2:

                                block.tags.append(nbt.TAG_Byte(name=Structures.CHANGE, value=True))
                                block.tags.append(nbt.TAG_String(name=Structures.CHANGE_TO, value=self.info[Structures.REPLACEMENTS][replacementWord]["type"]))  
                                block.tags.append(nbt.TAG_Int(name=Structures.CHANGE_STATE, value=2))
                                block.tags.append(nbt.TAG_String(name=Structures.CHANGE_ORIGINAL_BLOCK, value=(block["Name"].value) ))
                                block.tags.append(nbt.TAG_String(name=Structures.CHANGE_REPLACEMENT_WORD, value=replacementWord))

                                # True or False
                                block.tags.append(nbt.TAG_Byte(name=Structures.CHANGE_EXCLUDED_ZONES, 
                                    value=("excluded" in self.info[Structures.REPLACEMENTS][replacementWord].keys())))
                                break
                                
            
            block.tags.append(nbt.TAG_Byte(name=Structures.CHANGE, value=False))
        
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
    def getNextBuildingInformation(self, flip, rotation):
        info = {}
        info["entry"] = { 
            "position" : self.info["mainEntry"]["position"].copy(), 
            "facing" : self.getFacingMainEntry(flip, rotation) }
        info["size"] = self.size
        info["corner"] = self.getCornersLocalPositions(self.info["mainEntry"]["position"].copy(), flip, rotation)

        return info


    def build(self, worldModif, buildingCondition, chestGeneration):
        ## Pre computing :
        buildingCondition["referencePoint"] = buildingCondition["referencePoint"].copy()
        self.computeOrientation(buildingCondition["rotation"], buildingCondition["flip"])

        if buildingCondition["flip"] == 1 or buildingCondition["flip"] == 3:
            buildingCondition["referencePoint"][0] = self.size[0] - 1 - buildingCondition["referencePoint"][0] 
        if buildingCondition["flip"] == 2 or buildingCondition["flip"] == 3:
            buildingCondition["referencePoint"][2] = self.size[2] - 1 - buildingCondition["referencePoint"][2] 

        # Replace bloc by these given
        for blockPalette in self.file["palette"]:
            if blockPalette[Structures.CHANGE].value:
                changeState = blockPalette[Structures.CHANGE_STATE].value

                if changeState == 0 or changeState == 1:
                    blockPalette["Name"].value = buildingCondition["replacements"][blockPalette[Structures.CHANGE_TO].value].split("[")[0]
                elif changeState == 2:
                    blockPalette["Name"].value = blockPalette[Structures.CHANGE_ORIGINAL_BLOCK].value.replace(
                        blockPalette[Structures.CHANGE_REPLACEMENT_WORD].value, 
                        buildingCondition["replacements"][blockPalette[Structures.CHANGE_TO].value].split("[")[0] )

        
        # Place support underHouse
        self.placeSupportUnderStructure(worldModif, buildingCondition)

        # Air zone
        self.placeAirZones(worldModif, buildingCondition)
        
        ## Computing : Modify from blocks
        for block in self.file["blocks"]:
            blockPalette = self.file["palette"][block["state"].value] 
            self.placeImmediately = False

            # Check if the current block is in excluded zone
            takeOriginalBlock = False
            blockName = blockPalette["Name"].value
            if (blockPalette[Structures.CHANGE].value):
                if (blockPalette[Structures.CHANGE_EXCLUDED_ZONES].value):
                    for zone in self.info["replacements"][blockPalette[Structures.CHANGE_REPLACEMENT_WORD].value]["excluded"] :
                        if projectMath.isPointInSquare([ block["pos"][0].value, block["pos"][1].value, block["pos"][2].value], zone) :
                            takeOriginalBlock = True
                            blockName = blockPalette[Structures.CHANGE_ORIGINAL_BLOCK].value
                            break


            # Check for block air replacement
            if blockName in Structures.AIR_BLOCKS and buildingCondition["replaceAllAir"] != 1:
                continue
            
            # Compute position of block from local space to world space
            blockPosition = self.returnWorldPosition(
                [ block["pos"][0].value, block["pos"][1].value + 1, block["pos"][2].value ],
                buildingCondition["flip"], buildingCondition["rotation"], 
                buildingCondition["referencePoint"], buildingCondition["position"] )
            
            self.checkBeforePlacing(blockName)
            theBlock = self.convertNbtBlockToStr(
                    self.file["palette"][block["state"].value],
                    takeOriginalBlock
                    )      

            worldModif.setBlock( 
                blockPosition[0], blockPosition[1], blockPosition[2],
               theBlock , placeImmediately=self.placeImmediately
            )

            self.checkAfterPlacing(block, blockName, blockPosition, chestGeneration, buildingCondition)

        # Place sign
        if "sign" in self.info.keys():
            signPosition = self.returnWorldPosition(
                self.info["sign"]["position"],
                buildingCondition["flip"], buildingCondition["rotation"], 
                buildingCondition["referencePoint"], buildingCondition["position"]
            )
            signPosition[1] += 1

            self.generateSignatureSign(signPosition, worldModif, buildingCondition["replacements"]["woodType"], buildingCondition["villager"])

        self.parseSpecialRule(buildingCondition, worldModif)
            

    def checkBeforePlacing(self, blockName):
        if "chest" in blockName or "shulker" in blockName or "lectern" in blockName or "barrel" in blockName:
            self.placeImmediately = True


    def checkAfterPlacing(self, block, blockName, blockPosition, chestGeneration, buildingCondition):
        # If structure has loot tables and chest encounter
        if "chest" in blockName or "barrel" in blockName:
            if not "lootTables" in self.info: 
                return
                
            if self.lootTable :
                choosenLootTable = ""
                for lootTable in self.info["lootTables"] :
                    if len(lootTable) == 1:
                        choosenLootTable = lootTable[0]
                    elif projectMath.isPointInCube([ block["pos"][0].value, block["pos"][1].value, block["pos"][2].value ], lootTable[1]) :
                        choosenLootTable = lootTable[0]
                    
                if choosenLootTable  != "":
                    additionalObjects = []
                    if choosenLootTable in buildingCondition["special"].keys():
                        additionalObjects = buildingCondition["special"][choosenLootTable]

                    chestGeneration.generate(blockPosition[0], blockPosition[1], blockPosition[2], choosenLootTable, buildingCondition["replacements"], additionalObjects)

        if "lectern" in blockName:
            if not "lectern" in self.info:
                return

            for key in self.info["lectern"].keys():
                position = self.info["lectern"][key]
                if block["pos"][0].value == position[0] and block["pos"][1].value == position[1] and block["pos"][2].value == position[2]:
                    result = util.changeNameWithBalise(key, buildingCondition["replacements"])
                    if result[0] >= 0:
                        util.addBookToLectern(blockPosition[0], blockPosition[1], blockPosition[2], result[1])
                    else :
                        print("Can't add a book to a lectern at pos : " + str(blockPosition))
                    break


    def convertNbtBlockToStr(self, blockPalette, takeOriginalBlockName=False):
        if takeOriginalBlockName:
            block = blockPalette[Structures.CHANGE_ORIGINAL_BLOCK].value
        else:
            block = blockPalette["Name"].value

        property = "["
        if "Properties" in blockPalette.keys():
            for key in blockPalette["Properties"].keys():
                if self.propertyCompatible(block, key):
                    property += self.convertProperty(key, blockPalette["Properties"][key].value) + ","
  
            property = property[:-1] 
        block = block + property + "]"
        return block
