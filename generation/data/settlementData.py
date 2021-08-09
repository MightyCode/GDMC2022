from generation.data.murdererData import MurdererData
import copy

class SettlementData:
    VILLAGE_PROFESSION_LIST = [
                    "farmer", "fisherman", "shepherd", "fletcher", "librarian", "cartographer", 
                    "cleric", "armorer", "weaponsmith", "toolsmith", "butcher", "leatherworker", "mason", "nitwit"]

    def __init__(self):
        self.area = [0, 0]
        self.center = [0, 0]
        self.size = []

        self.discoveredChunks = []

        # Materials replacement
        self.__materialsReplacement = {}

        # Biome 
        self.biomeId = 0
        self.biomeName = ""
        self.biomeBlockId = 0

        self.villageName = ""
        self.__materialsReplacement["villageName"] = self.villageName

        self.villagerNames = []
        self.villagerProfession = []
        self.villagerGameProfession = []

        # [0 -> content, 1 -> isGift]
        self.villagerDiary = []
        
        self.structuresNumberGoal = []

        # structures contains "position", "rotation", "flip" "name", "type", "group", "villagersId", "gift"
        self.structures = []
        self.freeVillager = 0

        self.ressources = {
            "woodResources" : 0,
            "dirtResources" : 0,
            "stoneResources" : 0
        }

        self.murdererData = MurdererData()


    def setArea(self, newArea):
        self.area = newArea
        self.center = [int((self.area[0] + self.area[3]) / 2), 80, int((self.area[2] + self.area[5]) / 2)]
        self.size = [self.area[3] - self.area[0] + 1, self.area[5] - self.area[2] + 1]

    
    def setVillageBiome(self, biomeId, resources):
        self.biomeId = biomeId
        self.biomeName = resources.biomeMinecraftId[int(self.biomeId)]
        self.biomeBlockId =  str(resources.biomesBlockId[self.biomeName])

        if self.biomeBlockId == "-1": 
            print("Generation on biome block id -1")
            self.biomeBlockId = "0"


    def setMaterialReplacement(self, propertyName, replacement):
        self.__materialsReplacement[propertyName] = replacement
    

    def getMaterialReplacement(self, propertyName):
        return self.__materialsReplacement[propertyName]


    def getMatRep(self, propertyName):
        return self.getMaterialReplacement(propertyName)


    def getMatRepDeepCopy(self):
        return copy.deepcopy(self.__materialsReplacement)
