from generation.chestGeneration import ChestGeneration
from utils.worldModification import WorldModification
from generation.resources import Resources
from utils.nameGenerator import NameGenerator
from generation.structures.baseStructure import BaseStructure
from generation.data.settlementData import SettlementData
from representation.village import Village
from utils.constants import Constants

import generation.loreMaker as lore_maker
import utils.util as util
import utils.book as book
import lib.toolbox as toolbox

import math
import random
import copy


def createSettlementData(area: list, village_model: Village, resources: Resources) -> SettlementData:
    settlement_data:SettlementData = SettlementData(village_model)
    settlement_data.setArea(area)

    # Biome 
    settlement_data.setVillageBiome(util.getBiome(settlement_data.center[0], settlement_data.center[2], 1, 1), resources) # TODO get mean

    # Load replacements for structure biome
    for aProperty in resources.biomesBlocks[settlement_data.biome_block_id]:
        if aProperty in resources.biomesBlocks["rules"]["village"]:
            settlement_data.setMaterialReplacement(aProperty, resources.biomesBlocks[settlement_data.biome_block_id][aProperty])

    # Per default, chosen color is white
    lore_maker.fillSettlementDataWithColor(settlement_data, "white")
    
    settlement_data.structure_number_goal = random.randint(20, 70)

    return settlement_data


def generateBooks(settlementData:SettlementData, nameGenerator:NameGenerator) -> dict:
    # Create books for the village
    strVillagers:str = settlementData.villager_names[0] + " : " + settlementData.villager_profession[0] + ";"

    for i in range(1, len(settlementData.villager_names)):
        strVillagers += settlementData.villager_names[i] + " : " + settlementData.villager_profession[i] + ";"
    listOfVillagers: list = strVillagers.split(";")

    textVillagersNames = book.createTextForVillagersNames(listOfVillagers)
    textDeadVillagers = book.createTextForDeadVillagers(listOfVillagers, nameGenerator)
    settlementData.villagerDeadNames = textDeadVillagers[2]
    textVillagePresentationBook = book.createTextOfPresentationVillage(settlementData.village_model.name,
                                                                       settlementData.structure_number_goal, settlementData.structures, textDeadVillagers[1], listOfVillagers)
                
    settlementData.textOfBooks = [textVillagersNames, textDeadVillagers]
    
    books:dict = {}
    books["villageNameBook"] = toolbox.writeBook(textVillagePresentationBook, title="Village Presentation", author="Mayor", description="Presentation of the village")
    books["villagerNamesBook"] = toolbox.writeBook(textVillagersNames, title="List of all villagers", author="Mayor", description="List of all villagers")
    books["deadVillagersBook"] = toolbox.writeBook(textDeadVillagers[0], title="List of all dead villagers", author="Mayor", description="List of all dead villagers")

    return books


def initNumberHouse(x_size: int, z_size: int) -> tuple:
    minimal_number_of_house: int = int(math.sqrt(x_size * z_size) / 2.2)
    maximum_number_of_house: int = int(math.sqrt(x_size * z_size) / 1.8)

    return minimal_number_of_house, maximum_number_of_house


def placeBooks(settlement_data: SettlementData, books: dict, world_modification: WorldModification):
    items: list = []

    for key in books.keys():
        items += [["minecraft:written_book" + books[key], 1]]

    # Set a chest for the books and place the books in the chest
    world_modification.setBlock(settlement_data.center[0],
                                Constants.getHeight(settlement_data.center[0], settlement_data.center[2]),
                                settlement_data.center[2], "minecraft:chest[facing=east]", placeImmediately=True)

    util.addItemChest(settlement_data.center[0],
                      Constants.getHeight(settlement_data.center[0], settlement_data.center[2]),
                      settlement_data.center[2], items)


    # Set a lectern for the book of village presentation
    toolbox.placeLectern(
        settlement_data.center[0],
        Constants.getHeight(settlement_data.center[0], settlement_data.center[2]),
        settlement_data.center[2] + 1, books["villageNameBook"], world_modification, 'east')


def generateStructure(structureData:dict, settlementData:SettlementData, resources:Resources, worldModif:WorldModification, chestGeneration:ChestGeneration) -> None:
    #print(structureData["name"])
    #print(structureData["validPosition"])
    structure = resources.structures[structureData["name"]]
    info = structure.info

    buildMurdererCache = False
    
    buildingCondition = BaseStructure.createBuildingCondition() 
    murdererData = settlementData.murderer_data

    for index in structureData["villagersId"]:
        if index == murdererData.villagerIndex:
            if "murdererTrap" in info["villageInfo"].keys():
                buildMurdererCache = True

        buildingCondition["villager"].append(settlementData.villager_names[index])

    buildingCondition["flip"] = structureData["flip"]
    buildingCondition["rotation"] = structureData["rotation"]
    buildingCondition["position"] = structureData["position"]
    buildingCondition["replaceAllAir"] = 3
    buildingCondition["referencePoint"] = structureData["prebuildingInfo"]["entry"]["position"]
    buildingCondition["size"] = structureData["prebuildingInfo"]["size"]
    buildingCondition["prebuildingInfo"] = structureData["prebuildingInfo"]
    structureBiomeId = util.getBiome(buildingCondition["position"][0], buildingCondition["position"][2], 1, 1)
    structureBiomeName = resources.biomeMinecraftId[int(structureBiomeId)]
    structureBiomeBlockId = str(resources.biomesBlockId[structureBiomeName])

    if structureBiomeBlockId == "-1" :
        structureBiomeBlockId = settlementData.biome_block_id
    
    buildingCondition["replacements"] = settlementData.getMatRepDeepCopy()
    # Load block for structure biome
    for aProperty in resources.biomesBlocks[structureBiomeBlockId]:
        if aProperty in resources.biomesBlocks["rules"]["structure"]:
            buildingCondition["replacements"][aProperty] = resources.biomesBlocks[structureBiomeBlockId][aProperty]

    modifyBuildingConditionDependingOnStructure(buildingCondition, settlementData, structureData, structureData["name"])

    structure.build(worldModif,  buildingCondition, chestGeneration)
    
    """util.spawnVillagerForStructure(settlementData, structureData,
        [structureData["position"][0], 
         structureData["position"][1] + 1, 
         structureData["position"][2]])"""

    if buildMurdererCache:
        buildMurdererHouse(structureData, settlementData, resources, worldModif, chestGeneration, buildingCondition)

    if "gift" in structureData.keys():
        position = structureData["position"]
        position[1] = position[1] - structureData["prebuildingInfo"]["entry"]["position"][1]
        worldModif.setBlock(position[0], position[1], position[2], structureData["gift"])


