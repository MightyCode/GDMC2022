from generation.data.villager import Villager
from generation.data.village import Village
from generation.data.loreStructure import LoreStructure
from generation.data.villageInteraction import VillageInteraction

import generation.generator as generator

import random as rd

REASON_OF_DEATHS = ["murdered", "died because of old age", "died of creeper attack", "died of skeleton attack",
                    "died of spider attack (he did not became Spider-Man)",
                    "died of zombie attack", "died of witch attack", "died suffocating from sand falling",
                    "died eating too much cake", "died crushing by a rock",
                    "died suffocating from gravel falling"]
DIARY_TEXTS_WITHOUT_TARGETS = [" I really like the color of the village. ", " I really like the name of the village. ",
                               " I hate the color of the village.",
                               " I am afraid of spiders. ", " I am afraid of creppers. ", " I am afraid of zombies. ",
                               " I am afraid of skeletons. ",
                               " I don't like the facade of my house. ", " I don't like the flower of the village. ",
                               " I really like the flower of the village. ", " I really like the mayor. ",
                               " I hate the flower of the village. ", " I hate the mayor. ",
                               " I would like to have a better house. ",
                               " I hope he finds the gift I left him under his door. ",
                               " I really like pigs. ", " I really like cows. ", " I am interested about sheeps.  ",
                               " I am interested about chickens. "]
DIARY_TEXTS_WITH_TARGETS = [" I am sad since the death of ", " I am happy since the death of ", " I used to hate ",
                            " I once hit "]

VILLAGER_NAME_PATH = "data/names/"

MIN_SIZE = 4
MAX_SIZE = 15


def returnFirstPage(message: str, title: str) -> str:
    return ('\\\\s------------------'
            ' \\\\n'
            ' \\\\n'
            f'{message}\\\\n'
            ' \\\\n'
            f'{title} \\\\n'
            ' \\\\n'
            ' \\\\n'
            ' \\\\n'
            ' \\\\n'
            ' \\\\n'
            ' \\\\n'
            '-------------------\f\\\\s')


def villageMessage(village_name: str) -> str:
    return "-" + village_name + " settlement-"


"""
Return the text of the book of the village presentation
"""


def createTextOfPresentationVillage(village: Village):
    text_village_presentation_book = returnFirstPage("Welcome to :", village.name)

    # Status of the village
    number_structure_destroyed: int = 0
    number_house: int = 0

    for structure in village.lore_structures:
        if structure.destroyed:
            number_structure_destroyed += 1
        elif structure.type == LoreStructure.TYPE_HOUSES:
            number_house += 1

    # Status of the village relationship

    text_village_presentation_book += '-------------------\\\\n'
    text_village_presentation_book += 'Village relationships: \\\\n'
    text_village_presentation_book += f'Status of {village.name} : {village.status}\\\\n'

    hadBrokeARelation: bool = False

    for village_key in village.village_interactions:
        interaction: VillageInteraction = village.village_interactions[village_key]

        if interaction.brokeTheirRelation:
            hadBrokeARelation = True

        if interaction.state == interaction.STATE_WAR:
            text_village_presentation_book += "In war with "
        elif interaction.state == interaction.STATE_TENSION:
            text_village_presentation_book += "Got tension with "
        elif interaction.state == interaction.STATE_FRIENDSHIP:
            text_village_presentation_book += "Friendship relation with "
        elif interaction.state == interaction.STATE_LOVE:
            text_village_presentation_book += "Very close relation with "

        if interaction.state != interaction.STATE_NEUTRAL:
            text_village_presentation_book += f'{village_key.name}. \\\\n'

    if hadBrokeARelation:
        text_village_presentation_book += f'Due to the war, {village.name} had broke their relation with '
        for village_key in village.village_interactions:
            interaction: VillageInteraction = village.village_interactions[village_key]

            if interaction.brokeTheirRelation:
                text_village_presentation_book += village_key.name + " "

    text_village_presentation_book += " \\\\n"

    text_village_presentation_book += '-------------------\\\\n'
    text_village_presentation_book += "\f\\\\s"


    # Stats on the village
    text_village_presentation_book += '-------------------\\\\n'

    text_village_presentation_book += f'There are {len(village.lore_structures)} structures.\\\\n'
    text_village_presentation_book += ('The population of the village is composed of '
                                       f'{len(village.villagers)} villagers.\\\\n'
                                       f'They are living on {number_house} houses.\\\\n')
    text_village_presentation_book += f'{len(village.dead_villagers)} villagers have died since their arrival.\\\\n'
    text_village_presentation_book += f'{number_structure_destroyed} structures are destroyed.\\\\n'
    text_village_presentation_book += '-------------------\\\\n\f\\\\s'

    text_village_presentation_book += "List of structures : \\\\n"
    for structure in village.lore_structures:
        text_village_presentation_book += f'Villagers built the {structure.name}.\\\\n'

    return text_village_presentation_book


"""
Return the text of the book of the villagers names and professions
"""


def createTextForVillagersNames(village_name: str, villagers: list):
    text_villager_names = returnFirstPage(villageMessage(village_name), "Registry of living villagers.")

    villager_text: str
    i = 0
    for villager in villagers:
        villager_text = villager.name + " : " + villager.job

        text_villager_names += f'-{villager_text} \\\\n'

    text_villager_names += '\f'

    return text_villager_names


"""
Return the text of the book of the dead villagers names and professions
"""


