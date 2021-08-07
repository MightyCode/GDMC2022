import generation.generator as generator

import random as rd
import pandas as pd
import numpy as np

REASON_OF_DEATHS = ["murdered", "died because of old age", "died of creeper attack", "died of skeleton attack", "died of spider attack (he did not became Spider-Man)",
                    "died of zombie attack", "died of witch attack", "died suffocating from sand falling" , "died eating too much cake", "died crushing by a rock" 
                    , "died suffocating from gravel falling"]
DIARY_TEXTS_WITHOUT_TARGETS = [" I really like the color of the village. ", " I really like the name of the village. ", " I hate the color of the village.", 
               " I am afraid of spiders. ", " I am afraid of creppers. ", " I am afraid of zombies. ", " I am afraid of skeletons. ",
               " I don't like the facade of my house. ", " I don't like the flower of the village. ",
               " I really like the flower of the village. ", " I really like the mayor. ", " I hate the flower of the village. ", " I hate the mayor. ",
               " I would like to have a better house. ", " I hope he finds the gift I left him under his door. ",
               " I really like pigs. ", " I really like cows. ", " I am interested about sheeps.  ", " I am interested about chickens. "]
DIARY_TEXTS_WITH_TARGETS = [" I am sad since the death of ", " I am happy since the death of ", " I used to hate ", " I once hit "] 

VILLAGER_NAME_PATH = "data/names/"

MIN_SIZE = 4
MAX_SIZE = 15

"""
Return the text of the book of the village presentation
"""
def createTextOfPresentationVillage(villageName, structuresNumber, structuresNames, deadVillagersNumber, listOfVillagers):
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
    textVillagePresentationBook += ('\f\\\\s---------------\\\\n')
    
    numberOfHouse = 0
    for i in range(len(structuresNames)):
        if "house" in structuresNames[i]["name"]:
            numberOfHouse += 1
    textVillagePresentationBook += (f'{len(listOfVillagers)} villagers arrived in '
                                    f'{numberOfHouse} houses \\\\n')
    textVillagePresentationBook += (f'{deadVillagersNumber} villagers have died since their arrival. \\\\n')
    textVillagePresentationBook += (''
                      'There are '
                      f'{structuresNumber} structures. \\\\n')
    textVillagePresentationBook += ('---------------\\\\n\f')

    for i in range(len(structuresNames)):
        if i <= 2:
            if "lumberjachut" in structuresNames[i]["name"]:
                textVillagePresentationBook += ('Villagers built a '
                                                f'{structuresNames[i]["name"]} \\\\n')
            elif "quarry" in structuresNames[i]["name"] or "well" in structuresNames[i]["name"] or "basichouse" in structuresNames[i]["name"]:
                textVillagePresentationBook += ('Using the lumberjack hut, villagers built a '
                                                f'{structuresNames[i]["name"]} \\\\n')
            elif "smeltery" in structuresNames[i]["name"] or "furnace" in structuresNames[i]["name"] or "stonecutter" in structuresNames[i]["name"]:
                textVillagePresentationBook += ('Using the quarry, villagers built a '
                                                f'{structuresNames[i]["name"]} \\\\n')
            elif "workshop" in structuresNames[i]["name"] or "jail" in structuresNames[i]["name"] or "townhall" in structuresNames[i]["name"] or "farm" in structuresNames[i]["name"] or "mediumhouse" in structuresNames[i]["name"]:
                textVillagePresentationBook += ('Using the stone cutter, villagers built a '
                                                f'{structuresNames[i]["name"]} \\\\n')
            elif "graveyard" in structuresNames[i]["name"]:
                textVillagePresentationBook += ('Using the furnace, villagers built a '
                                                f'{structuresNames[i]["name"]} \\\\n')
            elif "basicwindmill" in structuresNames[i]["name"] or "barrack" in structuresNames[i]["name"] or "weaverhouse" in structuresNames[i]["name"] or "observatory" in structuresNames[i]["name"]:
                textVillagePresentationBook += ('Using the workshop, villagers built a '
                                                f'{structuresNames[i]["name"]} \\\\n')
            elif "mediumwindmill" in structuresNames[i]["name"]:
                textVillagePresentationBook += ('Using the windmill and the weaver house, villagers built a '
                                                f'{structuresNames[i]["name"]} \\\\n')
            elif "tavern" in structuresNames[i]["name"]:
                textVillagePresentationBook += ('Using the windmill, the farm and the furnace, villagers built a '
                                                f'{structuresNames[i]["name"]} \\\\n')
            elif "adventurerhouse" in structuresNames[i]["name"]:
                textVillagePresentationBook += ('Using the tavern, villagers built an '
                                                f'{structuresNames[i]["name"]} \\\\n')
        if i % 3 == 0 and i != 0:
            textVillagePresentationBook += ('\f')
        if i >= 3:
            if "lumberjachut" in structuresNames[i]["name"]:
                textVillagePresentationBook += ('Villagers built a '
                                                f'{structuresNames[i]["name"]} \\\\n')
            elif "quarry" in structuresNames[i]["name"] or "well" in structuresNames[i]["name"] or "basichouse" in structuresNames[i]["name"]:
                textVillagePresentationBook += ('Using the lumberjack hut, villagers built a '
                                                f'{structuresNames[i]["name"]} \\\\n')
            elif "smeltery" in structuresNames[i]["name"] or "furnace" in structuresNames[i]["name"] or "stonecutter" in structuresNames[i]["name"]:
                textVillagePresentationBook += ('Using the quarry, villagers built a '
                                                f'{structuresNames[i]["name"]} \\\\n')
            elif "workshop" in structuresNames[i]["name"] or "jail" in structuresNames[i]["name"] or "townhall" in structuresNames[i]["name"] or "farm" in structuresNames[i]["name"] or "mediumhouse" in structuresNames[i]["name"]:
                textVillagePresentationBook += ('Using the stone cutter, villagers built a '
                                                f'{structuresNames[i]["name"]} \\\\n')
            elif "graveyard" in structuresNames[i]["name"]:
                textVillagePresentationBook += ('Using the furnace, villagers built a '
                                                f'{structuresNames[i]["name"]} \\\\n')
            elif "basicwindmill" in structuresNames[i]["name"] or "barrack" in structuresNames[i]["name"] or "weaverhouse" in structuresNames[i]["name"] or "observatory" in structuresNames[i]["name"]:
                textVillagePresentationBook += ('Using the workshop, villagers built a '
                                                f'{structuresNames[i]["name"]} \\\\n')
            elif "mediumwindmill" in structuresNames[i]["name"]:
                textVillagePresentationBook += ('Using the windmill and the weaver house, villagers built a '
                                                f'{structuresNames[i]["name"]} \\\\n')
            elif "tavern" in structuresNames[i]["name"]:
                textVillagePresentationBook += ('Using the windmill, the farm and the furnace, villagers built a '
                                                f'{structuresNames[i]["name"]} \\\\n')
            elif "adventurerhouse" in structuresNames[i]["name"]:
                textVillagePresentationBook += ('Using the tavern, villagers built an '
                                                f'{structuresNames[i]["name"]} \\\\n')
    return textVillagePresentationBook

