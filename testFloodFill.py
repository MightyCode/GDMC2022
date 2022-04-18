from generation.resources import *
from generation.chestGeneration import *
from generation.structures.nbtStructures import *
from generation.structureManager import *
from generation.floodFill import *
from utils.worldModification import *
from lib.worldLoader import WorldSlice
#seed testing : -2997648135289524795

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
xPos = -36
zPos = -25
yPos = floodFill.getHeight(xPos,zPos, ws)
print(xPos,yPos,zPos)
testing = floodFill.floodfill(xPos,yPos,zPos,ws,15)
print(testing)