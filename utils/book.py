from generation.data.villager import Villager
from generation.data.village import Village
from generation.data.loreStructure import LoreStructure
from generation.data.villageInteraction import VillageInteraction
from utils.bookWriter import BookWriter

import generation.generator as generator
import utils.projectMath as pmath

import random as rd

VILLAGER_NAME_PATH = "data/names/"

MIN_SIZE = 4
MAX_SIZE = 15


def villageMessage(village_name: str) -> str:
    return "-" + village_name + " settlement-"


"""
Return the text of the book of the village presentation
"""


def createTextOfPresentationVillage(settlementData) -> BookWriter:
    village: Village = settlementData.village_model

    book_writer: BookWriter = BookWriter()
    book_writer.writeFirstPage("Welcome to :",
                               "The " + ("old " if village.age == 1 else "") + "village of " + village.name)

    # Status of the village
    number_structure_destroyed: int = 0
    number_house: int = 0

    for structure in village.lore_structures:
        if structure.destroyed:
            number_structure_destroyed += 1
        elif structure.type == LoreStructure.TYPE_HOUSES:
            number_house += 1

    # Status of the village relationship

    book_writer.fillLineWith('-')

    tier: str = "basic " if village.tier == 0 else "medium " if village.tier == 1 else "advanced "
    book_writer.writeLine(f'Welcome to the {"old " if village.age == 1 else "" + tier} village of {village.name}')

    book_writer.writeLine(f'Status of {village.name} :', breakLine=False)
    book_writer.setTextMode(BookWriter.TEXT_BOLD, True)
    book_writer.writeLine(f'{village.status}')
    book_writer.setTextMode(BookWriter.TEXT_BOLD, False)
    book_writer.writeEmptyLine(1)

    hadBrokeARelation: bool = False
    book_writer.setTextMode(book_writer.TEXT_UNDERLINE, True)
    book_writer.writeLine('Village relationships', False)
    book_writer.setTextMode(book_writer.TEXT_UNDERLINE, False)
    book_writer.writeLine(':')
    book_writer.writeEmptyLine(1)

    for village_key in village.village_interactions:
        interaction: VillageInteraction = village.village_interactions[village_key]

        if interaction.brokeTheirRelation:
            hadBrokeARelation = True

        if interaction.state == interaction.STATE_WAR:
            book_writer.writeLine('In ', breakLine=False)
            book_writer.setColor(BookWriter.COLOR_RED)
            book_writer.writeLine('war', breakLine=False)
            book_writer.setColor(BookWriter.COLOR_BLACK)
            book_writer.writeLine(' with ', breakLine=False)
        elif interaction.state == interaction.STATE_TENSION:
            book_writer.writeLine('Got ', breakLine=False)
            book_writer.setColor(BookWriter.COLOR_GOLD)
            book_writer.writeLine('tension', breakLine=False)
            book_writer.setColor(BookWriter.COLOR_BLACK)
            book_writer.writeLine(' with ', breakLine=False)
        elif interaction.state == interaction.STATE_FRIENDSHIP:
            book_writer.setColor(BookWriter.COLOR_BLUE)
            book_writer.writeLine('Friendship relation', breakLine=False)
            book_writer.setColor(BookWriter.COLOR_BLACK)
            book_writer.writeLine(' with ', breakLine=False)
        elif interaction.state == interaction.STATE_LOVE:
            book_writer.setColor(BookWriter.COLOR_GREEN)
            book_writer.writeLine('Very close relation', breakLine=False)
            book_writer.setColor(BookWriter.COLOR_BLACK)
            book_writer.writeLine(' with ', breakLine=False)

        if interaction.state != interaction.STATE_NEUTRAL:
            book_writer.writeLine(f'{village_key.name}.')

        book_writer.writeEmptyLine(1)

    if hadBrokeARelation:
        book_writer.writeLine(f'Due to the war, {village.name} had broke their relation with ', breakLine=False)
        for village_key in village.village_interactions:
            interaction: VillageInteraction = village.village_interactions[village_key]

            if interaction.brokeTheirRelation:
                book_writer.writeLine(village_key.name + ' ', breakLine=False)

    book_writer.fillLineWith('-')
    book_writer.breakPage()
    book_writer.fillLineWith('-')
    book_writer.setTextMode(book_writer.TEXT_UNDERLINE, True)
    book_writer.writeLine('Village statistics', False)
    book_writer.setTextMode(book_writer.TEXT_UNDERLINE, False)
    book_writer.writeLine(':')
    book_writer.writeLine(f'Dirt resources: {round(settlementData.resources["dirtResources"], 2)}')
    book_writer.writeLine(f'Wood resources: {round(settlementData.resources["woodResources"], 2)}')
    book_writer.writeLine(f'Stone resources: {round(settlementData.resources["stoneResources"], 2)}')
    book_writer.fillLineWith('-')
    book_writer.breakPage()

    # Stats on the village
    book_writer.fillLineWith('-')

    book_writer.writeLine(f'There are {len(village.lore_structures)} structures.')
    book_writer.writeLine('The population of the village is composed of ', breakLine=False)

    book_writer.setColor(BookWriter.COLOR_GREEN)
    book_writer.writeLine(f'{len(village.villagers)}', breakLine=False)
    book_writer.setColor(BookWriter.COLOR_BLACK)
    book_writer.writeLine(' villagers.')

    book_writer.writeLine(f'They are living on {number_house} houses.')

    book_writer.setColor(BookWriter.COLOR_RED)
    book_writer.writeLine(f'{len(village.dead_villagers)}', breakLine=False)
    book_writer.setColor(BookWriter.COLOR_BLACK)
    book_writer.writeLine(f' villagers have died since their arrival.')
    book_writer.writeLine(f'{number_structure_destroyed} structures are destroyed.')
    book_writer.fillLineWith('-')
    book_writer.breakPage()

    book_writer.writeLine('List of structures :')
    for structure in village.lore_structures:
        book_writer.writeLine('-', breakLine=False)
        if structure.age == 1:
            book_writer.writeLine(' Old', breakLine=False)

        if structure.destroyed == 1:
            book_writer.writeLine(' Destroyed', breakLine=False)

        book_writer.writeLine(f' {structure.group}.')

    return book_writer


