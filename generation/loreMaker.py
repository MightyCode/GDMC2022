import random
from representation.village import Village
from representation.village import VillageInteraction


def initializedVillages(number_of_village: int, nameGenerator) -> list:
    villages: list = []

    for i in range(number_of_village):
        villages.append(Village())
        villages[i].generateVillageInformation(nameGenerator)
        villages[i].defineTierAndAge()

    return villages


def createVillageRelationAndAssign(villages: list) -> VillageInteraction:
    interactions: list = []
    otherVillages = villages.copy()
    del otherVillages[0]

    for i in range(len(villages) - 1):
        villages[i].makeRelations(otherVillages)
        for villageId in villages[i].villageInteractions.keys():
            interactions.append(villages[i].villageInteractions[villageId])

        del otherVillages[0]

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

            interaction1 = village.villageInteractions[interaction.village1]
            interaction2 = village.villageInteractions[interaction.village2]

            if (interaction1.state != VillageInteraction.STATE_LOVE and interaction1.state != VillageInteraction.STATE_FRIENDSHIP) or \
                    (interaction2.state != VillageInteraction.STATE_LOVE and interaction2.state != VillageInteraction.STATE_FRIENDSHIP):
                continue

            if random.randint(0, 1) == 1:
                interaction1.state = VillageInteraction.STATE_NEUTRAL
                interaction1.brokeTheirRelation = True
                print("Relation between " + interaction1.village1.name + " " + interaction1.village2.name + " broken")
            else:
                interaction2.state = VillageInteraction.STATE_NEUTRAL
                interaction2.brokeTheirRelation = True
                print("Relation between " + interaction2.village1.name + " " + interaction2.village2.name + " broken")


def alterSettlementDataWithNewStructures(settlementData, structure):
    if structure.name == "basictownhall":
        voteForColor(settlementData)


def voteForColor(settlementData):
    colors = ["white", "orange", "magenta", "light_blue", "yellow", "lime", "pink", "gray", "light_gray", "cyan",
              "purple", "blue", "brown", "green", "red", "black"]
    color = colors[random.randint(0, len(colors) - 1)]

    settlementData.village_model.color = color

    fillSettlementDataWithColor(settlementData, color)


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
