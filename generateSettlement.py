import time
from generation.data.village import Village
from generation.data.villager import Villager
from generation.data.trade import Trade
from generation.data.loreStructure import LoreStructure
from generation.chestGeneration import ChestGeneration
from generation.structureManager import StructureManager
from generation.structures.blockTransformation.oldStructureTransformation import OldStructureTransformation
from generation.structures.blockTransformation.damagedStructureTransformation import DamagedStructureTransformation
from generation.structures.blockTransformation.burnedStructureTransformation import BurnedStructureTransformation
from generation.structures.blockTransformation.abandonedStructureTransformation import AbandonedStructureTransformation
from generation.resources import Resources
from generation.floodFill import FloodFill
from generation.wallConstruction import WallConstruction
from generation.terrainModification import TerrainModification
from utils.nameGenerator import NameGenerator
from utils.worldModification import WorldModification
from utils.constants import Constants
from generation.road import Road
from utils.checkOrCreateConfig import Config

import generation.generator as generator
import generation.resourcesLoader as resLoader
import utils.util as util
import utils.book as book
import utils.projectMath as projectMath
import utils.argumentParser as argParser
import generation.loreMaker as loreMaker
import lib.interfaceUtils as interfaceUtil

import random

config: dict = Config.getOrCreateConfig()

milliseconds: int = int(round(time.time() * 1000))

TIME_LIMIT: int = Config.LOADED_CONFIG["timeLimit"]
TIME_TO_BUILD_A_VILLAGE: int = 30

file: str = "temp.txt"
interfaceUtil.setCaching(True)
interfaceUtil.setBuffering(True)

world_modification: WorldModification = WorldModification()
args, parser = argParser.giveArgsAndParser()
build_area = argParser.getBuildArea(args)

name_generator: NameGenerator = NameGenerator()

if build_area == -1:
    exit()

build_area: tuple = (
build_area[0], build_area[1], build_area[2], build_area[3] - 1, build_area[4] - 1, build_area[5] - 1)
size_area: list = [build_area[3] - build_area[0] + 1, build_area[5] - build_area[2] + 1]

