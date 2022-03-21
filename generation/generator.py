from generation.chestGeneration import ChestGeneration
from generation.resources import Resources
from generation.structures.baseStructure import BaseStructure
from generation.data.settlementData import SettlementData
from representation.village import Village
from representation.loreStructure import LoreStructure
from representation.villager import Villager
from utils.constants import Constants
from utils.nameGenerator import NameGenerator
from utils.worldModification import WorldModification

import generation.loreMaker as lore_maker
import utils.util as util
import utils.book as book
import lib.toolbox as toolbox

import math
import random
import copy


def createSettlementData(area: list, village_model: Village, resources: Resources) -> SettlementData:
    settlement_data: SettlementData = SettlementData(village_model)
    settlement_data.setArea(area)

    # Biome 
    settlement_data.setVillageBiome(util.getBiome(settlement_data.center[0], settlement_data.center[2], 1, 1),
                                    resources)  # TODO get mean

    # Load replacements for structure biome
    for aProperty in resources.biomesBlocks[settlement_data.biome_block_id]:
        if aProperty in resources.biomesBlocks["rules"]["village"]:
            settlement_data.setMaterialReplacement(aProperty,
                                                   resources.biomesBlocks[settlement_data.biome_block_id][aProperty])

    # Per default, chosen color is white
    lore_maker.fillSettlementDataWithColor(settlement_data, "white")

    # settlement_data.structure_number_goal = 8
    settlement_data.structure_number_goal = random.randint(20, 40)

    return settlement_data


def generateVillageBooks(settlementData: SettlementData, nameGenerator: NameGenerator) -> dict:
    village_model: Village = settlementData.village_model

    # Create books for the village
    strVillagers: str = ""

    for villager in village_model.villagers:
        strVillagers += villager.name + " : " + villager.job + ";"

    listOfVillagers: list = strVillagers.split(";")

    textVillagersNames = book.createTextForVillagersNames(listOfVillagers)
    textDeadVillagers = book.createTextForDeadVillagers(listOfVillagers, nameGenerator)

    for name in textDeadVillagers[2]:
        dead_villager = Villager(village_model)
        dead_villager.name = name
        village_model.deadVillager.append(dead_villager)

    textVillagePresentationBook = book.createTextOfPresentationVillage(village_model.name,
                                                                       settlementData.structure_number_goal,
                                                                       village_model.lore_structures,
                                                                       textDeadVillagers[1],
                                                                       listOfVillagers)

    settlementData.textOfBooks = [textVillagersNames, textDeadVillagers]

    books: dict = {
        "villageNameBook": toolbox.writeBook(textVillagePresentationBook, title="Village Presentation", author="Mayor",
                                             description="Presentation of the village"),
        "villagerNamesBook": toolbox.writeBook(textVillagersNames, title="List of all villagers", author="Mayor",
                                               description="List of all villagers"),
        "deadVillagersBook": toolbox.writeBook(textDeadVillagers[0], title="List of all dead villagers", author="Mayor",
                                               description="List of all dead villagers")}

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


def generateStructure(lore_structure: LoreStructure, settlement_data: SettlementData, resources: Resources,
                      world_modification: WorldModification, chest_generation: ChestGeneration,
                      block_transformation: list) -> None:

    # print(structureData["name"])
    # print(structureData["validPosition"])
    block_transformation[0].age = lore_structure.age
    structure = resources.structures[lore_structure.name]
    info: dict = structure.info
    current_Village: Village = settlement_data.village_model

    buildMurdererCache = False

    buildingCondition = BaseStructure.createBuildingCondition()
    murdererData = current_Village.murderer_data

    for villager in current_Village.villagers:
        if villager == murdererData.villagerMurderer:
            if "murdererTrap" in info["villageInfo"].keys():
                buildMurdererCache = True

        buildingCondition["villager"].append(villager.name)

    buildingCondition["flip"] = lore_structure.flip
    buildingCondition["rotation"] = lore_structure.rotation
    buildingCondition["position"] = lore_structure.position
    buildingCondition["replaceAllAir"] = 3
    buildingCondition["referencePoint"] = lore_structure.prebuildingInfo["entry"]["position"]
    buildingCondition["size"] = lore_structure.prebuildingInfo["size"]
    buildingCondition["prebuildingInfo"] = lore_structure.prebuildingInfo
    structureBiomeId = util.getBiome(buildingCondition["position"][0], buildingCondition["position"][2], 1, 1)
    structureBiomeName = resources.biomeMinecraftId[int(structureBiomeId)]
    structureBiomeBlockId = str(resources.biomesBlockId[structureBiomeName])

    if structureBiomeBlockId == "-1":
        structureBiomeBlockId = settlement_data.biome_block_id

    buildingCondition["replacements"] = settlement_data.getMatRepDeepCopy()
    # Load block for structure biome
    for aProperty in resources.biomesBlocks[structureBiomeBlockId]:
        if aProperty in resources.biomesBlocks["rules"]["structure"]:
            buildingCondition["replacements"][aProperty] = resources.biomesBlocks[structureBiomeBlockId][aProperty]

    modifyBuildingConditionDependingOnStructure(buildingCondition, settlement_data, lore_structure)

    structure.build(world_modification, buildingCondition, chest_generation, block_transformation)

    """util.spawnVillagerForStructure(settlementData, structureData,
        [structureData["position"][0], 
         structureData["position"][1] + 1, 
         structureData["position"][2]])"""

    if buildMurdererCache:
        buildMurdererHouse(lore_structure, settlement_data, resources, world_modification, chest_generation,
                           buildingCondition, block_transformation)

    if lore_structure.gift != "Undefined":
        position = lore_structure.position
        position[1] = position[1] - lore_structure.prebuildingInfo["entry"]["position"][1]
        world_modification.setBlock(position[0], position[1], position[2], lore_structure.gift)


