import time
from representation.village import Village
from representation.loreStructure import LoreStructure
from generation.data.murdererData import MurdererData
from generation.chestGeneration import ChestGeneration
from generation.structureManager import StructureManager
from generation.structures.blockTransformation.oldStructureTransformation import OldStructureTransformation
from generation.resources import Resources
from generation.floodFill import FloodFill
import generation.generator as generator
from utils.nameGenerator import NameGenerator
from utils.worldModification import WorldModification
from utils.constants import Constants

import generation.resourcesLoader as resLoader
import utils.util as util
import utils.argumentParser as argParser
import generation.loreMaker as loreMaker
import generation.road as road
import lib.interfaceUtils as interfaceUtil
import lib.toolbox as toolbox
import utils.book as book

import random

milliseconds = int(round(time.time() * 1000))

TIME_LIMIT: int = 600
TIME_TO_BUILD_A_VILLAGE: int = 30

file: str = "temp.txt"
interface: interfaceUtil.Interface = interfaceUtil.Interface()
interface.setCaching(True)
interface.setBuffering(True)
interfaceUtil.setCaching(True)
interfaceUtil.setBuffering(True)

world_modification: WorldModification = WorldModification(interface)
args, parser = argParser.giveArgsAndParser()
build_area = argParser.getBuildArea(args)

nameGenerator: NameGenerator = NameGenerator()

if build_area == -1:
    exit()

build_area: tuple = (build_area[0], build_area[1], build_area[2], build_area[3] - 1, build_area[4] - 1, build_area[5] - 1)
size_area: list = [build_area[3] - build_area[0] + 1, build_area[5] - build_area[2] + 1]

"""Generate village involving on our generation"""
print("Generate lore of the world")
villages: list = loreMaker.initializedVillages(7, nameGenerator)
villageInteractions: list = loreMaker.createVillageRelationAndAssign(villages)
loreMaker.checkForImpossibleInteractions(villages, villageInteractions)

settlement_index: int = 0
current_village: Village

block_transformation: list = [OldStructureTransformation()]

