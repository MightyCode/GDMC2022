import random
import copy

import utils.util as util
from generation.data.village import Village
from generation.data.villager import Villager
from generation.data.village import VillageInteraction
from generation.data.loreStructure import LoreStructure
from utils.checkOrCreateConfig import Config


def genPositionOfVillage(existing_areas: list, goal_number: int) -> list:
    positions: list = []

    for area in existing_areas:
        positions.append([int((area[0] + area[3]) / 2),
                          int((area[2] + area[5]) / 2)])

    remaining_index_start: int = len(existing_areas)

    for i in range(goal_number - remaining_index_start):
        random_index: int = random.randint(0, len(positions) - 1)

        reference: list = copy.copy(positions[random_index])
        reference[0] += random.randint(400, 900) if random.randint(1, 2) == 1 else random.randint(-900, 400)
        reference[1] += random.randint(400, 900) if random.randint(1, 2) == 1 else random.randint(-900, 400)

        positions.append(reference)

    return positions


def initializedVillages(positions_of_villages: list, name_generator) -> list:
    villages: list = []

    for i in range(len(positions_of_villages)):
        villages.append(Village())
        villages[i].position = positions_of_villages[i]
        villages[i].generateVillageInformation(name_generator)
        villages[i].generateVillageLore()

    return villages


def createVillageRelationAndAssign(villages: list) -> list:
    interactions: list = []
    other_villages = villages.copy()
    del other_villages[0]

    for i in range(len(villages) - 1):
        villages[i].makeRelations(other_villages)
        for villageId in villages[i].village_interactions.keys():
            interactions.append(villages[i].village_interactions[villageId])

        del other_villages[0]

    for village in villages:
        village.generateLoreAfterRelation()

    return interactions


def checkForImpossibleInteractions(villages: list, interactions: list):
    """Check for two enemy villages if they are friend with same village"""

    village_to_check = villages.copy()
    random.shuffle(village_to_check)

    for village in village_to_check:
        for interaction in interactions:
            if village == interaction.village1 or village == interaction.village2:
                continue

            if interaction.state != VillageInteraction.STATE_WAR:
                continue

            interaction1 = village.village_interactions[interaction.village1]
            interaction2 = village.village_interactions[interaction.village2]
            interaction2 = village.village_interactions[interaction.village2]

            if (interaction1.state != VillageInteraction.STATE_LOVE
                and interaction1.state != VillageInteraction.STATE_FRIENDSHIP) or \
                    (interaction2.state != VillageInteraction.STATE_LOVE
                     and interaction2.state != VillageInteraction.STATE_FRIENDSHIP):
                continue

            if random.randint(0, 1) == 1:
                interaction1.brokeRelation()
                # print("Relation between " + interaction1.village1.name + " " + interaction1.village2.name + " broken")
            else:
                interaction2.brokeRelation()
                # print("Relation between " + interaction2.village1.name + " " + interaction2.village2.name + " broken")


def generateLoreAfterRelation(villages: list):
    order_to_check: list = villages.copy()
    random.shuffle(order_to_check)

    for village in order_to_check:
        if village.status == "peaceful":
            village.isDestroyed = random.randint(1, 10) == 1

            if village.isDestroyed:
                village.destroyCause = "pillager" if random.randint(1, 2) == 1 else "abandoned"
        else:
            village.destroyCause = "war"
            chance: float = computeChanceOfDestructionComparingTier(village)

            if chance == 0.8:
                village.isDestroyed = random.randint(1, 3) == 1
            elif chance == 0.6:
                village.isDestroyed = random.randint(1, 4) != 4

        village.isDestroyed = Config.getValueOrDefault("villageDestroyed", village.isDestroyed)
        village.destroyCause = Config.getValueOrDefault("villageDestroyedCause", village.destroyCause)


def alterSettlementDataWithNewStructures(settlement_data, lore_structure: LoreStructure):
    result: dict = isDestroyStructure(settlement_data.village_model, lore_structure)
    if result != {}:
        # print("DESTRUCTED STRUCTURE")
        lore_structure.destroyed = True
        lore_structure.causeDestroy = result
        applyStructureDestroy(settlement_data.village_model, lore_structure)


def applyLoreToSettlementData(settlement_data):
    fillSettlementDataWithColor(settlement_data, settlement_data.village_model.color)


def fillSettlementDataWithColor(settlement_data, color):
    settlement_data.setMaterialReplacement("color", color)
    settlement_data.setMaterialReplacement("wool", "minecraft:" + color + "_wool")
    settlement_data.setMaterialReplacement("terracota", "minecraft:" + color + "_terracota")
    settlement_data.setMaterialReplacement("carpet", "minecraft:" + color + "_carpet")
    settlement_data.setMaterialReplacement("stained_glass", "minecraft:" + color + "_stained_glass")
    settlement_data.setMaterialReplacement("shulker_box", "minecraft:" + color + "_shulker_box")
    settlement_data.setMaterialReplacement("glazed_terracota", "minecraft:" + color + "_glazed_terracotta")
    settlement_data.setMaterialReplacement("stained_glass_pane", "minecraft:" + color + "_stained_glass_pane")
    settlement_data.setMaterialReplacement("concrete", "minecraft:" + color + "_concrete")
    settlement_data.setMaterialReplacement("concrete_powder", "minecraft:" + color + "_concrete_powder")
    settlement_data.setMaterialReplacement("dye", "minecraft:" + color + "_dye")
    settlement_data.setMaterialReplacement("bed", "minecraft:" + color + "_bed")
    settlement_data.setMaterialReplacement("banner", "minecraft:" + color + "_banner")
    settlement_data.setMaterialReplacement("wall_banner", "minecraft:" + color + "_wall_banner")


