import utils.util as util
import utils.book as book
import lib.toolbox as toolbox
from generation.structures.baseStructure import BaseStructure
import generation.loremaker as loremaker
import math
import random
import copy

def createSettlementData(area, resources):
    settlementData = {}
    settlementData["area"] = area
    settlementData["center"] = [int((area[0] + area[3]) / 2) , 82, int((area[2] + area[5]) / 2)]
    settlementData["size"] = [area[3] - area[0] + 1, area[5] - area[2] + 1]
    settlementData["discoveredChunk"] = []

    # Materials replacement
    settlementData["materialsReplacement"] = {}

    # Biome 
    settlementData["biomeId"] = util.getBiome(settlementData["center"][0], settlementData["center"][2], 1, 1) # TODO get mean
    settlementData["biomeName"] = resources.biomeMinecraftId[int(settlementData["biomeId"])]
    settlementData["biomeBlockId"] = str(resources.biomesBlockId[settlementData["biomeName"]])
    if settlementData["biomeBlockId"] == "-1": 
        print("Generation on biome block id -1")
        settlementData["biomeBlockId"] = "0"

    # Load replaceements for structure biome
    for aProperty in resources.biomesBlocks[settlementData["biomeBlockId"]]:
        if aProperty in resources.biomesBlocks["rules"]["village"]:
            settlementData["materialsReplacement"][aProperty] = resources.biomesBlocks[settlementData["biomeBlockId"]][aProperty]

    # Per default, choosen color is white
    loremaker.fillSettlementDataWithColor(settlementData, "white")

    settlementData["villageName"] = book.generateVillageName()
    settlementData["materialsReplacement"]["villageName"] = settlementData["villageName"]

    settlementData["villagerNames"] = []
    settlementData["villagerProfession"] = []
    settlementData["villagerGameProfession"] = []
    settlementData["villagerProfessionList"] = [
                "farmer", "fisherman", "shepherd", "fletcher", "librarian", "cartographer", 
                "cleric", "armorer", "weaponsmith", "toolsmith", "butcher", "leatherworker", "mason", "nitwit"]

    # [0 -> content, 1 -> isGift]
    settlementData["villagerDiary"] = []
    
    settlementData["structuresNumberGoal"] = random.randint(20, 70)

    # structures contains "position", "rotation", "flip" "name", "type", "group", "villagersId", "gift"
    settlementData["structures"] = []
    settlementData["freeVillager"] = 0

    settlementData["woodResources"] = 0
    settlementData["dirtResources"] = 0
    settlementData["stoneResources"] = 0

    return settlementData


def generateBooks(settlementData):
    # Create books for the village
    strVillagers = settlementData["villagerNames"][0] + " : " + settlementData["villagerProfession"][0] + ";"
    for i in range(1, len(settlementData["villagerNames"])):
        strVillagers += settlementData["villagerNames"][i] + " : " + settlementData["villagerProfession"][i] + ";"
    listOfVillagers = strVillagers.split(";")

    textVillagersNames = book.createTextForVillagersNames(listOfVillagers)
    textDeadVillagers = book.createTextForDeadVillagers(listOfVillagers)
    settlementData["villagerDeadNames"] = textDeadVillagers[2]
    textVillagePresentationBook = book.createTextOfPresentationVillage(settlementData["villageName"], 
                settlementData["structuresNumberGoal"], settlementData["structures"], textDeadVillagers[1], listOfVillagers)
    settlementData["textOfBooks"] = [textVillagersNames, textDeadVillagers]
    
    books = {}
    books["villageNameBook"] = toolbox.writeBook(textVillagePresentationBook, title="Village Presentation", author="Mayor", description="Presentation of the village")
    books["villagerNamesBook"] = toolbox.writeBook(textVillagersNames, title="List of all villagers", author="Mayor", description="List of all villagers")
    books["deadVillagersBook"] = toolbox.writeBook(textDeadVillagers[0], title="List of all dead villagers", author="Mayor", description="List of all dead villagers")

    return books


def initnumberHouse(xSize, zSize):
    numberOhHousemin = math.isqrt(xSize * zSize)/ 2.2
    numberOhHousemax = math.isqrt(xSize * zSize)/ 1.8
    return numberOhHousemin, numberOhHousemax