# Five main steps : init settlement Data, choose structures and find its positions, make road between these
# structures, and finally build structures.
if not args.remove:
    resources: Resources = Resources()
    resLoader.loadAllResources(resources)

    chest_generation: ChestGeneration = ChestGeneration(resources, interface)

    # Each zone for takes 500 blocks, division begin after 1000
    zone_number_x: int = int(size_area[0] / 500)
    if zone_number_x == 0:
        zone_number_x = 1

    zone_size_x = int(size_area[0] / zone_number_x)

    zone_number_z = int(size_area[1] / 500)
    if zone_number_z == 0:
        zone_number_z = 1
    zone_size_z = int(size_area[1] / zone_number_z)

    current_zone_x: int = 0
    current_zone_z: int = 0

    while current_zone_z < zone_number_z:
        current_time: int = int(round(time.time() * 1000)) - milliseconds

        if current_time / 1000 >= TIME_LIMIT - TIME_TO_BUILD_A_VILLAGE:
            print("Aboard immediately, not time to generate")
            current_zone_z = zone_number_z
            continue

        # Area of the local village
        area: list = [
            build_area[0] + current_zone_x * zone_size_x,
            build_area[1],
            build_area[2] + current_zone_z * zone_size_z,
            build_area[3] if current_zone_x == zone_number_x - 1 else build_area[0] + (
                    current_zone_x + 1) * zone_size_x,
            build_area[4],
            build_area[5] if current_zone_z == zone_number_z - 1 else build_area[2] + (
                    current_zone_z + 1) * zone_size_z]

        print("\n-------------\nBuild a village in subarea", area)
        current_zone_x += 1
        if current_zone_x >= zone_number_x:
            current_zone_z += 1
            current_zone_x = 0

        interfaceUtil.setBuildArea(area[0], area[1], area[2], area[3] + 1, area[4] + 1, area[5] + 1)
        print("Make global slice")
        interfaceUtil.makeGlobalSlice()
        print("Global slice done")

        current_village = villages[settlement_index]
        current_village.generated = True
        block_transformation[0].age = current_village.age

        """ First main step : init settlementData """
        settlementData = generator.createSettlementData(area, current_village, resources)

        floodFill = FloodFill(world_modification, settlementData)

        structureManager = StructureManager(settlementData, resources, nameGenerator)

        """ Second main step : choose structures and their position """
        i = 0
        while i < settlementData.structure_number_goal:
            print("Generate position " + str(i + 1) + "/" + str(settlementData.structure_number_goal) + "  ", end="\r")
            current_village.lore_structures.append(LoreStructure())
            # 0 -> normal, 1 -> replacement, 2 -> no more structure
            result: int = structureManager.chooseOneStructure()

            if result == 2:
                settlementData.structure_number_goal = i
                break

            if result == 1:
                settlementData.structure_number_goal -= 1
                continue

            current_village.lore_structures[i].generateAge(current_village)
            baseStructure = resources.structures[current_village.lore_structures[i].name]
            structureManager.printStructureChoose()

            corners: tuple = baseStructure.setupInfoAndGetCorners()
            result: dict = floodFill.findPosHouse(corners)

            if not result["validPosition"]:
                settlementData.structure_number_goal -= 1
                structureManager.removeLastStructure()
                floodFill.set_number_of_houses(settlementData.structure_number_goal)
                continue

            current_village.lore_structures[i].validePosition = result["validPosition"]

            current_village.lore_structures[i].position = result["position"]
            current_village.lore_structures[i].flip = result["flip"]
            current_village.lore_structures[i].rotation = result["rotation"]

            current_village.lore_structures[i].prebuildingInfo = baseStructure.getNextBuildingInformation(
                result["flip"],
                result["rotation"])

            # If new chunk discovered, add new resources
            chunk = [int(current_village.lore_structures[i].position[0] / 16),
                     int(current_village.lore_structures[i].position[2] / 16)]

            if chunk not in settlementData.discovered_chunks:
                structureBiomeId = util.getBiome(current_village.lore_structures[i].position[0],
                                                 current_village.lore_structures[i].position[2], 1, 1)
                structureBiomeName = resources.biomeMinecraftId[int(structureBiomeId)]
                structureBiomeBlockId = str(resources.biomesBlockId[structureBiomeName])

                settlementData.discovered_chunks.append(chunk)
                util.addResourcesFromChunk(resources, settlementData, structureBiomeBlockId)

            loreMaker.alterSettlementDataWithNewStructures(settlementData, current_village.lore_structures[i])

            current_time = int(round(time.time() * 1000)) - milliseconds

            if current_time / 1000 < TIME_LIMIT - TIME_TO_BUILD_A_VILLAGE:
                structureManager.checkDependencies()
                i += 1
            else:
                settlementData.structure_number_goal = i + 1
                floodFill.set_number_of_houses(settlementData.structure_number_goal)
                print("Abort finding position and adding structures due to time expired")
                break

        """ Third main step : creates lore of the village """
        print("\nGenerate lore of the village")

        # Murderer
        murdererData: MurdererData = current_village.murderer_data
        current_village.generateVillageLore()

        books: dict = generator.generateVillageBooks(settlementData, nameGenerator)
        generator.placeBooks(settlementData, books, world_modification)

        # Villager interaction
        for villager in current_village.villagers:
            available: bool = True
            structure: LoreStructure = current_village.lore_structures[0]

            for tested_structure in current_village.lore_structures:
                if villager in tested_structure.villagers:
                    available = "haybale" not in tested_structure.name
                    structure = tested_structure
                    break

            if random.randint(1, 3) == 1 and available:
                # print("Generate diary of " + settlementData["villagerNames"][i])
                villager.diary = book.createBookForVillager(settlementData.village_model, villager)

                villager.diary[0] = "minecraft:written_book" + toolbox.writeBook(
                    villager.diary[0],
                    title="Diary of " + villager.name, author=villager.name,
                    description="Diary of " + villager.name)

                if villager.diary[1] != "":
                    structure.gift = villager.diary[1]

        # Add books replacements
        settlementData.setMaterialReplacement("villageBook", "minecraft:written_book" + books["villageNameBook"])
        settlementData.setMaterialReplacement("villageLecternBook", books["villageNameBook"])
        settlementData.setMaterialReplacement("villagerRegistry", "minecraft:written_book" + books["villagerNamesBook"])
        settlementData.setMaterialReplacement("deadVillagerRegistry",
                                              "minecraft:written_book" + books["deadVillagersBook"])

        """ Fourth main step : creates the roads of the village """
        road.initRoad(floodFill.listHouse, settlementData, world_modification)

        """ Five main step : places every structure and after that every decorations """
        i: int = 0
        current_time: int = int(round(time.time() * 1000)) - milliseconds
        while i < len(current_village.lore_structures) and current_time / 1000 < TIME_LIMIT:
            print("Build structure " + str(i + 1) + "/" + str(settlementData.structure_number_goal) + "  ", end="\r")
            generator.generateStructure(current_village.lore_structures[i], settlementData, resources,
                                        world_modification, chest_generation, block_transformation)
            util.spawnVillagerForStructure(settlementData, current_village.lore_structures[i],
                                           current_village.lore_structures[i].position)
            current_time = int(round(time.time() * 1000)) - milliseconds
            i += 1

        world_modification.saveToFile(file)

        if i < len(current_village.lore_structures):
            print("\nAbort building due time expired")

        print("\nBuild decoration")
        floodFill.placeDecorations(settlementData)
        print("Position of lectern for village", current_zone_z * zone_number_x, ":", [settlementData.center[0],
                                                                                       Constants.getHeight(
                                                                                           settlementData.center[0],
                                                                                           settlementData.center[2]),
                                                                                       settlementData.center[1]])
        print("Position of first structure",
              [floodFill.listHouse[0][0], floodFill.listHouse[0][1], floodFill.listHouse[0][2]])
        # iu.runCommand("tp {} {} {}".format(floodFill.listHouse[0][0], floodFill.listHouse[0][1], floodFill.listHouse[0][2]))
        print("Time left :", TIME_LIMIT - (int(round(time.time() * 1000)) - milliseconds) / 1000, "s")

        settlement_index += 1

    interfaceUtil.setBuildArea(build_area[0], build_area[1], build_area[2], build_area[3] + 1, build_area[4] + 1,
                               build_area[5] + 1)
else:
    if args.remove == "r":
        world_modification.loadFromFile(file)
    else:
        world_modification.loadFromFile(args.remove)

    world_modification.undoAllModification()

milliseconds2: int = int(round(time.time() * 1000))
result: int = milliseconds2 - milliseconds

print("Time took : ", result / 1000)