def generateLoreAfterAllStructure(village: Village, name_generator):
    createListOfDeadVillager(village, name_generator)
    handleVillageDestroy(village)
    handleMurderer(village)
    generateOrders(village)


REASON_OF_DEATHS = ["died because of old age", "died of creeper attack", "died of skeleton attack",
                    "died of spider attack (he did not became Spider-Man)",
                    "died of zombie attack", "died of witch attack", "died suffocating from sand falling",
                    "died eating too much cake", "died crushing by a rock",
                    "died suffocating from gravel falling",
                    "disappeared for reasons still unclear"]

# Minimum of 10 deaths
def createListOfDeadVillager(village: Village, name_generator):
    random_dead_villagers = random.randint(10, max(len(village.villagers) - 1, 10))

    for i in range(random_dead_villagers):
        dead_villager: Villager = Villager(village)
        dead_villager.name = name_generator.generateVillagerName(True)
        village.dead_villagers.append(dead_villager)

        if village.status == "war" and random.randint(1, 3):
            village.dead_villagers[-1].reason_death = "died in war."
        else:
            random_death = random.randint(0, len(REASON_OF_DEATHS) - 1)
            village.dead_villagers[-1].reason_death = REASON_OF_DEATHS[random_death]

def isDestroyStructure(current_village: Village, lore_structure: LoreStructure):
    if current_village.isDestroyed:
        return {}

    result: dict = {}

    # Special structure to avoid destroying
    if "townhall" in lore_structure.name:
        return result

    # Can't destroy the mayor house
    for villager in lore_structure.villagers:
        if "Mayor" in villager.job:
            return result

    # More chance if near war
    if current_village.status == "war":
        chance: float = computeChanceOfDestructionComparingTier(current_village)

        if random.randint(1, 20 * chance) == 1:
            result["burned"] = "war"
        if random.randint(1, 30 * chance) == 1:
            result["abandoned"] = "flight"
        if random.randint(1, 30 * chance) == 1:
            result["damaged"] = "war"

    if random.randint(1, 50) == 1 and "burned" not in result.keys():
        if random.randint(1, 2) == 1:
            result["burned"] = "storm"
        else:
            result["burned"] = "accident"
    if random.randint(1, 50) == 1 and "abandoned" not in result.keys():
        result["abandoned"] = "death"

    return result

    # Check relation if in war with more advanced civilization


def computeChanceOfDestructionComparingTier(current_village: Village) -> float:
    chance: float = 1

    for key in current_village.village_interactions:
        interaction: VillageInteraction = current_village.village_interactions[key]
        if interaction.state != VillageInteraction.STATE_WAR:
            continue

        village2: Village = interaction.village2 if interaction.village2 != current_village else interaction.village1

        if current_village.tier < village2.tier:
            return 0.6
        elif current_village.tier == village2.tier:
            chance = 0.8

    return chance


def applyStructureDestroy(current_village: Village, lore_structure: LoreStructure):
    if lore_structure.type == LoreStructure.TYPE_HOUSES:
        for villager in lore_structure.villagers:
            if villager.job == "Unemployed":
                current_village.free_villager -= len(lore_structure.villagers)

            current_village.villagers.remove(villager)
            current_village.dead_villagers.append(villager)

    else:
        for villager in lore_structure.villagers:
            villager.job = "Unemployed"
            villager.minecraftJob = "nitwit"


def handleVillageDestroy(current_village: Village):
    if not current_village.isDestroyed:
        return

    for lore_structure in current_village.lore_structures:
        causes: list
        if current_village.destroyCause == "war":
            causes = util.selectNWithChanceForOther(["burned", "damaged", "abandoned"], [0.4, 0.3, 0.3], 1)
        elif current_village.destroyCause == "pillager":
            causes = util.selectNWithChanceForOther(["burned", "damaged", "abandoned"], [0.2, 0.2, 0.2], 2)
        else:
            causes = util.selectNWithChanceForOther(["burned", "damaged", "abandoned"], [0.4, 0.3, 0.3], 0)

        for one_cause in causes:
            lore_structure.causeDestroy[one_cause] = current_village.destroyCause

        lore_structure.destroyed = True


def handleMurderer(village: Village):
    if village.status != village.STATE_WAR:
        return

    # Murderer
    if len(village.villagers) <= 1:
        return

    village.murderer_data.villagerMurderer = village.villagers[
        random.choice(
            [i for i in range(0, len(village.villagers)) if village.villagers[i].job != "Mayor"])]

    village.murderer_data.villagerTarget = village.villagers[
        random.choice(
            [i for i in range(0, len(village.villagers))
             if village.villagers[i] != village.murderer_data.villagerMurderer])]

    for structureData in village.lore_structures:
        if village.murderer_data.villagerTarget in structureData.villagers:
            structureData.gift = "minecraft:tnt"


def generateOrders(village: Village):
    for structure in village.lore_structures:
        if structure.type != LoreStructure.TYPE_FUNCTIONALS:
            return

        orders: list = []
        # Between (0, 1); (0, 2) or (0, 3)
        number: int = random.randint(0, village.tier + 1)

        size: int = len(village.villagers)
        # Order for
        for j in range(min(number, size)):

            villager: Villager = village.villagers[
                random.choice(
                    [i for i in range(size) if
                     village.villagers[i] not in structure.villagers and village.villagers[i] not in orders])]

            orders.append(villager)

        for ordering in orders:
            print(ordering.name)
            structure.addOrder(ordering, "uninitialized", 0)
