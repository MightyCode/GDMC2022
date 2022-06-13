from generation.chestGeneration import ChestGeneration
from generation.resources import Resources
from generation.structures.baseStructure import BaseStructure
from generation.data.settlementData import SettlementData
from generation.structures.buildingCondition import BuildingCondition
from generation.data.village import Village
from generation.data.loreStructure import LoreStructure
from utils.checkOrCreateConfig import Config
from utils.worldModification import WorldModification
from utils.bookWriter import BookWriter

import generation.loreMaker as loreMaker
import utils.util as util
import utils.book as book

import math
import random


def createSettlementData(area: list, village_model: Village, resources: Resources) -> SettlementData:
    settlement_data: SettlementData = SettlementData(village_model)
    settlement_data.init()
    settlement_data.setArea(area)

    # Biome 
    settlement_data.setVillageBiome(util.getBiome(settlement_data.center[0], settlement_data.center[2], 1, 1),
                                    resources)  # TODO get mean

    # Per default, chosen color is white
    loreMaker.fillSettlementDataWithColor(settlement_data, "white")

    # settlement_data.structure_number_goal = Config.getValueOrDefault("numberStructures", 8)
    settlement_data.structure_number_goal = Config.getValueOrDefault(
        "numberStructures",
        random.randint(Config.LOADED_CONFIG["minVillageStructure"], Config.LOADED_CONFIG["maxVillageStructure"]))

    return settlement_data


def generateVillageBooks(settlement_data: SettlementData) -> dict:
    village_model: Village = settlement_data.village_model

    # Create books for the village
    writer_village_presentation_book = book.createTextOfPresentationVillage(settlement_data)
    writer_village_presentation_book.setInfo(title="Village Presentation", author="Mayor",
                                             description="Presentation of the village")

    writer_villagers_names = book.createTextForVillagersNames(village_model.name, village_model.villagers)
    writer_villagers_names.setInfo(title="List of all villagers", author="Mayor",
                                   description="List of all villagers")

    writer_dead_villagers = book.createTextForDeadVillagers(village_model.name, village_model.villagers,
                                                            village_model.dead_villagers)
    writer_dead_villagers.setInfo(title="List of all dead villagers",
                                  author="Mayor",
                                  description="List of all dead villagers")

    return {
        "villageBook": writer_village_presentation_book.printBook(),
        "villagerNamesBook": writer_villagers_names.printBook(),
        "deadVillagersBook": writer_dead_villagers.printBook()
    }


def initNumberHouse(x_size: int, z_size: int) -> tuple:
    minimal_number_of_house: int = int(math.sqrt(x_size * z_size) / 2.2)
    maximum_number_of_house: int = int(math.sqrt(x_size * z_size) / 1.8)

    return minimal_number_of_house, maximum_number_of_house


def placeBook(position: list, local_position: list, world_modification: WorldModification, positions: list):
    items: list = []

    bookWriter: BookWriter = BookWriter()

    bookWriter.writeFirstPage("Position of villages", "")
    for i in range(len(positions)):
        bookWriter.writeLine("Village " + str(i) + " : " + str(positions[i]))
    bookWriter.setInfo("Village positions", "MightyCode")

    items += [["minecraft:written_book" + bookWriter.printBook(), 1]]

    # Set a chest for the books and place the books in the chest
    height: int = util.getHighestNonAirBlock(position[0], position[1], local_position[0], local_position[1])

    world_modification.setBlock(position[0], height + 20,
                                position[1], "minecraft:chest[facing=east]", place_immediately=True)

    util.addItemChest(position[0], height + 20, position[1], items)

    print("Chest with information at", position[0], height + 20, position[1])


def makeAirZone(lore_structure: LoreStructure, settlement_data: SettlementData, resources: Resources,
                world_modification: WorldModification, terrainModification):
    structure = resources.structures[lore_structure.name]

    building_conditions: BuildingCondition = structure.createBuildingCondition()
    building_conditions.setLoreStructure(lore_structure)

    building_conditions.replaceAirMethod = BuildingCondition.FILE_PREFERENCE_AIR_PLACEMENT
    building_conditions.replacements = settlement_data.getMatRepDeepCopy()

    structure.placeAirZones(world_modification, building_conditions, terrainModification)


