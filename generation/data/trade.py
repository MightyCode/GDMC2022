import random
import utils.util as util
import copy


class Trade:
    def __init__(self):
        self.mastery: int = 0
        self.offer: str = ""
        self.offer_quantity: int = 0

        self.needing: str = ""
        self.needing_quantity: int = 0

    @staticmethod
    def generateFromTradeTable(lore_village, villager, trade_table_original: dict, material_replacements: dict):
        number_required: int = 0

        trade_table: dict = Trade.filterTableTrade(lore_village, villager, trade_table_original)

        if "numberOfRequired" in trade_table.keys():
            number_required = trade_table["numberOfRequired"]

        chances: list = []
        trade: dict
        for trade in trade_table["trades"]:
            chances.append(trade["chance"])

        trades = util.selectNWithChanceForOther(trade_table["trades"], chances, number_required, True)
        for tradeModel in trades:
            trade: Trade = Trade()

            trade.needing = util.changeNameWithReplacements(tradeModel["required"], material_replacements)[1]

            if type(tradeModel["amount"]) == list:
                trade.needing_quantity = random.randint(tradeModel["amount"][0], tradeModel["amount"][1])
            else:
                trade.needing_quantity = tradeModel["amount"]

            trade.offer = util.changeNameWithReplacements(tradeModel["offered"], material_replacements)[1]
            if type(tradeModel["amountOffered"]) == list:
                trade.offer_quantity = random.randint(tradeModel["amountOffered"][0], tradeModel["amountOffered"][1])
            else:
                trade.offer_quantity = tradeModel["amountOffered"]

            villager.trades.append(trade)

        if "generateTrades" in trade_table.keys():
            Trade.handleGeneratedTrades(lore_village, villager, trade_table, material_replacements)

    @staticmethod
    def filterTableTrade(lore_village, villager, trade_table: dict) -> dict:
        table_copy: dict = copy.deepcopy(trade_table.copy())

        for i in range(len(table_copy["trades"]) - 1, -1, -1):
            trade = table_copy["trades"][i]

            if "conditions" in trade.keys():
                if not Trade.conditionsSatisfied(lore_village, villager, trade["conditions"]):
                    del table_copy["trades"][i]

        return table_copy

    @staticmethod
    def conditionsSatisfied(lore_village, villager, conditions: dict) -> dict:
        for condition in conditions.keys():
            if not Trade.checkOneConditions(lore_village, villager, conditions, condition):
                return False

        return True

    @staticmethod
    def checkOneConditions(lore_village, villager, conditions: dict, condition: str):
        if condition == "tier":
            min_tier: int = 0
            max_tier: int = 0

            if "min" in conditions["tier"].keys():
                min_tier = conditions["tier"]["min"]

            if "max" in conditions["tier"].keys():
                max_tier = conditions["tier"]["max"]

            if "value" in conditions["tier"].keys():
                min_tier = conditions["tier"]["value"]
                max_tier = conditions["tier"]["value"]

            return min_tier <= lore_village.tier <= max_tier

        return False

    @staticmethod
    def handleGeneratedTrades(lore_village, villager, trade_table: dict, material_replacements: dict):
        if villager.job == "Exchanger":
            pass

    def toStr(self, isFirstTrade=False) -> str:
        result: str

        if isFirstTrade:
            result = "{"
        else:
            result = ",{"

        # buy <-> dict

        if "{" not in self.needing and "[" not in self.needing:
            result += "buy:{id:\"" + self.needing + "\", "
        else:
            result += "buy:{id:" + self.needing + ", "

        result += "Count:" + str(self.needing_quantity) + "}"
        # buy B <-> dict
        if "{" not in self.offer and "[" not in self.offer:
            result += ", sell:{id:\"" + self.offer + "\","
        else:
            result += ", sell:{id:" + self.offer + ","

        result += "Count:" + str(self.offer_quantity) + "}"
        # maxUses <-> int
        result += ", maxUses:999999"
        # Xp <-> int
        # rewardXp <-> boolean
        # uses <-> int
        # specialPrice <-> float
        # price multiplier <-> float
        # demand <-> float

        result += "}"

        return result