def buildMurdererHouse(structureData:dict, settlementData:SettlementData, resources:Resources, 
        worldModif:WorldModification, chestGeneration:ChestGeneration, buildingCondition:dict):

    #print("Build a house hosting a murderer")
    structure = resources.structures[structureData["name"]]
    info = structure.info

    buildingCondition = copy.deepcopy(buildingCondition)
    buildingCondition["position"] = structure.returnWorldPosition(
            info["villageInfo"]["murdererTrap"], buildingCondition["flip"], buildingCondition["rotation"], 
             buildingCondition["referencePoint"], buildingCondition["position"])

    structureMurderer = resources.structures["murderercache"]
    buildingInfo = structureMurderer.setupInfoAndGetCorners()

    # Temporary
    buildingCondition["flip"] = 0
    buildingCondition["rotation"] = 0  

    buildingInfo = structureMurderer.getNextBuildingInformation( buildingCondition["flip"], buildingCondition["rotation"])
    buildingCondition["referencePoint"] = buildingInfo["entry"]["position"]
    buildingCondition["size"] = buildingInfo["size"]
    buildingCondition["flip"], buildingCondition["rotation"] = structureMurderer.returnFlipRotationThatIsInZone(buildingCondition["position"],
                                 buildingCondition["referencePoint"], settlementData.area)

    modifyBuildingConditionDependingOnStructure(buildingCondition, settlementData, { "type" : "decorations"}, "murderercache")

    structureMurderer.build(worldModif, buildingCondition, chestGeneration)
    facing = structureMurderer.getFacingMainEntry(buildingCondition["flip"], buildingCondition["rotation"])

    # Generate murderer trap
    worldModif.setBlock(buildingCondition["position"][0], buildingCondition["position"][1] + 2, buildingCondition["position"][2], "minecraft:ladder[facing=" + facing + "]")
    worldModif.setBlock(buildingCondition["position"][0], buildingCondition["position"][1] + 3, buildingCondition["position"][2], 
        "minecraft:" + buildingCondition["replacements"]["woodType"] + "_trapdoor[half=bottom,facing=" + facing  +"]")



def modifyBuildingConditionDependingOnStructure(buildingCondition:dict, settlementData:SettlementData, structureData:dict, structureName:str):
    if structureName == "basicgraveyard":
        number = 8

        buildingCondition["special"] = { "sign" : [] }

        listOfDead = settlementData.villagerDeadNames.copy()
        i = 0
        while i < number:
            buildingCondition["special"]["sign"].append("")
            buildingCondition["special"]["sign"].append("")
            buildingCondition["special"]["sign"].append("")
            buildingCondition["special"]["sign"].append("")

            if len(listOfDead) > 0:
                index = random.randint(0, len(listOfDead) -1 )
                name = listOfDead[index]
                util.parseVillagerNameInLines([name], buildingCondition["special"]["sign"], i * 4)

                del listOfDead[index]

            i += 1

    elif structureName == "murderercache":
        murdererData = settlementData.murderer_data

        buildingCondition["special"] = { "sign" : ["Next target :", "", "", ""] }
        name = settlementData.villager_names[murdererData.villagerTargetIndex]
        util.parseVillagerNameInLines([name], buildingCondition["special"]["sign"], 1)

    elif structureName == "adventurerhouse":
        buildingCondition["special"]["adventurerhouse"] = [book.createBookForAdventurerHouse(buildingCondition["flip"])]


    if structureData["type"] == "houses":
        for villagerIndex in structureData["villagersId"]:
            if len(settlementData.villager_diaries[villagerIndex]) > 0 :
                if not "bedroomhouse" in buildingCondition["special"]:
                    buildingCondition["special"]["bedroomhouse"] = []

                buildingCondition["special"]["bedroomhouse"].append(settlementData.villager_diaries[villagerIndex][0])
                #print("add diary of", settlementData["villagerNames"][villagerIndex])


def returnVillagerAvailableForGift(settlementData:SettlementData, exceptions:tuple):
    available = []
    for structureData in settlementData.structures:
        if not "gift" in structureData.keys():
            for index in structureData["villagersId"]:
                if not index in exceptions:
                    available.append(index)

    return available