"""
Return the text of the book of the villagers names and professions
"""
def createTextForVillagersNames(listOfVillagers):
    textVillagerNames = ('Registry of living villagers \\\\n')
    for i in range(len(listOfVillagers)):
        if i <= 3: 
            textVillagerNames += ('-'
                f'{listOfVillagers[i]}       \\\\n')
        if i % 4 == 0 and i != 0:
            textVillagerNames += ('\f')
        if i >= 4:
            textVillagerNames += ('-'
                f'{listOfVillagers[i]}       \\\\n')
    textVillagerNames += ('\f')
    return textVillagerNames


"""
Return the text of the book of the dead villagers names and professions
"""
def createTextForDeadVillagers(listOfVillagers):
    randomOfDeadVillagers = rd.randint(1, len(listOfVillagers) - 1)
    villagerFirstNamesList = getFirstNamelist()
    villagerLastNamesList = getLastNamelist()
    
    data = {}
    data["listOfDeadVillagers"] = []
    for i in range(randomOfDeadVillagers):
        data["listOfDeadVillagers"].append(getRandomVillagerNames(villagerFirstNamesList, 1)[0] + " " + getRandomVillagerNames(villagerLastNamesList, 1)[0])
    listOfVillagersWithoutJob = [i.split(':', 1)[0] for i in listOfVillagers]
    textDeadVillagers = ('Registry of dead villagers \\\\n')

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
            textDeadVillagers += ('\f')
        if i >= 3:
            textDeadVillagers += ('-'
                f'{deadVillager} : '
                f'{REASON_OF_DEATHS[randomDeath]} \\\\n')
    textDeadVillagers += ('\f')
    return [textDeadVillagers, randomOfDeadVillagers, data["listOfDeadVillagers"]]