# structures, and finally build structures.
if not args.remove:
    resources: Resources = Resources()
    resLoader.loadAllResources(resources)

    chest_generation: ChestGeneration = ChestGeneration(resources)

    # Each zone for takes 500 blocks, division begin after 1000
    defined_zone_size = [500, 500]
    settlement_zones_number: list = [size_area[0] // defined_zone_size[0], size_area[1] // defined_zone_size[1]]
    print("")
    print("Number of settlement :", settlement_zones_number[0] * settlement_zones_number[1])
    if settlement_zones_number[0] == 0:
        settlement_zones_number[0] = 1

    if settlement_zones_number[1] == 0:
        settlement_zones_number[1] = 1

    settlement_zones = projectMath.computeSquaredZoneWithNumber(settlement_zones_number, list(build_area))
    print("Settlement zones", settlement_zones)

    """Generate village involving on our generation"""
    print("Generate lore of the world")
    number_of_existing_village_in_lore = 7

    villages_positions: list = loreMaker.genPositionOfVillage(settlement_zones, number_of_existing_village_in_lore)

    villages: list = loreMaker.initializedVillages(villages_positions, name_generator)
    villageInteractions: list = loreMaker.createVillageRelationAndAssign(villages)

    loreMaker.checkForImpossibleInteractions(villages, villageInteractions)
    loreMaker.generateLoreAfterRelation(villages)

    settlement_index: int = 0
    current_village: Village

    block_transformation: list = [OldStructureTransformation(), DamagedStructureTransformation(),
                                  BurnedStructureTransformation(), AbandonedStructureTransformation()]
    current_zone_x: int = 0
    current_zone_z: int = 0

    position_of_villages_to_print: str = ""
    position_of_villages: list = []

    while current_zone_z < settlement_zones_number[1]:
        """ First main step : init settlement information """
        current_time: int = int(round(time.time() * 1000)) - milliseconds

        if current_time / 1000 >= TIME_LIMIT - TIME_TO_BUILD_A_VILLAGE:
            print("Aboard immediately, not time to generate")
            current_zone_z = settlement_zones_number[1]
            continue

        # Area of the local village
        area: list = settlement_zones[current_zone_z * settlement_zones_number[1] + current_zone_x]

        print("\n-------------\nBuild a village in subarea", area)
        current_zone_x += 1
        if current_zone_x >= settlement_zones_number[0]:
            current_zone_z += 1
            current_zone_x = 0

        current_village = villages[settlement_index]
        print("\nMake village named " + current_village.name)
        interfaceUtil.setBuildArea(area[0], area[1], area[2], area[3] + 1, area[4] + 1, area[5] + 1)

        print("Make global slice")
        interfaceUtil.makeGlobalSlice()
        """print(interfaceUtil.globalWorldSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"][128, 128])
        print(util.getHighestNonAirBlock(area[0] + 128, area[2] + 128, 128, 128))
        print(area[0] + 128, area[2] + 128)
        exit()"""

        print("Global slice done")
        print("Tier : " + str(current_village.tier) + ", Age : " + str(
            current_village.age) + ", Status : " + current_village.status)

        print("Village color : " + current_village.color)
        print("Village destroyed : " + str(current_village.isDestroyed))

        from generation.data.villageInteraction import VillageInteraction

        best_relation: int = VillageInteraction.STATE_WAR
        for interactionKey in current_village.village_interactions.keys():
            interaction = current_village.village_interactions[interactionKey]

            if VillageInteraction.isBestRelationThen(interaction.state, best_relation):
                best_relation = interaction.state

        print("Best relation : " + VillageInteraction.relationStateToStr(best_relation))

        current_village.generated = True
        block_transformation[0].age = current_village.age

        settlement_data = generator.createSettlementData(area, current_village, resources)
        loreMaker.applyLoreToSettlementData(settlement_data)

        floodFill = FloodFill(world_modification, settlement_data)

        structureManager = StructureManager(settlement_data, resources, name_generator)

        wallConstruction: WallConstruction = WallConstruction(current_village, 9)
        wallConstruction.setConstructionZone(area)

        terrain_modification: TerrainModification = TerrainModification(area, wallConstruction)

        """ Second main step : choose structures and their position """
        i = 0
        while i < settlement_data.structure_number_goal:
            print("Generate position " + str(i + 1) + "/" + str(settlement_data.structure_number_goal) + "  ")
            current_village.lore_structures.append(LoreStructure())
            # 0 -> normal, 1 -> replacement, 2 -> no more structure
            result: int = structureManager.chooseOneStructure()

            if result == 2:
                settlement_data.structure_number_goal = i
                break

            if result == 1:
                settlement_data.structure_number_goal -= 1
                continue

            current_village.lore_structures[i].generateAge(current_village)
            baseStructure = resources.structures[current_village.lore_structures[i].name]

            corners: tuple = baseStructure.setupInfoAndGetCorners()
            result: dict = floodFill.findPosHouse(corners)

            if not result["validPosition"]:
                settlement_data.structure_number_goal -= 1
                structureManager.removeLastStructure()
                floodFill.set_number_of_houses(settlement_data.structure_number_goal)
                continue

            current_village.lore_structures[i].validePosition = result["validPosition"]

            current_village.lore_structures[i].position = result["position"]
            current_village.lore_structures[i].flip = result["flip"]
            current_village.lore_structures[i].rotation = result["rotation"]

            current_village.lore_structures[i].preBuildingInfo = baseStructure.getNextBuildingInformation(
                result["flip"],
                result["rotation"])

            # If new chunk discovered, add new resources
            chunk = [int(current_village.lore_structures[i].position[0] / 16),
                     int(current_village.lore_structures[i].position[2] / 16)]

            if chunk not in settlement_data.discovered_chunks:
                structure_biome_id = util.getBiome(current_village.lore_structures[i].position[0],
                                                   current_village.lore_structures[i].position[2], 1, 1)
                structure_biome_name = resources.biomeMinecraftId[int(structure_biome_id)]
                structure_biome_block_id = str(resources.biomesBlockId[structure_biome_name])

                settlement_data.discovered_chunks.append(chunk)
                util.addResourcesFromChunk(resources, settlement_data, structure_biome_block_id)

            loreMaker.alterSettlementDataWithNewStructures(settlement_data, current_village.lore_structures[i])

            current_time = int(round(time.time() * 1000)) - milliseconds

            if current_time / 1000 < TIME_LIMIT - TIME_TO_BUILD_A_VILLAGE:
                structureManager.checkDependencies()
                i += 1
            else:
                settlement_data.structure_number_goal = i + 1
                floodFill.set_number_of_houses(settlement_data.structure_number_goal)
                print("Abort finding position and adding structures due to time expired")
                break

        structureManager.printStructureChoose()

        """ Third main step : creates lore of the village """
        print("\nGenerate lore of the village")

        loreMaker.generateLoreAfterAllStructure(current_village, name_generator)

        books: dict = generator.generateVillageBooks(settlement_data)
        # generator.placeBooks(settlement_data, books, world_modification)

        # Villager interaction
        for villager in current_village.villagers:
            available: bool = True
            structure: LoreStructure = current_village.lore_structures[0]

            for tested_structure in current_village.lore_structures:
                if villager in tested_structure.villagers and tested_structure.group == LoreStructure.TYPE_HOUSES:
                    available = "haybale" not in tested_structure.name
                    structure = tested_structure
                    break

            if (random.randint(1,
                               10) <= 9 or villager == settlement_data.village_model.murderer_data.fakeVillagerMurderer) and available:
                print("Generate diary of " + villager.name)
                villager.diary = book.createBookForVillager(settlement_data.village_model, villager)
                villager.diary[0].setInfo(title="Diary of " + villager.name, author=villager.name,
                                          description="Diary of " + villager.name)

                villager.diary[0] = "minecraft:written_book" + villager.diary[0].printBook()

                if villager.diary[1] != "":
                    structure.gift = villager.diary[1]

        # Add books replacements
        settlement_data.setVillageBook(books)

        for villager in current_village.villagers:
            if villager.job == Villager.DEFAULT_JOB:
                continue

            Trade.generateFromTradeTable(current_village, villager, resources.trades[villager.job],
                                         settlement_data.getMatRepDeepCopy())

        """ Fourth main step : creates the roads and wall of the village """
        print("\nInitialized road")
        road = Road(area)
        roadParts: list = road.initRoad(floodFill.structures, settlement_data)

        for lore_structure in current_village.lore_structures:
            wallConstruction.addRectangle([
                lore_structure.position[0] + lore_structure.preBuildingInfo["corner"][0],
                lore_structure.position[2] + lore_structure.preBuildingInfo["corner"][1],
                lore_structure.position[0] + lore_structure.preBuildingInfo["corner"][2],
                lore_structure.position[2] + lore_structure.preBuildingInfo["corner"][3]
            ])

        for roadData in roadParts:
            for blockPath in roadData.path:
                wallConstruction.addPoints(blockPath)

        print("\nCompute wall")
        wallType: int = WallConstruction.BOUNDING_CONVEX_HULL if Config.LOADED_CONFIG[
                                                                     "villageWall"] == "convexHull" else WallConstruction.BOUNDING_RECTANGULAR
        wallConstruction.computeWall(wallType)

        if Config.LOADED_CONFIG["shouldShowWallSchematic"]:
            wallConstruction.showImageRepresenting()

        i: int = 0
        print("Generate air zone")
        while i < len(current_village.lore_structures):
            generator.makeAirZone(current_village.lore_structures[i], settlement_data, resources,
                                  world_modification, terrain_modification)
            i += 1

        wallConstruction.placeAirZone(settlement_data, resources, world_modification, terrain_modification)

        """ Five main step : places every structure and after that every decorations """
        print("\nConstruct wall")

        wallConstruction.placeWall(settlement_data, resources, floodFill.computeCenter(), world_modification,
                                   block_transformation, terrain_modification)

        # Connect entry of village in wall to rest of village paths
        wallEntries: list = wallConstruction.returnWallEntries()
        mayorPosition = [roadParts[0].path[0][0], roadParts[0].yEntry1, roadParts[0].path[0][1]]
        mayorStruct: LoreStructure = roadParts[0].structure_ref_1
        for roadData in roadParts:
            if "townhall" in roadData.structure_ref_1.name:
                mayorPosition = [roadData.path[0][0], roadData.yEntry1, roadData.path[0][1]]
                mayorStruct = roadData.structure_ref_1
                break

        for entry in wallEntries:
            road.addRoad(entry, mayorPosition, mayorStruct, mayorStruct)

        print("\nConstruct road")
        road.generateRoad(world_modification, floodFill.structures, settlement_data, terrain_modification)

        i = 0
        print("\nBuild structure")
        current_time: int = int(round(time.time() * 1000)) - milliseconds
        while i < len(current_village.lore_structures) and current_time / 1000 < TIME_LIMIT:
            generator.generateStructure(current_village.lore_structures[i], settlement_data, resources,
                                        world_modification, chest_generation, block_transformation,
                                        terrain_modification)
            if not current_village.lore_structures[i].destroyed:
                util.spawnVillagerForStructure(settlement_data, current_village.lore_structures[i],
                                               current_village.lore_structures[i].position)

            current_time = int(round(time.time() * 1000)) - milliseconds
            i += 1

        if i < len(current_village.lore_structures):
            print("\nAbort building due time expired")

        print("\nBuild decoration")
        if not current_village.isDestroyed:
            floodFill.placeDecorations(settlement_data, road, wallConstruction)

        position_of_villages_to_print += "\nPosition of first structure " + str(
            [floodFill.structures[0][0], floodFill.structures[0][1], floodFill.structures[0][2]])

        position_of_villages.append([floodFill.structures[0][0], floodFill.structures[0][1], floodFill.structures[0][2]])

        # iu.runCommand("tp {} {} {}".format(floodFill.listHouse[0][0], floodFill.listHouse[0][1], floodFill.listHouse[0][2]))
        print("Time left :", TIME_LIMIT - (int(round(time.time() * 1000)) - milliseconds) / 1000, "s")

        settlement_index += 1

    interfaceUtil.setBuildArea(build_area[0], build_area[1], build_area[2], build_area[3] + 1, build_area[4] + 1, build_area[5] + 1)

    print(position_of_villages_to_print)
    generator.placeBook([build_area[0] + size_area[0] // 2, build_area[2] + size_area[1] // 2], [size_area[0] // 2, size_area[1] // 2], world_modification, position_of_villages)

else:
    if args.remove == "r":
        world_modification.loadFromFile(file)
    else:
        world_modification.loadFromFile(args.remove)

    world_modification.undoAllModification()

milliseconds2: int = int(round(time.time() * 1000))
result: int = milliseconds2 - milliseconds

world_modification.saveToFile(file)

print("Time took : ", result / 1000)
