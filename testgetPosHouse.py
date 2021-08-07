from generation.resources import *
from generation.chestGeneration import *
from generation.structures.structures import *
from generation.structureManager import *
from generation.floodFill import *
import generation.resourcesLoader as resLoader
from utils.worldModification import *
from lib.worldLoader import WorldSlice

interface = interfaceUtils.Interface()
area = (0, 0, 128, 128)
interfaceUtils.runCommand("execute at @p run setbuildarea ~-150 0 ~-150 ~150 255 ~150")
buildArea = interfaceUtils.requestBuildArea()
floodFill = FloodFill()
if buildArea != -1:
    x1 = buildArea[0]
    z1 = buildArea[2]
    x2 = buildArea[3]
    z2 = buildArea[5]
    print(buildArea)
    area = (x1, z1, x2 - x1, z2 - z1)
print(area)
ws = WorldSlice(area)
house1 = floodFill.findPosHouse([[-1, 63, -1], [-1, 63, 6], [3, 63, -1], [3, 63, 6]],ws)
house2 = floodFill.findPosHouse([[-1, 63, -1], [-1, 63, 6], [3, 63, -1], [3, 63, 6]],ws)

house3 = floodFill.findPosHouse([[-1, 63, -1], [-1, 63, 6], [3, 63, -1], [3, 63, 6]],ws)
print(house1,house2,house3)