def createBookForVillager(settlementData, villagerIndex):
    villagerName = settlementData["villagerNames"][villagerIndex]
    gift = ""

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
    textDiaryVillager += ('     \f')
    
    newDiaryTextWithoutTarget = DIARY_TEXTS_WITHOUT_TARGETS.copy()
    newDiaryTextWithTarget = DIARY_TEXTS_WITH_TARGETS.copy()
    targetTextDone = False
    murdererSuspicious = False

    numberPhrase = rd.randint(3, 7)
    for i in range(numberPhrase):
        # Spaces
        if rd.randint(1, 2) == 1:
            textDiaryVillager += ('                      \\\\n')
            if rd.randint(1, 2) == 1:
                textDiaryVillager += ('                      \\\\n')

        # Gift phrase
        if i == giftPlace:
            availableIndices = generator.returnVillagerAvailableForGift(settlementData, [villagerIndex])
            targetedVillager = availableIndices[rd.randint(0, len(availableIndices) - 1)]
            if randomGift == 1:
                if rd.randint(1, 2) == 1:
                    textDiaryVillager += (f'I love {settlementData["villagerNames"][targetedVillager]}\\\\n')
                else : 
                    textDiaryVillager += (f'{settlementData["villagerNames"][targetedVillager]} is my best friend\\\\n')

                if rd.randint(1, 2) == 1:
                    textDiaryVillager += (', I left a surprise under the door.\\\\n')
                else : 
                    textDiaryVillager += (', I hope my lover will finds the gift I left him under the door.\\\\n')
                    
            elif randomGift == 2:
                if rd.randint(1, 2) == 1:
                    textDiaryVillager += (f'I hate {settlementData["villagerNames"][targetedVillager]}\\\\n')
                else : 
                    textDiaryVillager += (f'{settlementData["villagerNames"][targetedVillager]} is a jerk\\\\n')

                if rd.randint(1, 2) == 1:
                    textDiaryVillager += (', I placed a tnt under the door.\\\\n')
                else : 
                    textDiaryVillager += (', I put a deadly trap under the door.\\\\n')
            continue
        
        # Murderer suspicion
        if rd.randint(1, 5) == 1 and not murdererSuspicious and settlementData["murdererIndex"] != -1 :
            textDiaryVillager += (f'I think that {settlementData["villagerNames"][settlementData["murdererIndex"]]} is really strange. \\\\n')
            murdererSuspicious = True
            continue

        # Other phrase    
        random = rd.randint(1, 5)
        if random == 1:
            randomProfession = rd.randint(0, len(settlementData["villagerProfessionList"]) - 1)
            textDiaryVillager += (f'I hate all {settlementData["villagerProfessionList"][randomProfession]} \\\\n')
            if rd.randint(1, 5) == 1:
                secondRandomProfession = rd.randint(0, len(settlementData["villagerProfessionList"]) - 1)
                if secondRandomProfession != randomProfession:
                    textDiaryVillager += (f'I would like to work as a {settlementData["villagerProfessionList"][secondRandomProfession]}.\\\\n')
        elif random == 2 and not targetTextDone: 
            randomDiaryTextWithTarget = rd.randint(0, len(newDiaryTextWithTarget) - 1)
            targeted = settlementData["villagerDeadNames"][rd.randint(0, len(settlementData["villagerDeadNames"]) - 1)]
            textDiaryVillager += (f'{newDiaryTextWithTarget[randomDiaryTextWithTarget]}'
                                          f'{targeted}.  \\\\n')
            newDiaryTextWithTarget.remove(newDiaryTextWithTarget[randomDiaryTextWithTarget])
            targetTextDone = True
        else: 
            randomDiaryTextWithoutTarget = rd.randint(0, len(newDiaryTextWithoutTarget) - 1)
            textDiaryVillager += (f'{newDiaryTextWithoutTarget[randomDiaryTextWithoutTarget]}   \\\\n')
            newDiaryTextWithoutTarget.remove(newDiaryTextWithoutTarget[randomDiaryTextWithoutTarget])

        if i % 4 == 0:
            textDiaryVillager += (' \f')
            
    return [textDiaryVillager, gift]


