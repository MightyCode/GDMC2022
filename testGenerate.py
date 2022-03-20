from generation.structures.generated.generatedWell import *
import sys
import lib.interfaceUtils as interfaceUtils
import utils.utils as _utils
from generation.structures.nbtStructures import *
from generation.structures.generated.generatedQuarry import *
from utils.worldModification import *
from generation.resources import *
from generation.chestGeneration import *


file = "temp.txt"

interface = interfaceUtils.Interface()
worldModif = WorldModification(interface)
resources = Resources()
chestGeneration = ChestGeneration(resources, interface)

# x position, z position, x size, z size
area = (0, 0, 128, 128)  # default build area if build area is not set

interfaceUtils.runCommand("execute at @p run setbuildarea ~-64 0 ~-64 ~64 255 ~64")


# see if a build area has been specified
# you can set a build area in minecraft using the /setbuildarea command
buildArea = interfaceUtils.requestBuildArea()
if buildArea == -1:
    exit()
x1 = buildArea[0]
z1 = buildArea[2]
x2 = buildArea[3]
z2 = buildArea[5]
# print(buildArea)
area = (x1, z1, x2 - x1, z2 - z1)

if len(sys.argv) <= 1:
    # Find the highest non-air block and build the quarry there
    cx = int(area[0] + area[2]/2)
    cz = int(area[1] + area[3]/2)

    cy = 255
    ## Find highest non-air block
    cy = _utils.getHighestNonAirBlock(cx, cy, cz)

    buildingConditions = NbtStructures.BUILDING_CONDITIONS.copy()
    buildingConditions["position"] = [cx, cy, cz]

    quarry = GeneratedQuarry()
    quarry.build(worldModif, buildingConditions) 
    # well = GeneratedWell()
    # well.build(worldModif, buildingConditions)
    
 

    worldModif.saveToFile(file)

else : 
    if sys.argv[1] == "r" :   
        worldModif.loadFromFile(file)
    else :
        worldModif.loadFromFile(sys.argv[1])
    worldModif.undoAllModification()
