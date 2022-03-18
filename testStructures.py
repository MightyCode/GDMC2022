from importlib.resources import Resource
from generation.resources import *
from generation.chestGeneration import *
from generation.structures.structures import *
from generation.structureManager import *
from generation.floodFill import *
import generation.resourcesLoader as resLoader
import utils.util as util
from utils.worldModification import *
import utils.argumentParser as argParser
import lib.interfaceUtils as iu
import generation.loreMaker as loremaker
import utils.book as book
import lib.toolbox as toolbox
import copy

file:str = "temp.txt"
interface:interfaceUtils.Interface = interfaceUtils.Interface(buffering=True, caching = True)
interface.setCaching(True)
interface.setBuffering(True)
iu.setCaching(True)
iu.setBuffering(True)
worldModif:WorldModification = WorldModification(interface)
args, parser = argParser.giveArgsAndParser()
area:tuple = argParser.getBuildArea(args)

if area == -1:
    exit()

if not args.remove:
    resources:Resources = Resources()
    resLoader.loadAllResources(resources)
    chestGeneration:ChestGeneration = ChestGeneration(resources, interface)
    structure:dict = resources.structures["basichouse1"]

    info = structure.info
    buildingCondition = BaseStructure.createBuildingCondition()
    buildingInfo = structure.setupInfoAndGetCorners()
    buildingCondition["flip"] = 1
    buildingCondition["rotation"] = 0
    buildingInfo = structure.getNextBuildingInformation( buildingCondition["flip"], buildingCondition["rotation"])
    buildingCondition["position"] = [4787, 69, 6095]
    buildingCondition["referencePoint"] = buildingInfo["entry"]["position"]
    buildingCondition["size"] = buildingInfo["size"]

    buildingCondition["replaceAllAir"] = 3

    structureBiomeId = util.getBiome(buildingCondition["position"][0], buildingCondition["position"][2], 1, 1)
    structureBiomeName = resources.biomeMinecraftId[int(structureBiomeId)]
    
    structureBiomeBlockId = str(resources.biomesBlockId[structureBiomeName])

    if structureBiomeBlockId == "-1" :
        structureBiomeBlockId = "0" 
        
    settlementData = {}
    settlementData["materialsReplacement"] = {}
    settlementData["materialsReplacement"]["villageName"] = "TestLand"
    loremaker.voteForColor(settlementData)
    buildingCondition["replacements"] = copy.deepcopy(settlementData["materialsReplacement"])

    # Load block for structure biome
    for aProperty in resources.biomesBlocks[structureBiomeBlockId]:
        if aProperty in resources.biomesBlocks["rules"]["village"]:
            buildingCondition["replacements"][aProperty] = resources.biomesBlocks[structureBiomeBlockId][aProperty]

    # Load block for structure biome
    for aProperty in resources.biomesBlocks[structureBiomeBlockId]:
        if aProperty in resources.biomesBlocks["rules"]["structure"]:
            buildingCondition["replacements"][aProperty] = resources.biomesBlocks[structureBiomeBlockId][aProperty]

    settlementData = {
        "villagerNames" : ["rodriguez sdfsd", "sdfsdfsdf"],
        "structures" : [
            {"name" : "basichouse1", "villagersId" : [0]},
            {"name" : "basichouse1", "villagersId" : [1]}
        ]
    }

    buildingCondition["special"]["bedroomhouse"] = ["minecraft:written_book" + toolbox.writeBook(
                book.createBookForVillager(settlementData, 0)[0],
                     title="jean ", author="SDQS", description="QSSDD" )]

    structure.build(worldModif, buildingCondition, chestGeneration)
    worldModif.saveToFile(file)

else : 
    if args.remove == "r" :   
        worldModif.loadFromFile(file)
    else :
        worldModif.loadFromFile(args.remove)
    worldModif.undoAllModification()