def createBookForAdventurerHouse(flip):
    flintPlace = "right" if flip > 0 else "left"
    bucketPlace = "left " if flip > 0 else "right"

    textAdventurerbook = (
            '\\\\s-------------------\\\\n'
            'Machine guide:  \\\\n'
            f'Place flint and steal {flintPlace} in the machine. Place water bucket in the {bucketPlace} machine. \\\\n'
            '                      \\\\n'
            '                      \\\\n'
            '                      \\\\n'
            '                      \\\\n'
            '                      \\\\n'
            '                      \\\\n'
            '                      \\\\n'
            '-------------------')
    textAdventurerbook += ('\f')

    return textAdventurerbook



# -------------------------------------------------------- generate random villagers names

def getFirstNamelist():
    with open(VILLAGER_NAME_PATH + "villagerFirstNames.txt", "r") as f:
        # return the split results, which is all the words in the file.
        return f.read().replace("\n", "").split(";")

def getLastNamelist():
    with open(VILLAGER_NAME_PATH + "villagerLastNames.txt", "r") as f:
        # return the split results, which is all the words in the file.
        return f.read().replace("\n", "").split(";")

def getRandomVillagerNames(villagerNamesList, number):
    listOfRandomVillagers = []
    listOfVillagers = villagerNamesList.copy()
    for i in range(number):
        # get a random name from the list of names
        randomName = rd.choice(listOfVillagers)
        # add the random name to the list of random villagers
        listOfRandomVillagers.append(randomName)
        # delete the random name from the list of all villagers so we don't get the same name twice
        del listOfVillagers[listOfVillagers.index(randomName)]
    return listOfRandomVillagers


