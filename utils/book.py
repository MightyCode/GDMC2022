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


def createTextOfPresentationVillage(village_name: str, structures_number: int, structures: list,
                                    dead_villagers_number: int, villages: list):
    text_village_presentation_book = (
        '\\\\s--------------\\\\n'
        '                      \\\\n'
        '                      \\\\n'
        '   Welcome to      \\\\n'
        f'{village_name} \\\\n'
        '                      \\\\n'
        '                      \\\\n'
        '                      \\\\n'
        '                      \\\\n'
        '                      \\\\n'
        '                      \\\\n'
        '                      \\\\n'
        '--------------')
    text_village_presentation_book += '\f\\\\s---------------\\\\n'

    number_of_house = 0
    for structure in structures:
        if "house" in structure.name:
            number_of_house += 1

    text_village_presentation_book += (f'{len(villages)} villagers arrived in '
                                       f'{number_of_house} houses \\\\n')
    text_village_presentation_book += f'{dead_villagers_number} villagers have died since their arrival. \\\\n'
    text_village_presentation_book += (''
                                       'There are '
                                       f'{structures_number} structures. \\\\n')
    text_village_presentation_book += '---------------\\\\n\f'

    i: int = 0
    for structure in structures:
        if i % 3 == 0 and i != 0:
            text_village_presentation_book += '\f'
        else:
            text_village_presentation_book += ('Villagers built the '
                                               f'{structure.name} \\\\n')

        i += 1
    return text_village_presentation_book


"""
Return the text of the book of the villagers names and professions
"""


def createTextForVillagersNames(villagers: list):
    text_villager_names = 'Registry of living villagers \\\\n'

    village_str: str
    i = 0
    for villager in villagers:
        village_str = villager.name + " : " + villager.job

        if i <= 3:
            text_villager_names += ('-'
                                    f'{village_str}       \\\\n')
        if i % 4 == 0 and i != 0:
            text_villager_names += '\f'
        if i >= 4:
            text_villager_names += ('-'
                                    f'{village_str}       \\\\n')

        i += 1

    text_villager_names += '\f'

    return text_villager_names


"""
Return the text of the book of the dead villagers names and professions
"""


def createTextForDeadVillagers(villagers: list, dead_villagers: list):
    number_of_dead = len(dead_villagers)

    names = []
    for villager in villagers:
        names.append(villager.name)

    text_dead_villagers = 'Registry of dead villagers \\\\n'

    i = 0
    for deadVillager in dead_villagers:
        random_death = rd.randint(0, len(REASON_OF_DEATHS) - 1)
        if deadVillager.name in names:
            text_dead_villagers += ('-'
                                    f'{deadVillager.name} Senior : '
                                    f'{REASON_OF_DEATHS[random_death]} \\\\n')
        if i <= 2:
            if i == 2:
                text_dead_villagers += ('-'
                                        f'{deadVillager.name} : '
                                        f'{REASON_OF_DEATHS[0]} \\\\n')
            else:
                text_dead_villagers += ('-'
                                        f'{deadVillager.name} : '
                                        f'{REASON_OF_DEATHS[random_death]} \\\\n')
        if i % 3 == 0 and i != 0:
            text_dead_villagers += '\f'
        if i >= 3:
            text_dead_villagers += ('-'
                                    f'{deadVillager.name} : '
                                    f'{REASON_OF_DEATHS[random_death]} \\\\n')

        i += 1
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
        f'{villager_name} diary  \\\\n'
        '                      \\\\n'
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
            text_diary_villager += '                      \\\\n'
            if rd.randint(1, 2) == 1:
                text_diary_villager += '                      \\\\n'

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
                    text_diary_villager += f'{targeted_villager.name} is a jerk\\\\n'

                if rd.randint(1, 2) == 1:
                    text_diary_villager += ', I placed a tnt under the door.\\\\n'
                else:
                    text_diary_villager += ', I put a deadly trap under the door.\\\\n'
            continue

        # Murderer suspicion
        murderer_data = village_model.murderer_data
        if rd.randint(1, 5) == 1 and not murderer_suspicious and murderer_data.villagerMurderer is not None:
            text_diary_villager += f'I think that {murderer_data.villagerMurderer.name} is really strange. \\\\n'
            murderer_suspicious = True
            continue

        # Other phrase    
        random = rd.randint(1, 5)
        if random == 1:
            random_profession = rd.randint(0, len(Villager.VILLAGE_PROFESSION_LIST) - 1)
            text_diary_villager += f'I hate all {Villager.VILLAGE_PROFESSION_LIST[random_profession]} \\\\n'
            if rd.randint(1, 5) == 1:
                second_random_profession = rd.randint(0, len(Villager.VILLAGE_PROFESSION_LIST) - 1)
                if second_random_profession != random_profession:
                    text_diary_villager += f'I would like to work as a {Villager.VILLAGE_PROFESSION_LIST[second_random_profession]}.\\\\n '
        elif random == 2 and not target_text_done:
            random_diary_text_with_target = rd.randint(0, len(new_diary_text_with_target) - 1)

            targeted = -1

            if len(village_model.dead_villagers) == 1:
                targeted = 0
            elif len(village_model.dead_villagers) > 1:
                targeted = village_model.dead_villagers[rd.randint(0, len(village_model.dead_villagers) - 1)].name

            if targeted != -1:
                text_diary_villager += (f'{new_diary_text_with_target[random_diary_text_with_target]}'
                                        f'{targeted}.  \\\\n')

            new_diary_text_with_target.remove(new_diary_text_with_target[random_diary_text_with_target])
            target_text_done = True
        else:
            random_diary_text_without_target = rd.randint(0, len(new_diary_text_without_target) - 1)
            text_diary_villager += f'{new_diary_text_without_target[random_diary_text_without_target]}   \\\\n'
            new_diary_text_without_target.remove(new_diary_text_without_target[random_diary_text_without_target])

        if i % 4 == 0:
            text_diary_villager += ' \f'

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
