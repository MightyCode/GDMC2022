import utils.libUtil as libUtil
import utils.util as util
import random


class ChestGeneration:
    def __init__(self, resources):
        self.resources = resources

    """
    Generate a chest content at given position and loottable
    x : x position of chest
    y : y position of chest
    z : z position of chest
    lootTableName : name of the lootTable used
    changeItemName : indicates what ** balise should change, ex : *woodType*
    additionnalObjects : refers to items that must appear in the chest
    """

    def generate(self, x, y, z, loot_table_name, change_item_name: dict = None, additional_object: list = None):
        if change_item_name is None:
            change_item_name = {}
        if additional_object is None:
            additional_object = []

        loot_table = self.resources.lootTables[loot_table_name]["pools"][0]

        if isinstance(loot_table["rolls"], dict):
            number_item = random.randint(loot_table["rolls"]["min"], loot_table["rolls"]["max"])
        else:
            number_item = loot_table["rolls"]

        item_places = self.generatePlaces(number_item + len(additional_object) - 1)
        item_places.sort()
        items = []

        additional_places, additional_indices = self.generateAdditionalPlacesIndices(item_places.copy(),
                                                                                     len(additional_object))

        sum_weight = 0
        for item in loot_table["entries"]:
            sum_weight += item["weight"]

        j = 0
        for i in range(len(item_places)):
            if j < len(additional_places):
                if item_places[i] == additional_places[j]:
                    items.append([additional_object[additional_indices[j]], 1])
                    j += 1
                    continue

            current_weight = random.randint(0, sum_weight)

            for item in loot_table["entries"]:
                current_weight -= item["weight"]

                # This item is choosen
                if current_weight <= 0:
                    number_of_item = 1

                    # Compute number of items
                    if "functions" in item.keys():
                        if item["functions"][0]["function"] == "set_count":
                            number_of_item = random.randint(item["functions"][0]["count"]["min"],
                                                            item["functions"][0]["count"]["max"])

                    # Compute item's name if balise *, means that one word should change
                    result = util.changeNameWithReplacements(item["name"], change_item_name)

                    if result[0] >= 0:
                        items.append([result[1], number_of_item])
                    else:
                        items.append(["", 0])

                    break

        libUtil.addItemChest(x, y, z, items, item_places)

    """
    Generate places of items
    """

    @staticmethod
    def generatePlaces(number: int):
        places = list(range(28))
        if number > 13:
            for i in range(27 - number):
                index = random.randint(0, len(places) - 1)
                del places[index]
            return places
        else:
            places_b = []
            for i in range(number):
                index = random.randint(0, len(places) - 1)
                places_b.append(places[index])
                del places[index]
            return places_b

    """
    Generate places of additional items
    """

    @staticmethod
    def generateAdditionalPlacesIndices(places, size):
        indices: list = list(range(size))

        additional_places: list = []
        additional_indices: list = []

        for i in range(size):
            index: int = random.randint(0, len(indices) - 1)
            additional_indices.append(indices[index])
            del indices[index]

            index = random.randint(0, len(places) - 1)
            additional_places.append(places[index])
            del places[index]

        additional_places.sort()
        return additional_places, additional_indices
