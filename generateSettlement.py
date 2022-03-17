import time
from generation.data.murdererData import MurdererData
from generation.chestGeneration import ChestGeneration
from generation.structureManager import StructureManager
from generation.resources import Resources
from generation.floodFill import FloodFill
from utils.constants import Constants
import generation.generator as generator
import generation.resourcesLoader as resLoader
import utils.util as util
from utils.nameGenerator import NameGenerator
from utils.worldModification import *
import utils.argumentParser as argParser
import generation.loremaker as loremaker
import generation.road as road
import lib.interfaceUtils as iu
import lib.toolbox as toolbox

import random

import utils.book as book
from representation.village import Village

milliseconds = int(round(time.time() * 1000))

TIME_LIMIT: int = 600
TIME_TO_BUILD_A_VILLAGE: int = 30

file: str = "temp.txt"
interface: interfaceUtils.Interface = interfaceUtils.Interface()
interface.setCaching(True)
interface.setBuffering(True)
iu.setCaching(True)
iu.setBuffering(True)
worldModif: WorldModification = WorldModification(interface)
args, parser = argParser.giveArgsAndParser()
buildArea = argParser.getBuildArea(args)

nameGenerator: NameGenerator = NameGenerator()

if buildArea == -1:
    exit()

buildArea: tuple = (buildArea[0], buildArea[1], buildArea[2], buildArea[3] - 1, buildArea[4] - 1, buildArea[5] - 1)
sizeArea: list = [buildArea[3] - buildArea[0] + 1, buildArea[5] - buildArea[2] + 1]

"""Generate village involving on our generation"""
villages: list = []
for i in range(7):
    villages.append(Village())
    villages[i].generateVillageInformation(nameGenerator)

settlementIndex: int = 0
currentVillage: Village

