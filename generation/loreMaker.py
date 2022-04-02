import random

import utils.util as util
from representation.village import Village
from representation.villager import Villager
from representation.village import VillageInteraction
from representation.loreStructure import LoreStructure


def gen_position_of_village(existing_areas: list, goal_number: int) -> list:
    positions: list = []

    for area in existing_areas:
        positions.append([int((area[0] + area[3]) / 2),
                          int((area[2] + area[5]) / 2)])

    remaining_index_start: int = len(existing_areas)

    for i in range(goal_number - remaining_index_start):
        random_index: int = random.randint(0, len(positions) - 1)
        positions.append([positions[random_index][0] - 500, positions[random_index][0] + 500,
                          positions[random_index][1] - 500, positions[random_index][1] + 500])

    return positions


def initializedVillages(positions_of_villages: list, nameGenerator) -> list:
    villages: list = []

    for i in range(len(positions_of_villages)):
        villages.append(Village())
        villages[i].position = positions_of_villages[i]
        villages[i].generateVillageInformation(nameGenerator)
        villages[i].generateVillageLore()

        voteForColor(villages[i])

    return villages


def createVillageRelationAndAssign(villages: list) -> VillageInteraction:
    interactions: list = []
    otherVillages = villages.copy()
    del otherVillages[0]

    for i in range(len(villages) - 1):
        villages[i].makeRelations(otherVillages)
        for villageId in villages[i].village_interactions.keys():
            interactions.append(villages[i].village_interactions[villageId])

        del otherVillages[0]

    for village in villages:
        village.generateLoreAfterRelation()

    return interactions


def checkForImpossibleInteractions(villages: list, interactions: list):
    """Check for two enemy villages if they are friend with same village"""

    villageToCheck = villages.copy()
    random.shuffle(villageToCheck)

    for village in villageToCheck:
        for interaction in interactions:
            if village == interaction.village1 or village == interaction.village2:
                continue

            if interaction.state != VillageInteraction.STATE_WAR:
                continue

            interaction1 = village.village_interactions[interaction.village1]
            interaction2 = village.village_interactions[interaction.village2]

            if (
                    interaction1.state != VillageInteraction.STATE_LOVE and interaction1.state != VillageInteraction.STATE_FRIENDSHIP) or \
                    (
                            interaction2.state != VillageInteraction.STATE_LOVE and interaction2.state != VillageInteraction.STATE_FRIENDSHIP):
                continue

            if random.randint(0, 1) == 1:
                interaction1.state = VillageInteraction.STATE_NEUTRAL
                interaction1.brokeTheirRelation = True
                interaction1.reason = VillageInteraction.REASON_TWO_FRIENDS_WENT_IN_WAR
                # print("Relation between " + interaction1.village1.name + " " + interaction1.village2.name + " broken")
            else:
                interaction2.state = VillageInteraction.STATE_NEUTRAL
                interaction2.brokeTheirRelation = True
                interaction2.reason = VillageInteraction.REASON_TWO_FRIENDS_WENT_IN_WAR
                # print("Relation between " + interaction2.village1.name + " " + interaction2.village2.name + " broken")


def generateLoreAfterRelation(villages: list):
    orderToCheck: list = villages.copy()
    random.shuffle(orderToCheck)

    for village in orderToCheck:
        if village.status == "peaceful":
            village.isDestroyed = random.randint(1, 10) == 1

            if village.isDestroyed:
                village.destroyCause = "pillager" if random.randint(1, 2) == 1 else "abandonned"
        else:
            village.destroyCause = "war"
            chance: int = computeChanceOfDestructionComparingTier(village)

            if chance == 0.8:
                village.isDestroyed = random.randint(1, 3) == 1
            elif chance == 0.6:
                village.isDestroyed = random.randint(1, 4) != 4


def alterSettlementDataWithNewStructures(settlementData, lore_structure: LoreStructure):
    result: dict = isDestroyStructure(settlementData.village_model, lore_structure)
    if result != {}:
        print("DESTRUCTED STRUCTURE")
        lore_structure.destroyed = True
        lore_structure.causeDestroy = result
        applyStructureDestroy(settlementData.village_model, lore_structure)


def applyLoreToSettlementData(settlementData):
    fillSettlementDataWithColor(settlementData, settlementData.village_model.color)


def voteForColor(village):
    colors = ["white", "orange", "magenta", "light_blue", "yellow", "lime", "pink", "gray", "light_gray", "cyan",
              "purple", "blue", "brown", "green", "red", "black"]

    village.color = colors[random.randint(0, len(colors) - 1)]


def fillSettlementDataWithColor(settlementData, color):
    settlementData.setMaterialReplacement("color", color)
    settlementData.setMaterialReplacement("wool", "minecraft:" + color + "_wool")
    settlementData.setMaterialReplacement("terracota", "minecraft:" + color + "_terracota")
    settlementData.setMaterialReplacement("carpet", "minecraft:" + color + "_carpet")
    settlementData.setMaterialReplacement("stained_glass", "minecraft:" + color + "_stained_glass")
    settlementData.setMaterialReplacement("shulker_box", "minecraft:" + color + "_shulker_box")
    settlementData.setMaterialReplacement("glazed_terracota", "minecraft:" + color + "_glazed_terracota")
    settlementData.setMaterialReplacement("stained_glass_pane", "minecraft:" + color + "_stained_glass_pane")
    settlementData.setMaterialReplacement("concrete", "minecraft:" + color + "_concrete")
    settlementData.setMaterialReplacement("concrete_powder", "minecraft:" + color + "_concrete_powder")
    settlementData.setMaterialReplacement("dye", "minecraft:" + color + "_dye")
    settlementData.setMaterialReplacement("bed", "minecraft:" + color + "_bed")
    settlementData.setMaterialReplacement("banner", "minecraft:" + color + "_banner")
    settlementData.setMaterialReplacement("wall_banner", "minecraft:" + color + "_wall_banner")


# Minimum of 10 deaths
def createListOfDeadVillager(village: Village, nameGenerator):
    randomOfDeadVillagers = random.randint(10, max(len(village.villagers) - 1, 10))

    for i in range(randomOfDeadVillagers):
        dead_villager: Villager = Villager(village)
        dead_villager.name = nameGenerator.generateVillagerName(True)
        village.dead_villagers.append(dead_villager)


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


def computeChanceOfDestructionComparingTier(current_village: Village):
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