def buildMurdererHouse(lore_structure: LoreStructure, settlement_data: SettlementData, resources: Resources,
                       world_modification: WorldModification, chest_generation: ChestGeneration,
                       block_transformation: list,
                       building_conditions: dict):
    # print("Build a house hosting a murderer")
    structure = resources.structures[lore_structure.name]
    info = structure.info

    building_conditions = copy.deepcopy(building_conditions)
    building_conditions["position"] = structure.returnWorldPosition(
        info["villageInfo"]["murdererTrap"], building_conditions["flip"], building_conditions["rotation"],
        building_conditions["referencePoint"], building_conditions["position"])

    structureMurderer = resources.structures["murderercache"]
    buildingInfo = structureMurderer.setupInfoAndGetCorners()

    # Temporary
    building_conditions["flip"] = 0
    building_conditions["rotation"] = 0

    buildingInfo = structureMurderer.getNextBuildingInformation(building_conditions["flip"],
                                                                building_conditions["rotation"])
    building_conditions["referencePoint"] = buildingInfo["entry"]["position"]
    building_conditions["size"] = buildingInfo["size"]
    building_conditions["flip"], building_conditions["rotation"] = structureMurderer.returnFlipRotationThatIsInZone(
        building_conditions["position"],
        building_conditions["referencePoint"], settlement_data.area)

    lore_structure: LoreStructure = LoreStructure()
    lore_structure.name = "murderercache"
    lore_structure.type = "decorations"

    modifyBuildingConditionDependingOnStructure(building_conditions, settlement_data,
                                                lore_structure)

    structureMurderer.build(world_modification, building_conditions, chest_generation, block_transformation)
    facing = structureMurderer.getFacingMainEntry(building_conditions["flip"], building_conditions["rotation"])

    # Generate murderer trap
    world_modification.setBlock(building_conditions["position"][0], building_conditions["position"][1] + 2,
                                building_conditions["position"][2], "minecraft:ladder[facing=" + facing + "]")
    world_modification.setBlock(building_conditions["position"][0], building_conditions["position"][1] + 3,
                                building_conditions["position"][2],
                                "minecraft:" + building_conditions["replacements"][
                                    "woodType"] + "_trapdoor[half=bottom,facing=" + facing + "]")


def modifyBuildingConditionDependingOnStructure(buildingCondition: dict, settlementData: SettlementData,
                                                structure: LoreStructure):
    if structure.name == "basicgraveyard":
        number = 8

        buildingCondition["special"] = {"sign": []}

        listOfDead = settlementData.village_model.deadVillager.copy()
        i = 0
        while i < number:
            buildingCondition["special"]["sign"].append("")
            buildingCondition["special"]["sign"].append("")
            buildingCondition["special"]["sign"].append("")
            buildingCondition["special"]["sign"].append("")

            if len(listOfDead) > 0:
                index = random.randint(0, len(listOfDead) - 1)
                name = listOfDead[index].name
                util.parseVillagerNameInLines([name], buildingCondition["special"]["sign"], i * 4)

                del listOfDead[index]

            i += 1

    elif structure.name == "murderercache":
        murdererData = settlementData.village_model.murderer_data

        buildingCondition["special"] = {"sign": ["Next target :", "", "", ""]}
        name = murdererData.villagerTarget.name
        util.parseVillagerNameInLines([name], buildingCondition["special"]["sign"], 1)

    elif structure.name == "adventurerhouse":
        buildingCondition["special"]["adventurerhouse"] = [book.createBookForAdventurerHouse(buildingCondition["flip"])]

    if structure.type == "houses":
        for villager in settlementData.village_model.villagers:
            if len(villager.diary) > 0:
                if "bedroomhouse" not in buildingCondition["special"]:
                    buildingCondition["special"]["bedroomhouse"] = []

                buildingCondition["special"]["bedroomhouse"].append(villager.diary[0])
                # print("add diary of", settlementData["villagerNames"][villagerIndex])


def returnVillagerAvailableForGift(village_model: Village, villagers_excepted: list) -> list:
    available = []
    for structure in village_model.lore_structures:
        if structure.gift != "Undefined":
            for villager in village_model.villagers:
                if villager not in villagers_excepted:
                    available.append(villager)

    return available
