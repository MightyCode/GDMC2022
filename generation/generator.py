from generation.chestGeneration import ChestGeneration
from generation.resources import Resources
from generation.structures.baseStructure import BaseStructure
from generation.data.settlementData import SettlementData
from generation.buildingCondition import BuildingCondition
from generation.data.village import Village
from generation.data.loreStructure import LoreStructure
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
    settlement_data.init()
    settlement_data.setArea(area)

    # Biome 
    settlement_data.setVillageBiome(util.getBiome(settlement_data.center[0], settlement_data.center[2], 1, 1), resources)  # TODO get mean

    # Per default, chosen color is white
    lore_maker.fillSettlementDataWithColor(settlement_data, "white")

    #settlement_data.structure_number_goal = 12
    settlement_data.structure_number_goal = random.randint(25, 55)

    return settlement_data


def generateVillageBooks(settlementData: SettlementData, nameGenerator: NameGenerator) -> dict:
    village_model: Village = settlementData.village_model

    # Create books for the village

    textVillagersNames = book.createTextForVillagersNames(village_model.villagers)
    textDeadVillagers = book.createTextForDeadVillagers(village_model.villagers, village_model.dead_villagers)

    textVillagePresentationBook = book.createTextOfPresentationVillage(village_model.name,
                                                                       settlementData.structure_number_goal,
                                                                       village_model.lore_structures,
                                                                       textDeadVillagers[1],
                                                                       village_model.villagers)

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
                      block_transformations: list) -> None:

    # print(structureData["name"])
    # print(structureData["validPosition"])
    for block_transformation in block_transformations:
        block_transformation.setLoreStructure(lore_structure)

    structure = resources.structures[lore_structure.name]
    info: dict = structure.info
    current_Village: Village = settlement_data.village_model

    build_murderer_cache: bool = False

    buildingCondition: BuildingCondition = BaseStructure.createBuildingCondition()
    buildingCondition.setLoreStructure(lore_structure)
    murdererData = current_Village.murderer_data

    for villager in lore_structure.villagers:
        if villager == murdererData.villagerMurderer:
            if "murdererTrap" in info["villageInfo"].keys():
                build_murderer_cache = True

    buildingCondition.replaceAirMethod = BuildingCondition.FILE_PREFERENCE_AIR_PLACEMENT
    buildingCondition.replacements = settlement_data.getMatRepDeepCopy()

    ### Get the biome to change environmental blocks, like the ground by those on the biome
    structureBiomeId = util.getBiome(buildingCondition.position[0], buildingCondition.position[2], 1, 1)
    structureBiomeName = resources.biomeMinecraftId[int(structureBiomeId)]
    structureBiomeBlockId = str(resources.biomesBlockId[structureBiomeName])

    if structureBiomeBlockId == "-1":
        structureBiomeBlockId = settlement_data.biome_block_id

    # Load block for structure biome
    for aProperty in resources.biomesBlocks[structureBiomeBlockId]:
        if aProperty in resources.biomesBlocks["rules"]["structure"]:
            buildingCondition.replacements[aProperty] = resources.biomesBlocks[structureBiomeBlockId][aProperty]

    modifyBuildingConditionDependingOnStructure(buildingCondition, settlement_data, lore_structure)

    structure.build(world_modification, buildingCondition, chest_generation, block_transformations)

    if build_murderer_cache:
        buildMurdererCache(lore_structure, settlement_data, resources, world_modification, chest_generation,
                           buildingCondition, block_transformations)

    if lore_structure.gift != "Undefined":
        position = lore_structure.position
        position[1] = position[1] - lore_structure.preBuildingInfo["entry"]["position"][1]
        world_modification.setBlock(position[0], position[1], position[2], lore_structure.gift)


