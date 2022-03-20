import generation.road as road
from generation.resources import *
from generation.chestGeneration import *
from generation.structures.nbtStructures import *
from generation.structureManager import *
from generation.floodFill import *
import generation.resourcesLoader as resLoader
from utils.worldModification import *
from lib.worldLoader import WorldSlice
import random
#seed testing : -2997648135289524795

interface = interfaceUtils.Interface()
area = (-128, 0, -128, 128,255,128)
interfaceUtils.runCommand("execute at @p run setbuildarea ~-150 0 ~-150 ~150 255 ~150")
buildArea = interfaceUtils.requestBuildArea()
floodFill = FloodFill(area)
ws = WorldSlice(area[0], area[2], area[3], area[5])

test1 = road.Node([-53,26])
test2 = road.Node([-47,11])
chemin = road.Astar(test1,test2,[-48,14,-54,8],[-54,29,-63,23])
for i in chemin:
	interfaceUtils.setBlock(i[0],floodFill.getHeight(i[0],i[1],ws) - 1,i[1],"minecraft:bricks")