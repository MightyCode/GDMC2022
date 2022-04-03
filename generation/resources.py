from generation.structures.nbtStructures import NbtStructures
import json
from nbt import nbt


class Resources:
    DATA = "data/"
    STRUCTURE_PATH = DATA + "structures/"
    LOOT_TABLE_PATH = DATA + "lootTables/"
    BIOME = DATA + "biome.txt"
    BIOME_BLOCK = DATA + "biomeBlocks.json"
    TRADES = DATA + "trades.json"

    def __init__(self):
        # Each structures
        self.structures: dict = {}
        self.lootTables: dict = {}

        # Contains for each biome, its minecraft id
        # biome name -> id minecraft
        self.biomes: dict = {}
        # Contains for each id biome, its name
        # id minecraft -> biome name
        self.biomeMinecraftId: dict = {}

        # Contains for each id biome, its block id
        # biome name -> id block (decoration)
        self.biomesBlockId: dict = {}

        # Indicates for each block id, what should be blocks for types (ex : wookType)
        self.biomesBlocks: dict = {}

        with open(Resources.BIOME_BLOCK) as json_file:
            self.biomesBlocks = json.load(json_file)

        file_in = open(Resources.BIOME)

        lines = file_in.readlines()
        i = 0
        for line in lines:
            if len(line.split(":")) > 1:
                biome_name = line.split(":")[0]
                value = int(line.split(":")[1])

                self.biomeMinecraftId[i] = biome_name
                self.biomes[biome_name] = i
                self.biomesBlockId[biome_name] = value

            i += 1

        self.trades: dict = {}
        with open(Resources.TRADES) as json_file:
            self.trades = json.load(json_file)

    """ 
    Load and add structures from files
    path : path of nbt file
    infoPath : path of info json file related to the structure
    name : name of the structure that will be used on the system
    """

    def loadStructures(self, path, infoPath, name):
        nbt_file: nbt.NBTFile = nbt.NBTFile(Resources.STRUCTURE_PATH + path, 'rb')

        with open(Resources.STRUCTURE_PATH + infoPath) as json_file:
            info = json.load(json_file)

        assert (name not in self.structures.keys())
        self.structures[name] = NbtStructures(nbt_file, info, name)

    """ 
    Add an hand made structure
    object : instance of the class
    infoPath : path of info json file related to the structure
    name : name of the structure that will be used on the system
    """

    def addGeneratedStructures(self, structureObject, infoPath, name) -> None:
        with open(Resources.STRUCTURE_PATH + infoPath) as json_file:
            info = json.load(json_file)

        structureObject.setInfo(info)

        assert (name not in self.structures.keys())
        self.structures[name] = structureObject

    """ 
    Load and add new loot table from files
    path : path of json file
    name : name of the loot table that will be used on the system
    """

    def loadLootTable(self, path, name) -> None:
        with open(Resources.LOOT_TABLE_PATH + path) as json_file:
            self.lootTables[name] = json.load(json_file)