def buildMurdererCache(lore_structure: LoreStructure, settlement_data: SettlementData, resources: Resources,
                       world_modification: WorldModification, chest_generation: ChestGeneration,
                       block_transformation: list,
                       building_conditions_original: BuildingCondition):
    print("Build a house hosting a murderer")
    structure = resources.structures[lore_structure.name]
    info = structure.info

    building_conditions = building_conditions_original.__copy__()
    building_conditions.position = structure.returnWorldPosition(
        info["villageInfo"]["murdererTrap"], building_conditions.flip, building_conditions.rotation,
        building_conditions.referencePoint, building_conditions.position)

    structureMurderer = resources.structures["murderercache"]
    structureMurderer.setupInfoAndGetCorners()

    buildingInfo = structureMurderer.getNextBuildingInformation(building_conditions.flip,
                                                                building_conditions.rotation)
    building_conditions.referencePoint = buildingInfo["entry"]["position"]
    building_conditions.size = buildingInfo["size"]
    building_conditions.flip, building_conditions.rotation = structureMurderer.returnFlipRotationThatIsInZone(
        building_conditions.position,
        building_conditions.referencePoint, settlement_data.area)

    lore_structure: LoreStructure = LoreStructure()
    lore_structure.name = "murderercache"
    lore_structure.type = LoreStructure.TYPE_DECORATIONS

    modifyBuildingConditionDependingOnStructure(building_conditions, settlement_data,
                                                lore_structure)

    structureMurderer.build(world_modification, building_conditions, chest_generation, block_transformation)
    facing = structureMurderer.getFacingMainEntry(building_conditions.flip, building_conditions.rotation)

    # Generate murderer trap
    world_modification.setBlock(building_conditions.position[0], building_conditions.position[1] + 2,
                                building_conditions.position[2], "minecraft:ladder[facing=" + facing + "]")
    world_modification.setBlock(building_conditions.position[0], building_conditions.position[1] + 3,
                                building_conditions.position[2],
                                "minecraft:" + building_conditions.replacements[
                                    "woodType"] + "_trapdoor[half=bottom,facing=" + facing + "]")


def modifyBuildingConditionDependingOnStructure(building_conditions: BuildingCondition, settlementData: SettlementData,
                                                structure: LoreStructure):
    if structure.name == "basicgraveyard":
        number = 8

        building_conditions.special = {"sign": []}

        listOfDead = settlementData.village_model.dead_villagers.copy()
        i = 0
        while i < number:
            building_conditions.special["sign"].append("")
            building_conditions.special["sign"].append("")
            building_conditions.special["sign"].append("")
            building_conditions.special["sign"].append("")

            if len(listOfDead) > 0:
                index = random.randint(0, len(listOfDead) - 1)
                name = listOfDead[index].name
                util.parseVillagerNameInLines([name], building_conditions.special["sign"], i * 4)

                del listOfDead[index]

            i += 1

    elif structure.name == "murderercache":
        murdererData = settlementData.village_model.murderer_data

        building_conditions.special = {"sign": ["Next target :", "", "", ""]}
        name = murdererData.villagerTarget.name
        util.parseVillagerNameInLines([name], building_conditions.special["sign"], 1)

    elif structure.name == "adventurerhouse":
        building_conditions.special["adventurerhouse"] = [book.createBookForAdventurerHouse(building_conditions.flip)]
    elif structure.name == "mediumstatue":
        building_conditions.special = {"sign": ["", "", "", "", "", "", "", ""]}
        index: int = 0
        if len(settlementData.village_model.dead_villagers) > 1:
            index = random.randint(0, len(settlementData.village_model.dead_villagers) - 1)

        name = settlementData.village_model.dead_villagers[index].name
        util.parseVillagerNameInLines([
            "In tribute to " + name + ", hero who died in the war"
        ], building_conditions.special["sign"])

        if building_conditions.special["sign"][4] == "":
            building_conditions.special["sign"] = building_conditions.special["sign"][0:4]

    if structure.type == LoreStructure.TYPE_HOUSES:
        for villager in settlementData.village_model.villagers:
            if len(villager.diary) > 0:
                if "bedroomhouse" not in building_conditions.special:
                    building_conditions.special["bedroomhouse"] = []

                building_conditions.special["bedroomhouse"].append(villager.diary[0])

                print(len(building_conditions.special["bedroomhouse"]))


def returnVillagerAvailableForGift(village_model: Village, villagers_excepted: list) -> list:
    available = []
    for structure in village_model.lore_structures:
        if structure.gift != "Undefined":
            for villager in village_model.villagers:
                if villager not in villagers_excepted:
                    available.append(villager)

    return available
