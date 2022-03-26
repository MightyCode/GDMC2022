from utils.nameGenerator import NameGenerator
from representation.villager import Villager
from representation.village import Village

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
                                    listOfVillagers):
    textVillagePresentationBook = (
        '\\\\s--------------\\\\n'
        '                      \\\\n'
        '                      \\\\n'
        '   Welcome to      \\\\n'
        f' {villageName} \\\\n'
        '                      \\\\n'
        '                      \\\\n'
        '                      \\\\n'
        '                      \\\\n'
        '                      \\\\n'
        '                      \\\\n'
        '                      \\\\n'
        '--------------')
    textVillagePresentationBook += '\f\\\\s---------------\\\\n'

    numberOfHouse = 0
    for structure in structures:
        if "house" in structure.name:
            numberOfHouse += 1

    textVillagePresentationBook += (f'{len(listOfVillagers)} villagers arrived in '
                                    f'{numberOfHouse} houses \\\\n')
    textVillagePresentationBook += f'{deadVillagersNumber} villagers have died since their arrival. \\\\n'
    textVillagePresentationBook += (''
                                    'There are '
                                    f'{structuresNumber} structures. \\\\n')
    textVillagePresentationBook += '---------------\\\\n\f'

    i: int = 0
    for structure in structures:
        if i % 3 == 0 and i != 0:
            textVillagePresentationBook += '\f'
        else:
            textVillagePresentationBook += ('Villagers built the '
                                            f'{structure.name} \\\\n')

        i += 1
    return textVillagePresentationBook


"""
Return the text of the book of the villagers names and professions
"""


def createTextForVillagersNames(listOfVillagers):
    textVillagerNames = 'Registry of living villagers \\\\n'
    for i in range(len(listOfVillagers)):
        if i <= 3:
            textVillagerNames += ('-'
                                  f'{listOfVillagers[i]}       \\\\n')
        if i % 4 == 0 and i != 0:
            textVillagerNames += '\f'
        if i >= 4:
            textVillagerNames += ('-'
                                  f'{listOfVillagers[i]}       \\\\n')
    textVillagerNames += '\f'

    return textVillagerNames


"""
Return the text of the book of the dead villagers names and professions
"""


def createTextForDeadVillagers(listOfVillagers: list, nameGenerator: NameGenerator):
    randomOfDeadVillagers = rd.randint(1, len(listOfVillagers) - 1)

    data = {"listOfDeadVillagers": []}
    for i in range(randomOfDeadVillagers):
        data["listOfDeadVillagers"].append(nameGenerator.generateVillagerName(True))
    listOfVillagersWithoutJob = [i.split(':', 1)[0] for i in listOfVillagers]
    textDeadVillagers = 'Registry of dead villagers \\\\n'

    for i in range(len(data["listOfDeadVillagers"])):
        deadVillager = data["listOfDeadVillagers"][i]
        randomDeath = rd.randint(0, len(REASON_OF_DEATHS) - 1)
        if deadVillager in listOfVillagersWithoutJob:
            textDeadVillagers += ('-'
                                  f'{deadVillager} Senior : '
                                  f'{REASON_OF_DEATHS[randomDeath]} \\\\n')
        if i <= 2:
            if i == 2:
                textDeadVillagers += ('-'
                                      f'{deadVillager} : '
                                      f'{REASON_OF_DEATHS[0]} \\\\n')
            else:
                textDeadVillagers += ('-'
                                      f'{deadVillager} : '
                                      f'{REASON_OF_DEATHS[randomDeath]} \\\\n')
        if i % 3 == 0 and i != 0:
            textDeadVillagers += '\f'
        if i >= 3:
            textDeadVillagers += ('-'
                                  f'{deadVillager} : '
                                  f'{REASON_OF_DEATHS[randomDeath]} \\\\n')
    textDeadVillagers += '\f'

    return [textDeadVillagers, randomOfDeadVillagers, data["listOfDeadVillagers"]]