"""
Return the text of the book of the villagers names and professions
"""


def createTextForVillagersNames(village_name: str, villagers: list):
    book_writer: BookWriter = BookWriter()
    book_writer.writeFirstPage(villageMessage(village_name), "Registry of living villagers.")

    villager_text: str
    for villager in villagers:
        villager_text = villager.name + " : " + villager.job

        book_writer.writeLine(f'-{villager_text}.')

    return book_writer


DIARY_TEXTS_WITHOUT_TARGETS = [" I really like the color of the village. ", " I really like the name of the village. ",
                               " I hate the color of the village.",
                               " I am afraid of spiders. ", " I am afraid of creepers. ", " I am afraid of zombies. ",
                               " I am afraid of skeletons. ",
                               " I don\\\'t like the facade of my house. ",
                               " I don\\\'t like the flower of the village. ",
                               " I really like the flower of the village. ", " I really like the mayor. ",
                               " I hate the flower of the village. ", " I hate the mayor. ",
                               " I would like to have a better house. ",
                               " I really like pigs. ", " I really like cows. ", " I am interested about sheep.  ",
                               " I am interested about chickens. "]

DIARY_TEXTS_WITH_TARGETS = [" I am sad since the death of ", " I am happy since the death of ", " I used to hate ",
                            " I once hit "]

"""
Return the text of the book of the dead villagers names and professions
"""
def createTextForDeadVillagers(village_name: str, villagers: list, deadVillagers: list):
    names = []
    for villager in villagers:
        names.append(villager.name)

    book_writer: BookWriter = BookWriter()
    book_writer.writeFirstPage(villageMessage(village_name), "Registry of dead villagers.")

    for deadVillager in deadVillagers:
        book_writer.writeLine(
            f'-{deadVillager.name} {"Senior" if deadVillager.name in names else ""} : {deadVillager.reason_death}.')

    return book_writer


