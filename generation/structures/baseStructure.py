import utils.projectMath as _math
import utils.util as util
import utils.projectMath as projectMath
import lib.interfaceUtils as interfaceUtils
import generation.floodFill as floodFill
import random
import math

""" 
# Main class which corresponds to a buildeable 
"""
class BaseStructure:

    AIR_BLOCKS = ["minecraft:air", "minecraft:void_air", "minecraft:cave_air"]

    ORIENTATIONS = ["west", "north" , "east", "south"]

    LIST_ALL_FACING = ["south", "south-southwest", "southwest",
                    "west-southwest",  "west", "west-northwest", 
                    "northwest", "north-northwest", "north",
                    "north-northeast", "northeast", "east-northeast",
                    "east", "east-southeast", "southeast", "south-southeast"]

    AIR_FILLING_PROBLEMATIC_BLOCS = ["minecraft:sand", "minecraft:red_sand",
                             "minecraft:gravel", "minecraft:water", "minecraft:lava"]

    """ 
    Empty constructor
    """
    def __init__(self):
        pass
    
    """
    Set info
    info : dictionnary containings information about the structures
    """
    def setInfo(self, info):
        self.info = info
        self.size = [0, 0, 0]
        self.computedOrientation = {}


    """
    Return a premake dictionnary required to build a structure
    Flip is applied before rotation

    size : size of the structure
    position : the of the refencePoint in the real world
    referencePoint : point x, z where the building will rotate around, the block at the reference point will be on position point
    flip : No flip = 0, Flip x = 1, flip z = 2, Flip xz = 3
    rotation : No rotation = 0, rotation 90° = 1, rotation 180° = 2, rotation 270° = 3
    replaceAllAir : 0 no air placed, 1 place all air block, 2 place all choosen air block, 3 take the prefered replacement air from info file
    replacements : change one type of block to another
    prebuildingInfo
    special : dict to put very specific informations
    """
    def createBuildingCondition():
        return {
            "size" : [0, 0, 0],
            "position" : [0, 0, 0],
            "referencePoint" : [0, 0, 0],
            "flip" : 0,
            "rotation" : 0,
            "replaceAllAir" : 0,
            "replacements" : {},
            "villager" : [],
            "prebuildingInfo" : {},
            "special" : {}
        }


    """
    Return a position in the world 
    localPoint : position of the block inside the local space, [0, 0, 0]
    flip : flip applied to localspace, [0|1|2|3]
    rotation : rotation applied to localspace, [0|1|2|3]
    referencePoint : the origin of the local space, what should be the 0, 0, [0, 0, 0]
    worldStructurePosition : position of the structure in real world, position in relation with reference point
    """
    def returnWorldPosition(self, localPoint, flip, rotation, referencePoint, worldStructurePosition) :
        worldPosition = [0, 0, 0]
        
        # Position in building local spacereplacements
        if flip == 1 or flip == 3 :
            worldPosition[0] = self.size[0] - 1 - localPoint[0]
        else : 
            worldPosition[0] = localPoint[0]

        if flip == 2 or flip == 3 :
            worldPosition[2] = self.size[2] - 1 - localPoint[2]
        else :
           worldPosition[2] = localPoint[2]

        worldPosition[1] = localPoint[1]

        # Take rotation into account, apply to building local positions
        worldPosition[0], worldPosition[2] = _math.rotatePointAround(
            [worldStructurePosition[0] + referencePoint[0], worldStructurePosition[2] + referencePoint[2]], 
            [worldStructurePosition[0] + worldPosition[0], worldStructurePosition[2] + worldPosition[2]], 
            rotation *  math.pi / 2)

        # Position in real world
        worldPosition[0] = int(worldPosition[0])                        - referencePoint[0]
        worldPosition[1] = worldStructurePosition[1] + worldPosition[1] - referencePoint[1] 
        worldPosition[2] = int(worldPosition[2])                        - referencePoint[2]

        return worldPosition 

    
    """
    Convert a property using computedOrintation (left, right, north, south, east, west)
    """
    def convertProperty(self, propertyName, propertyValue):
        if propertyValue in self.computedOrientation.keys():
            propertyValue = self.computedOrientation[propertyValue]

        return propertyName + "=" + propertyValue


    """
    Return number, depending to the rotation
    """
    def returnRotationFromFacing(self, facing):
        for i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]:
            if BaseStructure.LIST_ALL_FACING[i] == facing:
                return i
        
        return -1


    """
    Compute all orientation
    rotation : rotation applied to the structure, No rotation = 0, rotation 90° = 1, rotation 180° = 2, rotation 270° = 3
    flip : flip applied to the structure, No flip = 0, Flip x = 1, flip z = 2, Flip xz = 3
    """
    def computeOrientation(self, rotation, flip) :
        # Construct orientation
        self.computedOrientation = { 
            "left" : "left",
            "right" : "right",
            "x" : "x",
            "y" : "y",
            BaseStructure.ORIENTATIONS[0] : BaseStructure.ORIENTATIONS[0],
            BaseStructure.ORIENTATIONS[1] : BaseStructure.ORIENTATIONS[1],
            BaseStructure.ORIENTATIONS[2] : BaseStructure.ORIENTATIONS[2],
            BaseStructure.ORIENTATIONS[3] : BaseStructure.ORIENTATIONS[3]
        }
        
        # Apply flip to orientation
        if flip == 1 or flip == 3:
            self.computedOrientation["east"] = "west" 
            self.computedOrientation["west"] = "east"
            
        if flip == 2 or flip == 3:
            self.computedOrientation["south"] = "north"
            self.computedOrientation["north"] = "south"

        if flip == 1 or flip == 2:
            self.computedOrientation["left"] = "right"
            self.computedOrientation["right"] = "left"

        # Apply rotation to orientation
        for orientation in self.computedOrientation.keys():
            if orientation in BaseStructure.ORIENTATIONS:
                self.computedOrientation[orientation] = BaseStructure.ORIENTATIONS[
                    (BaseStructure.ORIENTATIONS.index(self.computedOrientation[orientation]) + rotation) % len(BaseStructure.ORIENTATIONS)
                ]

        if rotation == 1 or rotation == 3:
            self.computedOrientation["x"] = "z"
            self.computedOrientation["z"] = "x"


    def parseSpecialRule(self, buildingCondition, worldModification):
        if not "special" in self.info.keys():
            return
        
        for key in self.info["special"].keys():
            if key == "sign":
                i = 0
                for sign in self.info["special"][key]:
                    signPosition = self.returnWorldPosition(
                        sign["position"],
                        buildingCondition["flip"], buildingCondition["rotation"], 
                        buildingCondition["referencePoint"], buildingCondition["position"]
                    )

                    worldModification.setBlock(signPosition[0], signPosition[1] + 1, signPosition[2], 
                        "minecraft:" + buildingCondition["replacements"]["woodType"] + "_wall_sign[facing=" + self.computedOrientation[sign["orientation"]] + "]", 
                        placeImmediately=True)

                    if buildingCondition["special"]["sign"][i * 4] == "" and buildingCondition["special"]["sign"][i * 4 + 1] == "" :
                        if buildingCondition["special"]["sign"][i * 4 + 2] == "" and buildingCondition["special"]["sign"][i * 4 + 3] == "":
                            continue

                    interfaceUtils.setSignText(
                        signPosition[0], signPosition[1] + 1, signPosition[2], 
                        buildingCondition["special"]["sign"][i * 4], buildingCondition["special"]["sign"][i * 4 + 1],
                        buildingCondition["special"]["sign"][i * 4 + 2], buildingCondition["special"]["sign"][i * 4 + 3])
                    
                    i += 1

    """
    Return position where reference position is the center of the local space
    referencePosition : the origin of the local space, what should be the 0, 0,  [0, 0, 0]
    flip : flip applied to localspace, [0|1|2|3]
    rotation : rotation applied to localspace, [0|1|2|3]
    """
    def getCornersLocalPositions(self, referencePosition, flip, rotation):
        refPos = referencePosition.copy()
        if flip == 1 or flip == 3 :
            refPos[0] = self.size[0] - 1 - refPos[0]

        if flip == 2 or flip == 3 :
            refPos[2] = self.size[2] - 1 - refPos[2]

        temp = _math.rotatePointAround([0, 0], [- refPos[0], - refPos[2]] , math.pi / 2 * rotation)

        temp1 = _math.rotatePointAround([0, 0], [self.size[0] - 1 - refPos[0], self.size[2] - 1 - refPos[2]] , math.pi / 2 * rotation)
        
        return [int(min(temp[0], temp1[0])), 
                int(min(temp[1], temp1[1])), 
                int(max(temp[0], temp1[0])), 
                int(max(temp[1], temp1[1]))]

    
    def returnFlipRotationThatIsInZone(self, position, mainEntryPosition, area):
        flip = random.randint(0, 3)
        rotations = list(range(4))
        valid = False

        while len(rotations) > 0 and not valid :
            valid = True
            index = random.randint(0, len(rotations) -1)
            rotation = rotations[index]
            del rotations[index]

            corner = self.getCornersLocalPositions(mainEntryPosition, flip, rotation)

            for i,j in [[0, 1], [2, 1], [0, 3], [2, 3]]:
                if not projectMath.isPointInSquare(
                    [position[0] + corner[i] , position[1] + corner[j]], 
                    [area[0], area[2] , area[3] , area[5]]):
                    valid = False
                    break

        return flip, rotation

    """
    Get corners of all possible flip and rotation
    """
    def getCornersLocalPositionsAllFlipRotation(self, referencePosition):
        corners = []
        for flip in [0, 1, 2, 3]:
            for rotation in [0, 1, 2, 3]:
                corners.append(self.getCornersLocalPositions(referencePosition, flip, rotation))

        return corners


    """
    Place wall sign, which
    position : position of the upper sign
    worldModification : class used to place blocks
    woodType : type of wood for the sign
    people : people's name which should appears in the sign
    """
    def generateSignatureSign(self, position, worldModification, woodType, people):
        if not "sign" in self.info.keys():
            return

        worldModification.setBlock(position[0], position[1], position[2], "minecraft:air", placeImmediately=True)
        worldModification.setBlock(position[0], position[1], position[2], 
            "minecraft:" + woodType + "_wall_sign[facing=" + self.computedOrientation[self.info["sign"]["facing"]] + "]", 
            placeImmediately=True)
    
        lines = ["", "", "", "", "", "", "", ""]
        lines[0] = "Tier " + str(self.info["sign"]["tier"])
        lines[1] = self.info["sign"]["name"]
        
        util.parseVillagerNameInLines(people, lines, 2)

        interfaceUtils.setSignText(
            position[0], position[1], position[2], 
            lines[0], lines[1], lines[2], lines[3])

        if len(lines[4]) > 0:
            worldModification.setBlock(position[0], position[1] - 1, position[2], "minecraft:air", placeImmediately=True)
            worldModification.setBlock(position[0], position[1] - 1, position[2], 
                "minecraft:" + woodType + "_wall_sign[facing=" + self.computedOrientation[self.info["sign"]["facing"]] + "]", 
                placeImmediately=True)

            interfaceUtils.setSignText(
                position[0], position[1] - 1, position[2], 
                lines[4], lines[5], lines[6], lines[7])


    """
    Place ground under the structure at given position
    worldModification : class used to place blocks
    buildingCondition : condition used to build a structures
    """
    def placeSupportUnderStructure(self, worldModif, buildingCondition):
        if not "ground" in self.info.keys():
            return

        zones = []
        if "info" in self.info["ground"].keys():
            if "all" == self.info["ground"]["info"] :
                zones.append([0, 0, self.size[0] - 1, self.size[2] - 1])
        elif "zones" in self.info["ground"].keys() :
            zones = self.info["ground"]["zones"]

        for zone in zones : 
            for x in range(zone[0], zone[2] + 1):
                for z in range(zone[1], zone[3] + 1):
                    position = self.returnWorldPosition( 
                        [ x, 0, z],
                        buildingCondition["flip"], buildingCondition["rotation"], 
                        buildingCondition["referencePoint"], buildingCondition["position"] 
                    )

                    if worldModif.interface.getBlock(position[0], position[1], position[2]) in floodFill.FloodFill.IGNORED_BLOCKS:
                        i = -2 
                        while worldModif.interface.getBlock(position[0], position[1] + i, position[2]) in floodFill.FloodFill.IGNORED_BLOCKS:
                            i -= 1
                        
                        worldModif.fillBlocks(position[0], position[1], position[2], position[0], position[1] + i, position[2], 
                        buildingCondition["replacements"]["ground2"])


    """
    Place air at given position
    worldModification : class used to place blocks
    buildingCondition : condition used to build a structures
    """
    def placeAirZones(self, worldModif, buildingCondition):
        if buildingCondition["replaceAllAir"] == 3:
            buildingCondition["replaceAllAir"] = self.info["air"]["preferedAirMode"]

        if buildingCondition["replaceAllAir"] == 2:
            for zones in self.info["air"]["replacements"]:
                blockFrom = self.returnWorldPosition([ zones[0], zones[1] + 1, zones[2] ],
                                                     buildingCondition["flip"], buildingCondition["rotation"], 
                                                     buildingCondition["referencePoint"], buildingCondition["position"])
                blockTo   = self.returnWorldPosition([ zones[3], zones[4] + 1, zones[5] ],
                                                     buildingCondition["flip"], buildingCondition["rotation"], 
                                                     buildingCondition["referencePoint"], buildingCondition["position"])

                for x in range(min(blockFrom[0], blockTo[0]), max(blockFrom[0], blockTo[0]) + 1):
                    for z in range(min(blockFrom[2], blockTo[2]), max(blockFrom[2], blockTo[2]) + 1):
                        if worldModif.interface.getBlock(x, blockTo[1] + 1, z) in BaseStructure.AIR_FILLING_PROBLEMATIC_BLOCS:
                            worldModif.setBlock(x, blockTo[1] + 1, z, "minecraft:stone", placeImmediately=True)
                                                     
                worldModif.fillBlocks(blockFrom[0], blockFrom[1], blockFrom[2], blockTo[0], blockTo[1], blockTo[2], BaseStructure.AIR_BLOCKS[0])

    """
    Get the facing of the main entry depending of the flip and rotation
    flip : flip applied to localspace, [0|1|2|3]
    rotation : rotation applied to localspace, [0|1|2|3]
    """
    def getFacingMainEntry(self, flip, rotation):
        self.computeOrientation(rotation, flip)
        return self.computedOrientation[self.info["mainEntry"]["facing"]]


    """
    Base function 
    Get all corners and setup variables
    """
    def setupInfoAndGetCorners(self):
        return []


    """
    Base function 
    Setup all variables which requires flip and rotation
    Return a dict with ["size"] of structure and ["entry]["position], ["entry]["facing"]
    flip : flip applied to localspace, [0|1|2|3]
    rotation : rotation applied to localspace, [0|1|2|3]
    """
    def getNextBuildingInformation(self, flip, rotation):
        return {}


    """
    Protected method
    Set size of structure
    """
    def setSize(self, size):
        self.size = size


    """
    Get size of structure
    Work for structure
    Work sometimes depending when called in hand made (generated) structure.
    """
    def getSize(self):
        return self.size
    
    """
    Get size x
    """
    def size_x(self):
        return self.size[0]
        
    """
    Get size y
    """
    def size_y(self):
        return self.size[1]
        

    """
    Get size z
    """
    def size_z(self):
        return self.size[2]

    """
    Get size of structure when rotated 90° or 270°
    """
    def getRotateSize(self):
        return [self.size[2], self.size[1], self.size[0]]

    """
    Indicates if property is valid with a block
    blockName : name of the block
    property : property which should be applied with blockName
    """
    def propertyCompatible(self, blockName, property):
        if property == "snowy":
            if blockName != "minecraft:grass_block":
                return False
        
        return True
