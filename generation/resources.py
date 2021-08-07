from generation.structures.structures import *
import json
from nbt import nbt

class Resources :
    STRUCTURE_PATH = "data/structures/"
    LOOT_TABLE_PATH = "data/lootTables/"
    BIOME = "data/biome.txt"
    BIOME_BLOCK = "data/biomeBlocks.json"

    def __init__(self):
        # Each structures
        self.structures = {}
        self.lootTables = {}


        # Contains for each biome, its minecraft id
        # biomename -> id minecraft
        self.biomes = {}
        # Contains for each id biome, its name
        # id minecraft -> biomename
        self.biomeMinecraftId = {}

        # Contains for each id biome, its block id
        # biomename -> id block (decoration)
        self.biomesBlockId = {}


        # Indicates for each block id, what should be blocks for types (ex : wookType)
        self.biomesBlocks = {}

        
        with open(Resources.BIOME_BLOCK) as json_file:
            self.biomesBlocks = json.load(json_file)

        filin = open(Resources.BIOME)

        lines = filin.readlines()
        i = 0
        for line in lines:
            if len(line.split(":")) > 1 :
                biomename = line.split(":")[0]
                value = int(line.split(":")[1])

                self.biomeMinecraftId[i] = biomename
                self.biomes[biomename] = i
                self.biomesBlockId[biomename] = value
            i = i + 1

    """ 
    Load and add structures from files
    path : path of nbt file
    infoPath : path of info json file related to the structure
    name : name of the structure that will be used on the system
    """
    def loadStructures(self, path, infoPath, name):
        nbtfile = nbt.NBTFile(Resources.STRUCTURE_PATH + path,'rb')
        with open(Resources.STRUCTURE_PATH + infoPath) as json_file:
           info = json.load(json_file)

        assert(not name in self.structures.keys())
        self.structures[name] = Structures(nbtfile, info, name)


    """ 
    Add an hand made structure
    object : instance of the class
    infoPath : path of info json file related to the structure
    name : name of the structure that will be used on the system
    """
    def addGeneratedStructures(self, object, infoPath, name):
        with open(Resources.STRUCTURE_PATH + infoPath) as json_file:
           info = json.load(json_file)
           
        object.setInfo(info)

        assert(not name in self.structures.keys())
        self.structures[name] = object


    """ 
    Load and add new loot table from files
    path : path of json file
    name : name of the loot table that will be used on the system
    """
    def loadLootTable(self, path, name):
        with open(Resources.LOOT_TABLE_PATH + path) as json_file:
           self.lootTables[name] = json.load(json_file)