def generateStructure(lore_structure: LoreStructure, settlement_data: SettlementData, resources: Resources,
                      world_modification: WorldModification, chest_generation: ChestGeneration,
                      block_transformations: list, terrainModification) -> None:
    # print(structureData["name"])
    # print(structureData["validPosition"])

    structure = resources.structures[lore_structure.name]
    current_village: Village = settlement_data.village_model

    build_murderer_cache: bool = False

    building_conditions: BuildingCondition = structure.createBuildingCondition()
    building_conditions.setLoreStructure(lore_structure)
    murderer_data = current_village.murderer_data

    for villager in lore_structure.villagers:
        if villager == murderer_data.villagerMurderer:
            if "murdererTrap" in structure.info["villageInfo"].keys():
                build_murderer_cache = True

    building_conditions.replaceAirMethod = BuildingCondition.FILE_PREFERENCE_AIR_PLACEMENT
    building_conditions.replacements = settlement_data.getMatRepDeepCopy()

    ### Get the biome to change environmental blocks, like the ground by those on the biome
    structure_biome_id = util.getBiome(building_conditions.position[0], building_conditions.position[2], 1, 1)
    structure_biome_name = resources.biomeMinecraftId[int(structure_biome_id)]
    structure_biome_block_id = str(resources.biomesBlockId[structure_biome_name])

    if structure_biome_block_id == "-1":
        structure_biome_block_id = settlement_data.biome_block_id

    # Load block for structure biome
    for aProperty in resources.biomesBlocks[structure_biome_block_id]:
        if aProperty in resources.biomesBlocks["rules"]["structure"]:
            building_conditions.replacements[aProperty] = resources.biomesBlocks[structure_biome_block_id][aProperty]

    modifyBuildingConditionDependingOnStructure(building_conditions, settlement_data, lore_structure)

    for block_transformation in block_transformations:
        block_transformation.setLoreStructure(lore_structure)

    structure.build(world_modification, building_conditions, chest_generation, block_transformations)

    if build_murderer_cache:
        buildMurdererCache(lore_structure, settlement_data, resources, world_modification, chest_generation,
                           block_transformations, building_conditions, terrainModification)

    if lore_structure.gift != "Undefined":
        position = lore_structure.position
        position[1] = position[1] - lore_structure.preBuildingInfo["entry"]["position"][1]
        world_modification.setBlock(position[0], position[1], position[2], lore_structure.gift)


def modifyBuildingConditionDependingOnStructure(building_conditions: BuildingCondition, settlement_data: SettlementData,
                                                structure: LoreStructure):
    if "graveyard" in structure.name:
        number = 8 if "medium" in structure.name else 5

        building_conditions.special = {"sign": []}

        list_of_dead = settlement_data.village_model.dead_villagers.copy()
        i = 0
        while i < number:
            building_conditions.special["sign"].append("")
            building_conditions.special["sign"].append("")
            building_conditions.special["sign"].append("")
            building_conditions.special["sign"].append("")

            if len(list_of_dead) > 0:
                index = random.randint(0, len(list_of_dead) - 1)
                name = list_of_dead[index].name
                util.parseVillagerNameInLines([name], building_conditions.special["sign"], i * 4)

                del list_of_dead[index]

            i += 1
    elif structure.name == "adventurerhouse":
        writer = book.createBookForAdventurerHouse(settlement_data.village_model.name, building_conditions.flip)
        writer.setInfo(title="Portal Manual", author="Mayor",
                       description="Contains useful instructions")
        building_conditions.special["guide"] = ["minecraft:written_book" + writer.printBook()]

    elif "exchanger" in structure.name:
        building_conditions.special["trade"] = []

        economical_relations: list = []

        for villageKey in settlement_data.village_model.village_interactions:
            interaction = settlement_data.village_model.village_interactions[villageKey]

            if interaction.economicalRelation:
                building_conditions.special["trade"].append(
                    'minecraft:paper{'
                    'display:{Name:\'{\"text\":\"Commercial alliance pact\"}\''
                    ',Lore:[\'{\"text\":\"' + villageKey.name + ' currency exchange permit.\"}\']'
                                                                '}, Enchantments:[{}]'
                                                                '}'
                )

                economical_relations.append(villageKey)

        building_conditions.special["sign"] = []

        resources: list = ["dirt", "wood", "metal", "dirt", "sand", "food"]
        villageName: str
        resource: str

        for i in range(6):
            if len(economical_relations) == 0:
                building_conditions.special["sign"].append("")
                building_conditions.special["sign"].append("------------")
                building_conditions.special["sign"].append("------------")
                building_conditions.special["sign"].append("")
            else:
                villageName = economical_relations[random.randint(0, len(economical_relations) - 1)].name
                resource = resources[random.randint(0, len(resources) - 1)]

                if random.randint(1, 2) == 1:
                    building_conditions.special["sign"].append(f'Selling {resource}')
                else:
                    building_conditions.special["sign"].append(f'Ordering {resource}')

                building_conditions.special["sign"].append("resources to")
                building_conditions.special["sign"].append(villageName)
                building_conditions.special["sign"].append(f'Cost: {random.randint(1, 5)} emeralds')

    elif "statue" in structure.name:
        building_conditions.special = {"sign": ["", "", "", "", "", "", "", ""]}
        index: int = 0
        if len(settlement_data.village_model.dead_villagers) > 1:
            index = random.randint(0, len(settlement_data.village_model.dead_villagers) - 1)

        name = settlement_data.village_model.dead_villagers[index].name
        util.parseVillagerNameInLines([
            "In tribute to " + name + ", hero who died in the war"
        ], building_conditions.special["sign"])

        if building_conditions.special["sign"][4] == "":
            building_conditions.special["sign"] = building_conditions.special["sign"][0:4]

    if structure.type == LoreStructure.TYPE_HOUSES:
        i: int = 0
        for villager in structure.villagers:
            if len(villager.diary) > 0:
                name: str = f'diary{i}'

                if name not in building_conditions.special:
                    building_conditions.special[name] = []

                building_conditions.special[name].append(villager.diary[0])

            i += 1

    if len(structure.orders) > 0:
        building_conditions.special["order"] = []

    for order in structure.orders:
        building_conditions.special["order"].append(
            'minecraft:paper{'
            'display:{Name:\'{\"text\":\"' + order.villager_ordering.name + '\\\'s order\"}\''
            # ',Lore:[\'{\"text\":\" currency exchange permit.\"}\']'
                                                                            '}, Enchantments:[{}]'
                                                                            '}'
        )

