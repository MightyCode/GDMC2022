from generation.resources import Resources
from generation.data.village import Village
import copy
import utils.util as util


class SettlementData:
    def __init__(self, village: Village):
        self.village_model = village
        self.area: list = [0, 0]
        self.center: list = [0, 0]
        self.size: list = []

        self.discovered_chunks: list = []

        # Materials replacement
        self.__materials_replacement: dict = {}

        # Biome 
        self.biome_id: int = 0
        self.biome_name: str = ""
        self.biome_block_id: int = 0

        self.structure_number_goal: int = 0

        self.resources: dict = {
            "woodResources": 0,
            "dirtResources": 0,
            "stoneResources": 0
        }

    def init(self) -> None:
        self.__materials_replacement["villageName"] = self.village_model.name

        self.__materials_replacement["village_currency_item"] = util.returnCurrencyItem(
            self.village_model.name + " gem")

        self.__materials_replacement["village_currency_trade"] = util.returnCurrencyTrade(
            self.village_model.name + " gem")

        self.__materials_replacement["toolMaterial"] = "wooden"
        self.__materials_replacement["equipmentMaterial"] = "leather"

        if self.village_model.tier == 1:
            self.__materials_replacement["toolMaterial"] = "stone"
            self.__materials_replacement["equipmentMaterial"] = "chainmail"
        elif self.village_model.tier == 2:
            self.__materials_replacement["toolMaterial"] = "iron"
            self.__materials_replacement["equipmentMaterial"] = "iron"

    def setArea(self, new_area: list) -> None:
        self.area = new_area
        self.center = [int((self.area[0] + self.area[3]) / 2), 80, int((self.area[2] + self.area[5]) / 2)]
        self.size = [self.area[3] - self.area[0] + 1, self.area[5] - self.area[2] + 1]

    def setVillageBiome(self, biome_id: int, resources: Resources) -> None:
        self.biome_id = biome_id
        self.biome_name = resources.biomeMinecraftId[int(self.biome_id)]
        self.biome_block_id = str(resources.biomesBlockId[self.biome_name])

        if self.biome_block_id == "-1":
            print("Generation on biome block id -1")
            self.biome_block_id = "0"

        # Load replacements for structure biome
        for aProperty in resources.biomesBlocks[self.biome_block_id]:
            if aProperty in resources.biomesBlocks["rules"]["village"]:
                self.setMaterialReplacement(aProperty,
                                            resources.biomesBlocks[self.biome_block_id][
                                                aProperty])

    def setMaterialReplacement(self, property_name: str, replacement: str) -> None:
        self.__materials_replacement[property_name] = replacement

    def getMaterialReplacement(self, propertyName: str) -> str:
        return self.__materials_replacement[propertyName]

    def getMatRepDeepCopy(self) -> dict:
        return copy.deepcopy(self.__materials_replacement)