def createBookForVillager(village_model: Village, villager: Villager) -> list:
    villager_name: str = villager.name

    # 1 / 2 chance to a gift
    available_indices: list = generator.returnVillagerAvailableForGift(village_model, [villager])
    random_gift = rd.randint(1, 4)
    gift: str = ""
    if random_gift == 1 and len(available_indices) >= 1:
        gift = "minecraft:gold_block"
    elif random_gift == 2 and len(available_indices) >= 1:
        gift = "minecraft:tnt"

    gift_place = -1 if gift == "" else rd.randint(1, 3)

    new_diary_text_without_target = DIARY_TEXTS_WITHOUT_TARGETS.copy()
    new_diary_text_with_target = DIARY_TEXTS_WITH_TARGETS.copy()

    target_text_done = False
    murderer_suspicious = False
    murdererData = village_model.murderer_data

    number_phrase = rd.randint(4, 7) + len(villager.orders)
    order_places = pmath.generatePlacesAmong(list(i for i in range(number_phrase) if i != gift_place), len(villager.orders))
    order_counter = 0

    book_writer: BookWriter = BookWriter()
    book_writer.writeFirstPage(villager_name + " diary", "")
    book_writer.writeLine(f'My job is to be a {villager.job}')

    sentence: str = ""
    for structure in village_model.lore_structures:
        if structure.type != LoreStructure.TYPE_HOUSES or villager not in structure.villagers:
            continue

        if len(structure.villagers) == 1:
            sentence = "nobody"
        else:
            for i in range(len(structure.villagers)):
                if structure.villagers[i] == villager:
                    continue

                sentence += structure.villagers[i].name

                if i != len(structure.villagers) - 1 or i != len(structure.villagers) - 2 and villager != structure.villagers[-1]:
                    sentence += ", "

    book_writer.writeLine(f'I\\\'m living with {sentence}')

    for i in range(number_phrase):
        # Other phrase
        random = rd.randint(1, 5)

        # Spaces
        book_writer.writeEmptyLine(rd.randint(0, 1))

        if villager == village_model.murderer_data.fakeVillagerMurderer and not murderer_suspicious:
            murderer_suspicious = True
            book_writer.writeLine(f'I don\\\'t understand why people have been looking at me strangely lately. ')

        elif i in order_places:
            order = villager.orders[order_counter]

            book_writer.writeLine(f'I made an order to the {order.structure.group}')
            order_counter += 1
        # Gift phrase
        elif i == gift_place:
            targeted_villager: Villager = available_indices[rd.randint(0, len(available_indices) - 1)]

            if random_gift == 1:
                if rd.randint(1, 2) == 1:
                    book_writer.writeLine(f'I love {targeted_villager.name}', breakLine=False)
                else:
                    book_writer.writeLine(f'{targeted_villager.name} is my best friend', breakLine=False)

                if rd.randint(1, 2) == 1:
                    book_writer.writeLine(', I left a surprise under the door.')
                else:
                    book_writer.writeLine(', I hope my lover will finds the gift I left him under the door.')

            elif random_gift == 2:
                if rd.randint(1, 2) == 1:
                    book_writer.writeLine(f'I hate {targeted_villager.name}', breakLine=False)
                else:
                    book_writer.writeLine(f'{targeted_villager.name} is a jerk', breakLine=False)

                if rd.randint(1, 2) == 1:
                    book_writer.writeLine(', I placed a tnt under the door.')
                else:
                    book_writer.writeLine(', I put a deadly trap under the door.')

        # Murderer suspicion
        elif rd.randint(1, 3) == 1 and not murderer_suspicious and murdererData.villagerMurderer is not None:
            suspected = murdererData.fakeVillagerMurderer if (murdererData.fakeVillagerMurderer is not None and rd.randint(1, 2) == 1) else murdererData.villagerMurderer

            if rd.randint(1, 2) == 1:
                book_writer.writeLine(f'I think that {suspected.name} is really strange.')
            else:
                book_writer.writeLine(f'I think that {suspected.name} has a strange behaviour.')

            murderer_suspicious = True

        elif random == 1:
            randomProfession = rd.randint(0, len(Villager.VILLAGE_PROFESSION_LIST) - 1)
            book_writer.writeLine(f'I hate all {Villager.VILLAGE_PROFESSION_LIST[randomProfession]}.')

            if rd.randint(1, 5) == 1:
                secondRandomProfession = rd.randint(0,
                                                    len(Villager.VILLAGE_PROFESSION_LIST) - 1)
                if secondRandomProfession != randomProfession:
                    book_writer.writeLine(
                        f'I would like to work as a {Villager.VILLAGE_PROFESSION_LIST[secondRandomProfession]}.')

        elif random == 2 and not target_text_done:
            randomDiaryTextWithTarget = rd.randint(0, len(new_diary_text_with_target) - 1)

            targeted = -1

            if len(village_model.dead_villagers) == 1:
                targeted = 0
            elif len(village_model.dead_villagers) > 1:
                targeted = village_model.dead_villagers[rd.randint(0, len(village_model.dead_villagers) - 1)].name

            if targeted != -1:
                book_writer.writeLine(f'{new_diary_text_with_target[randomDiaryTextWithTarget]}{targeted}.')

            new_diary_text_with_target.remove(new_diary_text_with_target[randomDiaryTextWithTarget])
            target_text_done = True
        else:
            randomDiaryTextWithoutTarget = rd.randint(0, len(new_diary_text_without_target) - 1)
            book_writer.writeLine(f'{new_diary_text_without_target[randomDiaryTextWithoutTarget]}')
            new_diary_text_without_target.remove(new_diary_text_without_target[randomDiaryTextWithoutTarget])

    return [book_writer, gift]


def createBookForAdventurerHouse(village_name: str, flip: int):
    flint_place = "right" if 0 < flip < 3 else "left"
    bucket_place = "left " if 0 < flip < 3 else "right"

    book_writer: BookWriter = BookWriter()
    book_writer.writeFirstPage(villageMessage(village_name), "Machine guide.")
    book_writer.fillLineWith('-')
    book_writer.writeLine('Instructions:')
    book_writer.writeLine(f'1. Place flint and steal in the {flint_place} machine.')
    book_writer.writeLine(f'2. Place water bucket in the {bucket_place} machine.')
    book_writer.fillLineWith('-')

    return book_writer