# -------------------------------------------------------- generate random village name
def initialize():
    with open (VILLAGER_NAME_PATH + "Lexique-query.tsv") as f:
        #Extract data
        dicto = pd.read_csv (f, sep = "\t")

        # Creation of the vector which contains all the words (delete missed values and duplicates)
        words = dicto.Word.dropna().unique()

        # Add the char ' ' at the end of words to mark the end
        for i in range(words.shape[0]):
            words[i] = words[i] + ' '


        # Cleaning of the data by replacing specials or rare chars by common chars
        clean_words = []
        for word in words:
            clean_word = word
            for letter in word:
                if letter == 'ã' or letter == 'â' or letter == 'à':
                    clean_word = clean_word.replace(letter, 'a')
                if letter == 'ï' or letter == 'î' or letter == 'ï':
                    clean_word = clean_word.replace(letter, 'i')
                if letter == 'û' or letter == 'ù' or letter == 'ü':
                    clean_word = clean_word.replace(letter, 'u')
                if letter == '-' or letter == '.':
                    clean_word = clean_word.replace(letter, '')
                if letter == 'ö' or letter == 'ô':
                    clean_word = clean_word.replace(letter, 'o')
                if letter == 'ñ':
                    clean_word = clean_word.replace(letter, 'n')
            clean_words.append(clean_word)
        #print(clean_words)



        # Creation of a list grouping all the used chars
        carac = set()
        for word in clean_words:
            for letter in word:
                carac.add(letter)
        carac = list(carac)
        last_ind = carac.index(' ')
        last_ind = np.array(last_ind, dtype=object)
        #print(carac)
        #print(last_ind)



        # Creation of a tensor of dimension 2, the rows and the columns represent the letters in the order of carac
        # At the intersection [i][j] is the number of times the letter in j is found after the letter in i
        arr1 = np.zeros([len(carac), len(carac)], dtype=object)
        for word in clean_words:
            for i in range(len(word) - 1):
                letter_index = carac.index(word[i])
                next_index = carac.index(word[i + 1])
                arr1[letter_index][next_index] += 1
        


        # Creation of a tensor of dimension 3, the rows and the columns represent the letters in the order of carac
        # At the intersection [i][j][k] is the number of times the letter in k is found after the letter in i and j
        arr2 = np.zeros([len(carac), len(carac), len(carac)], dtype=object)
        for word in clean_words:
            if len(word) > 2:
                for i in range(len(word) - 2):
                    letter_index = carac.index(word[i])
                    index_plus1 = carac.index(word[i + 1])
                    index_plus2 = carac.index(word[i + 2])
                    arr2[letter_index][index_plus1][index_plus2] += 1
        

        # Modification of arr1 by dividing each entry by the sum of the line
        # to have a vlaue of sum of 1
        i = 0
        arr_last1 = []
        for row in arr1:
            arr_temp = []
            summ = sum(row)
            if summ != 0:
                for item in row:
                    arr_temp.append(item/summ)
                arr_last1.append(arr_temp)
            else:
                arr_last1.append(row)
        arr_last1 = np.array(arr_last1, dtype=object)


        # Modification of arr2 by dividing each entry by the sum of the line
        # to have a vlaue of sum of 1
        i = 0
        arr_last2 = []
        for col in arr2:
            arr_temp2 = []
            for row in col:
                arr_temp1 = []
                summ = sum(row)
                if summ != 0:
                    for item in row:
                        arr_temp1.append(item/summ)
                    arr_temp2.append(arr_temp1)
                else:
                    arr_temp2.append(row)
            arr_last2.append(arr_temp2)
        arr_last2 = np.array(arr_last2, dtype=object)
        #print(arr_last2[0][2])
        #print(arr2[0][2])

        # Creation of two lists which regroup the cumulated probs of letters and their index in carac for vision 1
        arr_cum1 = []
        arr_ind1 = []
        for i, row in enumerate(arr_last1):
            arr_ind_temp = []
            arr_cum_temp = []
            summ = 0
            for j, item in enumerate(row):
                if item > 0:
                    summ += item
                    arr_ind_temp.append(j)
                    arr_cum_temp.append(summ)
            arr_ind1.append(arr_ind_temp)
            arr_cum1.append(arr_cum_temp)
        arr_cum1 = np.array(arr_cum1, dtype=object)
        arr_ind1 = np.array(arr_ind1, dtype=object)
        #print(arr_ind1)
        #print(arr_cum1)

        # Creation of two matrices which regroup the cumuluated probs of letter and their index in carac by vision 2
        arr_cum2 = []
        arr_ind2 = []
        for i, col in enumerate(arr_last2):
            arr_ind_temp2 = []
            arr_cum_temp2 = []
            for j, row in enumerate(col):
                arr_ind_temp1 = []
                arr_cum_temp1 = []
                summ = 0
                for k, item in enumerate(row):
                    if item > 0:
                        summ += item
                        arr_ind_temp1.append(k)
                        arr_cum_temp1.append(summ)
                arr_ind_temp2.append(arr_ind_temp1)
                arr_cum_temp2.append(arr_cum_temp1)
            arr_ind2.append(arr_ind_temp2)
            arr_cum2.append(arr_cum_temp2)
        arr_cum2 = np.array(arr_cum2, dtype=object)
        arr_ind2 = np.array(arr_ind2, dtype=object)
        #print(arr_ind2)
        #print(arr_cum2)

        # Creation of a list of charac by which a word start
        arr_temp = np.zeros([len(carac)])
        for word in clean_words:
            index = carac.index(word[0])
            arr_temp[index] += 1
        arr_deb = arr_temp/sum(arr_temp)

        arr_ind_pre = [] 
        arr_cum_pre = []
        summ = 0
        for i, el in enumerate(arr_deb):
            if el != 0:
                summ += el
                arr_ind_pre.append(i)
                arr_cum_pre.append(summ)
        arr_cum_pre = np.array(arr_cum_pre, dtype=object)
        arr_ind_pre = np.array(arr_ind_pre, dtype=object)
        f.close()   
        return arr_cum_pre, arr_ind_pre, carac, arr_cum1, arr_ind1, arr_cum2, arr_ind2, last_ind


# Generation of random name
def generateVillageName():
    arr_cum_pre, arr_ind_pre, carac, arr_cum1, arr_ind1, arr_cum2, arr_ind2, last_ind = initialize()
    word = []
    # Generation of first letter
    random = rd.random()
    for i, car in enumerate(arr_cum_pre):
        if random <= car:
            seed = arr_ind_pre[i]
            break
    word.append(carac[seed])

    # Generation of second letter
    random = rd.random()
    for i, car in enumerate(arr_cum1[seed]):
        if random <= car:
            seed = arr_ind1[seed][i]
            break

    # Generation of following letters
    cond = True
    while cond:
        word.append(carac[seed])
        previous_letter1 = carac.index(word[-1])
        previous_letter2 = carac.index(word[-2])
        random = rd.random()
        for i, car in enumerate(arr_cum2[previous_letter2][previous_letter1]):
            if random <= car:
                seed = arr_ind2[previous_letter2][previous_letter1][i]
                break
        if seed == last_ind:
            cond = False
    name = ""
    for let in word:
        if let != '':
            name += let
    if len(name) > MIN_SIZE and len(name) < MAX_SIZE:
        return name
    else:
        return generateVillageName()
        # print(let, end ='')
    # print("\n")
    # return name