def placeBooks(settlementData, books, floodFill, worldModif):
    items = []

    for key in books.keys():
        items += [["minecraft:written_book" + books[key], 1]]

    # Set a chest for the books and place the books in the chest
    worldModif.setBlock(settlementData["center"][0], 
                        floodFill.getHeight(settlementData["center"][0], settlementData["center"][2]), 
                        settlementData["center"][2], "minecraft:chest[facing=east]", placeImmediately=True)
    util.addItemChest(settlementData["center"][0], 
                        floodFill.getHeight(settlementData["center"][0], settlementData["center"][2]),
                        settlementData["center"][2], items)


    # Set a lectern for the book of village presentation
    toolbox.placeLectern(
        settlementData["center"][0], 
        floodFill.getHeight(settlementData["center"][0], settlementData["center"][2]), 
        settlementData["center"][2] + 1, books["villageNameBook"], worldModif, 'east')


def generateStructure(structureData, settlementData, resources, worldModif, chestGeneration):
    #print(structureData["name"])
    #print(structureData["validPosition"])
    structure = resources.structures[structureData["name"]]
    info = structure.info

    buildMurdererCache = False
    
    buildingCondition = BaseStructure.createBuildingCondition() 
    for index in structureData["villagersId"]:
        if index == settlementData["murdererIndex"]:
            if "murdererTrap" in info["villageInfo"].keys():
                buildMurdererCache = True

        buildingCondition["villager"].append(settlementData["villagerNames"][index])

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
        structureBiomeBlockId = settlementData["biomeBlockId"]    
    
    buildingCondition["replacements"] = copy.deepcopy(settlementData["materialsReplacement"])
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


def buildMurdererHouse(structureData, settlementData, resources, worldModif, chestGeneration, buildingCondition):
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
                                 buildingCondition["referencePoint"], settlementData["area"])

    modifyBuildingConditionDependingOnStructure(buildingCondition, settlementData, { "type" : "decorations"}, "murderercache")

    structureMurderer.build(worldModif, buildingCondition, chestGeneration)
    facing = structureMurderer.getFacingMainEntry(buildingCondition["flip"], buildingCondition["rotation"])

    # Generate murderer trap
    worldModif.setBlock(buildingCondition["position"][0], buildingCondition["position"][1] + 2, buildingCondition["position"][2], "minecraft:ladder[facing=" + facing + "]")
    worldModif.setBlock(buildingCondition["position"][0], buildingCondition["position"][1] + 3, buildingCondition["position"][2], 
        "minecraft:" + buildingCondition["replacements"]["woodType"] + "_trapdoor[half=bottom,facing=" + facing  +"]")



def modifyBuildingConditionDependingOnStructure(buildingCondition, settlementData, structureData, structureName):
    if structureName == "basicgraveyard":
        number = 8

        buildingCondition["special"] = { "sign" : [] }

        listOfDead = settlementData["villagerDeadNames"].copy()
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
        buildingCondition["special"] = { "sign" : ["Next target :", "", "", ""] }
        name = settlementData["villagerNames"][settlementData["murdererTargetIndex"]]
        util.parseVillagerNameInLines([name], buildingCondition["special"]["sign"], 1)

    elif structureName == "adventurerhouse":
        buildingCondition["special"]["adventurerhouse"] = [book.createBookForAdventurerHouse(buildingCondition["flip"])]


    if structureData["type"] == "houses":
        for villagerIndex in structureData["villagersId"]:
            if len(settlementData["villagerDiary"][villagerIndex]) > 0 :
                if not "bedroomhouse" in buildingCondition["special"]:
                    buildingCondition["special"]["bedroomhouse"] = []

                buildingCondition["special"]["bedroomhouse"].append(settlementData["villagerDiary"][villagerIndex][0])
                #print("add diary of", settlementData["villagerNames"][villagerIndex])


def returnVillagerAvailableForGift(settlementData, exception):
    available = []
    for structureData in settlementData["structures"]:
        if not "gift" in structureData.keys():
            for index in structureData["villagersId"]:
                if not index in exception:
                    available.append(index)

    return available