def createTextForDeadVillagers(village_name: str, villagers: list, deadVillagers: list):
    number_of_dead = len(deadVillagers)

    names = []
    for villager in villagers:
        names.append(villager.name)

    text_dead_villagers = returnFirstPage(villageMessage(village_name), "Registry of dead villagers.")

    for deadVillager in deadVillagers:
        random_death = rd.randint(0, len(REASON_OF_DEATHS) - 1)
        if deadVillager.name in names:
            text_dead_villagers += (f'-{deadVillager.name} Senior : '
                                    f'{REASON_OF_DEATHS[random_death]} \\\\n')

        text_dead_villagers += (f'-{deadVillager.name} : '
                                f'{REASON_OF_DEATHS[random_death]} \\\\n')

    text_dead_villagers += '\f'

    return [text_dead_villagers, number_of_dead]


def createBookForVillager(village_model: Village, villager: Villager) -> list:
    villager_name: str = villager.name
    gift: str = ""

    # 1 / 2 chance to a gift
    random_gift = rd.randint(1, 4)
    if random_gift == 1:
        gift = "minecraft:gold_block"
    elif random_gift == 2:
        gift = "minecraft:tnt"

    gift_place = rd.randint(1, 3)

    text_diary_villager = returnFirstPage(villager_name + " diary", "")

    new_diary_text_without_target = DIARY_TEXTS_WITHOUT_TARGETS.copy()
    new_diary_text_with_target = DIARY_TEXTS_WITH_TARGETS.copy()
    target_text_done = False
    murderer_suspicious = False

    number_phrase = rd.randint(3, 7)
    for i in range(number_phrase):
        # Spaces
        if rd.randint(1, 2) == 1:
            text_diary_villager += ' \\\\n'

        available_indices: list = generator.returnVillagerAvailableForGift(village_model, [villager])

        # Gift phrase
        if i == gift_place and len(available_indices) >= 1:
            targeted_villager: Villager = available_indices[rd.randint(0, len(available_indices) - 1)]

            if random_gift == 1:
                if rd.randint(1, 2) == 1:
                    text_diary_villager += f'I love {targeted_villager.name}'
                else:
                    text_diary_villager += f'{targeted_villager.name} is my best friend'

                if rd.randint(1, 2) == 1:
                    text_diary_villager += ', I left a surprise under the door.\\\\n'
                else:
                    text_diary_villager += ', I hope my lover will finds the gift I left him under the door.\\\\n'

            elif random_gift == 2:
                if rd.randint(1, 2) == 1:
                    text_diary_villager += f'I hate {targeted_villager.name}\\\\n'
                else:
                    text_diary_villager += f'{targeted_villager.name} is a jerk.\\\n'

                if rd.randint(1, 2) == 1:
                    text_diary_villager += ', I placed a tnt under the door.\\\\n'
                else:
                    text_diary_villager += ', I put a deadly trap under the door.\\\\n'
            continue

        # Murderer suspicion
        murdererData = village_model.murderer_data
        if rd.randint(1, 5) == 1 and not murderer_suspicious and murdererData.villagerMurderer is not None:
            text_diary_villager += f'I think that {murdererData.villagerMurderer.name} is really strange. \\\\n'
            murderer_suspicious = True
            continue

        # Other phrase    
        random = rd.randint(1, 5)
        if random == 1:
            randomProfession = rd.randint(0, len(Villager.VILLAGE_PROFESSION_LIST) - 1)
            text_diary_villager += f'I hate all {Villager.VILLAGE_PROFESSION_LIST[randomProfession]} \\\\n'
            if rd.randint(1, 5) == 1:
                secondRandomProfession = rd.randint(0,
                                                    len(Villager.VILLAGE_PROFESSION_LIST) - 1)
                if secondRandomProfession != randomProfession:
                    text_diary_villager += \
                        f'I would like to work as a {Villager.VILLAGE_PROFESSION_LIST[secondRandomProfession]}.\\\\n '
        elif random == 2 and not target_text_done:
            randomDiaryTextWithTarget = rd.randint(0, len(new_diary_text_with_target) - 1)

            targeted = -1

            if len(village_model.dead_villagers) == 1:
                targeted = 0
            elif len(village_model.dead_villagers) > 1:
                targeted = village_model.dead_villagers[rd.randint(0, len(village_model.dead_villagers) - 1)].name

            if targeted != -1:
                text_diary_villager += (f'{new_diary_text_with_target[randomDiaryTextWithTarget]}'
                                        f'{targeted}.\\\\n')

            new_diary_text_with_target.remove(new_diary_text_with_target[randomDiaryTextWithTarget])
            target_text_done = True
        else:
            randomDiaryTextWithoutTarget = rd.randint(0, len(new_diary_text_without_target) - 1)
            text_diary_villager += f'{new_diary_text_without_target[randomDiaryTextWithoutTarget]}\\\\n'
            new_diary_text_without_target.remove(new_diary_text_without_target[randomDiaryTextWithoutTarget])

    return [text_diary_villager, gift]


def createBookForAdventurerHouse(village_name: str, flip: int):
    flint_place = "right" if 0 < flip < 3 else "left"
    bucket_place = "left " if 0 < flip < 3 else "right"

    text_adventurer_book = returnFirstPage(villageMessage(village_name), "Machine guide.")

    text_adventurer_book += (
        '-------------------\\\\n'
        'Instructions:  \\\\n'
        f'1. Place flint and steal in the {flint_place} machine.\\\\n'
        f'2. Place water bucket in the {bucket_place} machine.\\\\n'
        '-------------------')

    return text_adventurer_book