def buildMurdererCache(lore_structure: LoreStructure, settlement_data: SettlementData, resources: Resources,
                       world_modification: WorldModification, chest_generation: ChestGeneration,
                       block_transformation: list,
                       building_conditions_original: BuildingCondition, terrainModification):
    print("Build a house hosting a murderer")
    structure = resources.structures[lore_structure.name]
    info = structure.info

    building_conditions = building_conditions_original.__copy__()
    building_conditions.loreStructure.destroyed = False
    building_conditions.loreStructure.causeDestroy = {}
    building_conditions.position = structure.returnWorldPosition(
        info["villageInfo"]["murdererTrap"], building_conditions.flip, building_conditions.rotation,
        building_conditions.referencePoint, building_conditions.position)

    structure_murderer: BaseStructure = resources.structures["completemurderercache" if settlement_data.village_model.isDestroyed else "murderercache"]
    structure_murderer.setupInfoAndGetCorners()

    building_info = structure_murderer.getNextBuildingInformation(building_conditions.flip,
                                                                  building_conditions.rotation)
    building_conditions.referencePoint = building_info["entry"]["position"]
    building_conditions.size = building_info["size"]
    building_conditions.flip, building_conditions.rotation = structure_murderer.returnFlipRotationThatIsInZone(
        building_conditions.position,
        building_conditions.referencePoint, settlement_data.area)

    lore_structure: LoreStructure = LoreStructure()
    lore_structure.name = "completemurderercache" if settlement_data.village_model.isDestroyed else "murderercache"
    lore_structure.type = LoreStructure.TYPE_DECORATIONS

    if lore_structure.name == "murderercache":
        murderer_data = settlement_data.village_model.murderer_data

        building_conditions.special = {"sign": ["Next target :", "", "", ""]}
        name = murderer_data.villagerTarget.name
        util.parseVillagerNameInLines([name], building_conditions.special["sign"], 1)
    elif lore_structure.name == "completemurderercache":
        building_conditions.special = {
            "sign": ["Infiltre village", settlement_data.village_model.name + " : X", "Kill the mayor : X",
                     "Divulgate precious", " information : X", "Win the war : X", "", "", ""]}

    for transformation in block_transformation:
        transformation.setLoreStructure(lore_structure)

    structure_murderer.placeAirZones(world_modification, building_conditions.__copy__(), terrainModification)
    structure_murderer.build(world_modification, building_conditions, chest_generation, block_transformation)
    facing = structure_murderer.getFacingMainEntry(building_conditions.flip, building_conditions.rotation)

    # Generate murderer trap
    world_modification.setBlock(building_conditions.position[0], building_conditions.position[1] + 3,
                                building_conditions.position[2],
                                "minecraft:" + building_conditions.replacements[
                                    "woodType"] + "_trapdoor[half=bottom,facing=" + facing + "]")
    world_modification.setBlock(building_conditions.position[0], building_conditions.position[1] + 2,
                                building_conditions.position[2], "minecraft:ladder[facing=" + facing + "]")


def returnVillagerAvailableForGift(village_model: Village, villagers_excepted: list) -> list:
    available = []
    for structure in village_model.lore_structures:
        if structure.gift != "Undefined":
            for villager in village_model.villagers:
                if villager not in villagers_excepted:
                    available.append(villager)

    return available
