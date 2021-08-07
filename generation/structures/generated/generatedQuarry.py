import collections, numpy
import random
import utils.util as util
import math
from generation.structures.baseStructure import * 

"""
Hand made generated quarry
"""
class GeneratedQuarry(BaseStructure):
    def __init__(self) :
        super(BaseStructure, self).__init__()
        self.listOfBlocks = numpy.array([])
        self.computedOrientation = {}

        self.uselessBlocks = [
        'minecraft:air', 'minecraft:cave_air', 'minecraft:water', 'minecraft:lava'
        'minecraft:oak_leaves',  'minecraft:leaves',  'minecraft:birch_leaves', 'minecraft:spruce_leaves'
        'minecraft:oak_log',  'minecraft:spruce_log',  'minecraft:birch_log',  'minecraft:jungle_log', 'minecraft:acacia_log', 'minecraft:dark_oak_log',
        'minecraft:grass', 'minecraft:snow', 'minecraft:poppy'
        'minecraft:dead_bush', "minecraft:cactus", "minecraft:sugar_cane"]

    
    def setupInfoAndGetCorners(self):
        self.setSize([random.randint(7, 14), random.randint(9, 21), random.randint(7, 14)])

        self.info["mainEntry"]["position"] = [int(self.size[0] / 2), self.size[1] - 5, 0]
        
        return self.getCornersLocalPositionsAllFlipRotation(self.info["mainEntry"]["position"])


    def getNextBuildingInformation(self, flip, rotation):
        info = {}
        self.info["mainEntry"]["facing"] = "north"
        info["entry"] = { 
            "position" : self.info["mainEntry"]["position"], 
            "facing" : self.getFacingMainEntry(flip, rotation) 
            }
        info["size"] = self.size
        info["corner"] = self.getCornersLocalPositions(self.info["mainEntry"]["position"].copy(), flip, rotation)

        return info


    def build(self, worldModif, buildingCondition, chestGeneration):
        self.setSize(buildingCondition["size"])
        self.entry = buildingCondition["referencePoint"].copy()
        self.computeOrientation(buildingCondition["rotation"], buildingCondition["flip"])

        if buildingCondition["flip"] == 1 or buildingCondition["flip"] == 3:
            buildingCondition["referencePoint"][0] = self.size[0] - 1 - buildingCondition["referencePoint"][0] 
        if buildingCondition["flip"] == 2 or buildingCondition["flip"] == 3:
            buildingCondition["referencePoint"][2] = self.size[2] - 1 - buildingCondition["referencePoint"][2] 

        woodType = "*woodType*"
        result = util.changeNameWithBalise(woodType, buildingCondition["replacements"])
        if result[0] >= 0:
            woodType = result[1]
        else :
            woodType = "oak"

        self.fenceType = "minecraft:" + woodType + "_fence"
        self.fenceGateType = self.fenceType + "_gate"
        self.strippedWoodType = "minecraft:stripped_" + woodType + "_wood"

        self.listOfBlocks = numpy.array([])
        ## Building the quarry.
        for dy in range(self.size_y()):
            for dx in range(1, self.size_x() - 1):
                for dz in range(1, self.size_z() -1):
                    # Get all the block we chunk
                    position = self.returnWorldPosition([dx, dy, dz], buildingCondition["flip"], 
                        buildingCondition["rotation"], buildingCondition["referencePoint"], buildingCondition["position"])

                    block = worldModif.interface.getBlock(position[0], position[1], position[2])
                    if block not in self.uselessBlocks:
                        self.listOfBlocks = numpy.append(self.listOfBlocks, block) 
        

        # Fill the area with air block
        
        fromBlock = self.returnWorldPosition([1, 0, 1], buildingCondition["flip"], 
                        buildingCondition["rotation"], buildingCondition["referencePoint"], buildingCondition["position"])
        toBlock = self.returnWorldPosition([self.size_x() - 2, self.size_y() - 1 , self.size_z() - 2], buildingCondition["flip"], 
                        buildingCondition["rotation"], buildingCondition["referencePoint"], buildingCondition["position"])

        worldModif.fillBlocks(fromBlock[0], fromBlock[1], fromBlock[2], toBlock[0], toBlock[1], toBlock[2], "minecraft:air")

        # Add the fences
        self.addFencesToQuarry(worldModif, buildingCondition)
        # Add the fence gate and the ladders
        self.addFenceGateToQuarry(worldModif, buildingCondition)   
        # Add the items to the chests
        self.addChestToQuarry(worldModif, buildingCondition, self.listOfBlocks)

        torchPositions = [[1, int(self.size_z() / 2)], [int(self.size_x() / 2), self.size_z() - 2], [self.size_x() - 2, int(self.size_z()/2)]]
        orientations = ["east", "north", "west"]

        for i in range(len(torchPositions)):
            position = self.returnWorldPosition(
                        [torchPositions[i][0], int(self.size_y() / 3), torchPositions[i][1]], 
                        buildingCondition["flip"], buildingCondition["rotation"], 
                        buildingCondition["referencePoint"], buildingCondition["position"])
            # Set a chest
            worldModif.setBlock(position[0], position[1], position[2], "minecraft:wall_torch[" +  self.convertProperty("facing", orientations[i])  +"]")

    """
    Add chest at the bottom of quarry and fill it with blocks removed by the quarry
    """
    def addChestToQuarry(self, worldModif, buildingCondition, list):  
        position = self.returnWorldPosition(
                        [1, 0, 1], buildingCondition["flip"], 
                        buildingCondition["rotation"], buildingCondition["referencePoint"], buildingCondition["position"])
        # Set a chest
        worldModif.setBlock(position[0], position[1], position[2], "minecraft:chest[" +  self.convertProperty("facing", "south")  +"]", placeImmediately=True)

        counter = collections.Counter(list)
        items = counter.items()
        itemsList = []
        for i in items:
            # If there is more than one stack of block (64)
            if i[1] > 64:
                x = i[1] / 64
                y = math.floor(x)
                for z in range(0, y):
                    newList = []
                    newList.append(i[0])
                    newList.append(64)
                    itemsList.append(newList)
            else:
                sublist = []
                sublist.append(i[0])
                sublist.append(i[1])
                itemsList.append(sublist)
        util.addItemChest(position[0], position[1], position[2], itemsList)
        

    def addFencesToQuarry(self, worldModif, buildingCondition):
        # Add the fences for the quarry

        fenceSideUpperPosition = self.size_y() - 3
        lengths = [self.size_x(), self.size_z(), self.size_x(), self.size_z()]
        multiplier = [[1, 0], [0, 1], [1, 0], [0, 1]]
        positions = [[0, 0], [0, 0], [0, self.size_z() - 1], [self.size_x() - 1, 0]]

        for i in [0, 1, 2, 3]:
            for j in range(lengths[i]):
                for y in range(fenceSideUpperPosition):
                    localPosition = [positions[i][0] + j * multiplier[i][0], y , positions[i][1] + j * multiplier[i][1]] 
                    position = self.returnWorldPosition(
                        localPosition, buildingCondition["flip"], 
                        buildingCondition["rotation"], buildingCondition["referencePoint"], buildingCondition["position"])
                    
                    block = worldModif.interface.getBlock(position[0], position[1], position[2])
                    if  block in self.uselessBlocks or y == fenceSideUpperPosition - 1:
                        worldModif.setBlock(position[0], position[1], position[2], self.fenceType + "[waterlogged=false]")

    
    def addFenceGateToQuarry(self, worldModif, buildingCondition):
        # Add the fence gate
        position = self.returnWorldPosition(
                        [self.entry[0], self.entry[1] + 2, self.entry[2]],
                        buildingCondition["flip"], buildingCondition["rotation"], buildingCondition["referencePoint"],
                        buildingCondition["position"])
        
        worldModif.setBlock(position[0], position[1], position[2],  "minecraft:air")

        worldModif.setBlock(position[0], position[1] - 1, position[2], self.fenceGateType + "[" + self.convertProperty("facing", "north") + "]")

        positions = [[-2, 2], [-1, 2], [-1, 3], [0, 3], [1, 3], [1, 2], [2, 2]]
        for pos in positions:
            position = self.returnWorldPosition(
                        [   self.entry[0] + pos[0], 
                            self.entry[1] + pos[1], 
                            self.entry[2]],
                        buildingCondition["flip"], buildingCondition["rotation"], buildingCondition["referencePoint"],
                        buildingCondition["position"])
            worldModif.setBlock(position[0], position[1], position[2], self.fenceType + "[waterlogged=false]")
        
        positions = [ [-1, 4], [0, 4], [1, 4]]
        for pos in positions:
            position = self.returnWorldPosition(
                        [   self.entry[0] + pos[0], 
                            self.entry[1] + pos[1], 
                            self.entry[2]],
                        buildingCondition["flip"], buildingCondition["rotation"], buildingCondition["referencePoint"],
                        buildingCondition["position"])
            worldModif.setBlock(position[0], position[1], position[2], "minecraft:torch")
        

        # Add the ladders
        for wood in range(self.entry[1] + 1):
            position = self.returnWorldPosition(
                [self.entry[0], wood, self.entry[2]],
                buildingCondition["flip"], buildingCondition["rotation"], buildingCondition["referencePoint"],
                buildingCondition["position"])

            worldModif.setBlock(position[0], position[1], position[2], self.strippedWoodType)

            position = self.returnWorldPosition(
                [self.entry[0], wood, self.entry[2] + 1],
                buildingCondition["flip"], buildingCondition["rotation"], buildingCondition["referencePoint"],
                buildingCondition["position"])
       
            worldModif.setBlock(position[0], position[1], position[2], "minecraft:ladder[" + self.convertProperty("facing", "south")  +  ",waterlogged=false]")
    
        #print("Finish building : basicQuarry")
        