# Five main steps : init settlement Data, choose structures and find its positions, make road between these
# structures, and finally build structures.
if not args.remove:
    resources: Resources = Resources()
    resLoader.loadAllResources(resources)

    chestGeneration: ChestGeneration = ChestGeneration(resources, interface)

    # Each zone for takes 500 blocks, division begin after 1000
    numberZoneX: int = int(sizeArea[0] / 500)
    if numberZoneX == 0:
        numberZoneX = 1
    sizeZoneX = int(sizeArea[0] / numberZoneX)
    numberZoneZ = int(sizeArea[1] / 500)
    if numberZoneZ == 0:
        numberZoneZ = 1
    sizeZoneZ = int(sizeArea[1] / numberZoneZ)

    xAdvencement: int = 0
    zAdvencement: int = 0

    while zAdvencement < numberZoneZ:
        timeNow: int = int(round(time.time() * 1000)) - milliseconds

        if timeNow / 1000 >= TIME_LIMIT - TIME_TO_BUILD_A_VILLAGE:
            print("Abord immediatly not time to generate")
            zAdvencement = numberZoneZ
            continue

        # Area of the local village
        area: list = [
            buildArea[0] + xAdvencement * sizeZoneX,
            buildArea[1],
            buildArea[2] + zAdvencement * sizeZoneZ,
            buildArea[3] if xAdvencement == numberZoneX - 1 else buildArea[0] + (xAdvencement + 1) * sizeZoneX,
            buildArea[4],
            buildArea[5] if zAdvencement == numberZoneZ - 1 else buildArea[2] + (zAdvencement + 1) * sizeZoneZ]

        print("\n-------------\nBuild a village in subarea", area)
        xAdvencement += 1
        if xAdvencement >= numberZoneX:
            zAdvencement += 1
            xAdvencement = 0

        iu.setBuildArea(area[0], area[1], area[2], area[3] + 1, area[4] + 1, area[5] + 1)
        print("Make global slice")
        iu.makeGlobalSlice()
        print("Global slice done")

        currentVillage = villages[settlementIndex]

        """ First main step : init settlementData """
        settlementData = generator.createSettlementData(area, currentVillage, resources)

        floodFill = FloodFill(worldModif, settlementData)

        structureManager = StructureManager(settlementData, resources, nameGenerator)

        """ Second main step : choose structures and their position """
        i = 0
        while i < settlementData.structuresNumberGoal:
            print("Generate position " + str(i + 1) + "/" + str(settlementData.structuresNumberGoal) + "  ", end="\r")
            # 0 -> normal, 1 -> replacement, 2 -> no more structure
            result: int = structureManager.chooseOneStructure()

            if result == 2:
                settlementData.structuresNumberGoal = i
                break

            if result == 1:
                settlementData.structuresNumberGoal -= 1
                continue

            structure = resources.structures[settlementData.structures[i]["name"]]

            corners: tuple = structure.setupInfoAndGetCorners()

            result: dict = floodFill.findPosHouse(corners)

            if not result["validPosition"]:
                settlementData.structuresNumberGoal -= 1
                structureManager.removeLastStructure()
                floodFill.set_number_of_houses(settlementData.structuresNumberGoal)
                continue

            settlementData.structures[i]["validPosition"] = result["validPosition"]

            settlementData.structures[i]["position"] = result["position"]
            settlementData.structures[i]["flip"] = result["flip"]
            settlementData.structures[i]["rotation"] = result["rotation"]

            settlementData.structures[i]["prebuildingInfo"] = structure.getNextBuildingInformation(result["flip"],
                                                                                                   result["rotation"])

            # If new chunck discovererd, add new ressources
            chunk = [int(settlementData.structures[i]["position"][0] / 16),
                     int(settlementData.structures[i]["position"][2] / 16)]
            if not chunk in settlementData.discoveredChunks:
                structureBiomeId = util.getBiome(settlementData.structures[i]["position"][0],
                                                 settlementData.structures[i]["position"][2], 1, 1)
                structureBiomeName = resources.biomeMinecraftId[int(structureBiomeId)]
                structureBiomeBlockId = str(resources.biomesBlockId[structureBiomeName])

                settlementData.discoveredChunks.append(chunk)
                util.addResourcesFromChunk(resources, settlementData, structureBiomeBlockId)

            loremaker.alterSettlementDataWithNewStructures(settlementData, i)

            timeNow = int(round(time.time() * 1000)) - milliseconds

            if timeNow / 1000 < TIME_LIMIT - TIME_TO_BUILD_A_VILLAGE:
                structureManager.checkDependencies()
                i += 1
            else:
                settlementData.structuresNumberGoal = i + 1
                floodFill.set_number_of_houses(settlementData.structuresNumberGoal)
                print("Abort finding position and adding structures due to time expired")
                break

        """ Third main step : creates lore of the village """
        print("\nGenerate lore")

        # Murderer
        murdererData: MurdererData = settlementData.murdererData

        if len(settlementData.villagerNames) > 1:
            murdererData.villagerIndex = random.choice([i for i in range(0, len(settlementData.villagerNames)) if
                                                        settlementData.villagerProfession[i] != "Mayor"])

            murdererData.villagerTargetIndex = random.choice(
                [i for i in range(0, len(settlementData.villagerNames)) if i != murdererData.villagerIndex])

        for structureData in settlementData.structures:
            if murdererData.villagerTargetIndex in structureData["villagersId"]:
                structureData["gift"] = "minecraft:tnt"

        books: dict = generator.generateBooks(settlementData, nameGenerator)
        generator.placeBooks(settlementData, books, worldModif)

        # Villager interaction
        for i in range(len(settlementData.villagerNames)):
            settlementData.villagerDiary.append([])

            available: bool = True
            for structureData in settlementData.structures:
                if i in structureData["villagersId"]:
                    available = not "haybale" in structureData["name"]
                    break

            if random.randint(1, 3) == 1 and available:
                # print("Generate diary of " + settlementData["villagerNames"][i])
                settlementData.villagerDiary[i] = book.createBookForVillager(settlementData, i)
                settlementData.villagerDiary[i][0] = "minecraft:written_book" + toolbox.writeBook(
                    settlementData.villagerDiary[i][0],
                    title="Diary of " + settlementData.villagerNames[i], author=settlementData.villagerNames[i],
                    description="Diary of " + settlementData.villagerNames[i])
                if settlementData.villagerDiary[i][1] != "":
                    structureData["gift"] = settlementData.villagerDiary[i][1]

        # Add books replacements
        settlementData.setMaterialReplacement("villageBook", "minecraft:written_book" + books["villageNameBook"])
        settlementData.setMaterialReplacement("villageLecternBook", books["villageNameBook"])
        settlementData.setMaterialReplacement("villagerRegistry", "minecraft:written_book" + books["villagerNamesBook"])
        settlementData.setMaterialReplacement("deadVillagerRegistry",
                                              "minecraft:written_book" + books["deadVillagersBook"])

        """ Fourth main step : creates the roads of the village """
        road.initRoad(floodFill.listHouse, settlementData, worldModif)

        """ Five main step : places every structrure and after that every decorations """
        i: int = 0
        timeNow: int = int(round(time.time() * 1000)) - milliseconds
        while i < len(settlementData.structures) and timeNow / 1000 < TIME_LIMIT:
            print("Build structure " + str(i + 1) + "/" + str(settlementData.structuresNumberGoal) + "  ", end="\r")
            generator.generateStructure(settlementData.structures[i], settlementData, resources, worldModif,
                                        chestGeneration)
            util.spawnVillagerForStructure(settlementData, settlementData.structures[i],
                                           settlementData.structures[i]["position"])
            timeNow = int(round(time.time() * 1000)) - milliseconds
            i += 1

        worldModif.saveToFile(file)

        if i < len(settlementData.structures):
            print("\nAbort building due time expired")

        print("\nBuild decoration")
        floodFill.placeDecorations(settlementData)
        print("Position of lectern for village", zAdvencement * numberZoneX, ":", [settlementData.center[0],
                                                                                   Constants.getHeight(
                                                                                       settlementData.center[0],
                                                                                       settlementData.center[2]),
                                                                                   settlementData.center[1]])
        print("Position of first structure",
              [floodFill.listHouse[0][0], floodFill.listHouse[0][1], floodFill.listHouse[0][2]])
        # iu.runCommand("tp {} {} {}".format(floodFill.listHouse[0][0], floodFill.listHouse[0][1], floodFill.listHouse[0][2]))
        print("Time left :", TIME_LIMIT - (int(round(time.time() * 1000)) - milliseconds) / 1000, "s")

        settlementIndex += 1

    iu.setBuildArea(buildArea[0], buildArea[1], buildArea[2], buildArea[3] + 1, buildArea[4] + 1, buildArea[5] + 1)
else:
    if args.remove == "r":
        worldModif.loadFromFile(file)
    else:
        worldModif.loadFromFile(args.remove)

    worldModif.undoAllModification()

milliseconds2: int = int(round(time.time() * 1000))
result: int = milliseconds2 - milliseconds

print("Time took : ", result / 1000)