def createBookForVillager(village_model: Village, villager: Villager) -> list:
    villagerName: str = villager.name
    gift: str = ""

    # 1 / 2 chance to a gift
    randomGift = rd.randint(1, 4)
    if randomGift == 1:
        gift = "minecraft:gold_block"
    elif randomGift == 2:
        gift = "minecraft:tnt"

    giftPlace = rd.randint(1, 3)

    textDiaryVillager = (
        '\\\\s--------------\\\\n'
        '                      \\\\n'
        '                      \\\\n'
        f'{villagerName} diary  \\\\n'
        '                      \\\\n'
        '                      \\\\n'
        '                      \\\\n'
        '                      \\\\n'
        '                      \\\\n'
        '                      \\\\n'
        '                      \\\\n'
        '--------------')
    textDiaryVillager += '     \f'

    newDiaryTextWithoutTarget = DIARY_TEXTS_WITHOUT_TARGETS.copy()
    newDiaryTextWithTarget = DIARY_TEXTS_WITH_TARGETS.copy()
    targetTextDone = False
    murdererSuspicious = False

    numberPhrase = rd.randint(3, 7)
    for i in range(numberPhrase):
        # Spaces
        if rd.randint(1, 2) == 1:
            textDiaryVillager += '                      \\\\n'
            if rd.randint(1, 2) == 1:
                textDiaryVillager += '                      \\\\n'

        availableIndices: list = generator.returnVillagerAvailableForGift(village_model, [villager])

        # Gift phrase
        if i == giftPlace and len(availableIndices) >= 1:
            targetedVillager: Villager = availableIndices[rd.randint(0, len(availableIndices) - 1)]

            if randomGift == 1:
                if rd.randint(1, 2) == 1:
                    textDiaryVillager += f'I love {targetedVillager.name}\\\\n'
                else:
                    textDiaryVillager += f'{targetedVillager.name} is my best friend\\\\n'

                if rd.randint(1, 2) == 1:
                    textDiaryVillager += ', I left a surprise under the door.\\\\n'
                else:
                    textDiaryVillager += ', I hope my lover will finds the gift I left him under the door.\\\\n'

            elif randomGift == 2:
                if rd.randint(1, 2) == 1:
                    textDiaryVillager += f'I hate {targetedVillager.name}\\\\n'
                else:
                    textDiaryVillager += f'{targetedVillager.name} is a jerk\\\\n'

                if rd.randint(1, 2) == 1:
                    textDiaryVillager += ', I placed a tnt under the door.\\\\n'
                else:
                    textDiaryVillager += ', I put a deadly trap under the door.\\\\n'
            continue

        # Murderer suspicion
        murdererData = village_model.murderer_data
        if rd.randint(1, 5) == 1 and not murdererSuspicious and murdererData.villagerMurderer is not None:
            textDiaryVillager += f'I think that {murdererData.villagerMurderer.name} is really strange. \\\\n'
            murdererSuspicious = True
            continue

        # Other phrase    
        random = rd.randint(1, 5)
        if random == 1:
            randomProfession = rd.randint(0, len(Villager.VILLAGE_PROFESSION_LIST) - 1)
            textDiaryVillager += f'I hate all {Villager.VILLAGE_PROFESSION_LIST[randomProfession]} \\\\n'
            if rd.randint(1, 5) == 1:
                secondRandomProfession = rd.randint(0,
                                                    len(Villager.VILLAGE_PROFESSION_LIST) - 1)
                if secondRandomProfession != randomProfession:
                    textDiaryVillager += f'I would like to work as a {Villager.VILLAGE_PROFESSION_LIST[secondRandomProfession]}.\\\\n'
        elif random == 2 and not targetTextDone:
            randomDiaryTextWithTarget = rd.randint(0, len(newDiaryTextWithTarget) - 1)

            targeted = -1

            if len(village_model.deadVillager) == 1:
                targeted = 0
            elif len(village_model.deadVillager) > 1:
                targeted = village_model.deadVillager[rd.randint(0, len(village_model.deadVillager) - 1)].name

            if targeted != -1:
                textDiaryVillager += (f'{newDiaryTextWithTarget[randomDiaryTextWithTarget]}'
                                      f'{targeted}.  \\\\n')

            newDiaryTextWithTarget.remove(newDiaryTextWithTarget[randomDiaryTextWithTarget])
            targetTextDone = True
        else:
            randomDiaryTextWithoutTarget = rd.randint(0, len(newDiaryTextWithoutTarget) - 1)
            textDiaryVillager += f'{newDiaryTextWithoutTarget[randomDiaryTextWithoutTarget]}   \\\\n'
            newDiaryTextWithoutTarget.remove(newDiaryTextWithoutTarget[randomDiaryTextWithoutTarget])

        if i % 4 == 0:
            textDiaryVillager += ' \f'

    return [textDiaryVillager, gift]


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
