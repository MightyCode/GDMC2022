from generation.data.villager import Villager
from generation.data.village import Village

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

"""
Return the text of the book of the village presentation
"""


def createTextOfPresentationVillage(villageName: str, structuresNumber: int, structures: list, deadVillagersNumber: int,
                                    villages: list):
    text_village_presentation_book = (
        '\\\\s--------------\\\\n'
        ' \\\\n'
        ' \\\\n'
        'Welcome to\\\\n'
        f'{villageName}\\\\n'
        ' \\\\n'
        ' \\\\n'
        ' \\\\n'
        ' \\\\n'
        ' \\\\n'
        ' \\\\n'
        ' \\\\n'
        '--------------')
    text_village_presentation_book += '\f\\\\s---------------\\\\n'

    number_of_house = 0
    for structure in structures:
        if "house" in structure.name:
            number_of_house += 1

    text_village_presentation_book += (f'{len(villages)} villagers arrived in '
                                       f'{number_of_house} houses.\\\\n')
    text_village_presentation_book += f'{deadVillagersNumber} villagers have died since their arrival.\\\\n'
    text_village_presentation_book += ('There are '
                                       f'{structuresNumber} structures.\\\\n')
    text_village_presentation_book += '---------------\\\\n\f'

    for structure in structures:
        text_village_presentation_book += f'Villagers built the {structure.name}.\\\\n'

    return text_village_presentation_book


"""
Return the text of the book of the villagers names and professions
"""


def createTextForVillagersNames(villagers: list):
    text_villager_names = 'Registry of living villagers \\\\n'

    villager_text: str
    i = 0
    for villager in villagers:
        villager_text = villager.name + " : " + villager.job

        text_villager_names += f'-{villager_text}\\\\n'

    text_villager_names += '\f'

    return text_villager_names


"""
Return the text of the book of the dead villagers names and professions
"""


def createTextForDeadVillagers(villagers: list, deadVillagers: list):
    number_of_dead = len(deadVillagers)

    names = []
    for villager in villagers:
        names.append(villager.name)

    text_dead_villagers = 'Registry of dead villagers \\\\n'

    for deadVillager in deadVillagers:
        random_death = rd.randint(0, len(REASON_OF_DEATHS) - 1)
        if deadVillager.name in names:
            text_dead_villagers += ('-'
                                    f'{deadVillager.name} Senior : '
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

    text_diary_villager = (
        '\\\\s--------------\\\\n'
        '                      \\\\n'
        '                      \\\\n'
        f'{villager_name} diary\\\\n'
        '                      \\\\n'
        '                      \\\\n'
        '                      \\\\n'
        '                      \\\\n'
        '                      \\\\n'
        '                      \\\\n'
        '--------------')
    text_diary_villager += '     \f'

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
                    text_diary_villager += f'I love {targeted_villager.name}\\\\n'
                else:
                    text_diary_villager += f'{targeted_villager.name} is my best friend\\\\n'

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
                    text_diary_villager += f'I would like to work as a {Villager.VILLAGE_PROFESSION_LIST[secondRandomProfession]}.\\\\n '
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


def createBookForAdventurerHouse(flip):
    flint_place = "right" if flip > 0 else "left"
    bucket_place = "left " if flip > 0 else "right"

    text_adventurer_book = (
        '\\\\s-------------------\\\\n'
        'Machine guide:  \\\\n'
        f'Place flint and steal {flint_place} in the machine. Place water bucket in the {bucket_place} machine. \\\\n'
        '                      \\\\n'
        '                      \\\\n'
        '                      \\\\n'
        '                      \\\\n'
        '                      \\\\n'
        '                      \\\\n'
        '                      \\\\n'
        '-------------------')
    text_adventurer_book += '\f'

    return text_adventurer_book
