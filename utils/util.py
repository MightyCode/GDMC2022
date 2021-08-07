import lib.interfaceUtils as interfaceUtils
import lib.worldLoader as worldLoader
import lib.lookup as lookup
import math
import requests
from io import BytesIO
import nbt
import random as rd


NUMBER = 5

def getBiome(x, z, dx, dz):
    """**Returns the chunk data.**"""
    x = math.floor(x / 16)
    z = math.floor(z / 16)
    url = f'http://localhost:9000/chunks?x={x}&z={z}&dx={dx}&dz={dz}'
    try:
        response = requests.get(url)
    except ConnectionError:
        return -1
        #return "minecraft:plains"
    biomeId = response.text.split(":")
    biomeinfo = biomeId[6].split(";")
    biome = biomeinfo[1].split(",")
    return biome[0]
    
def getAllBiome():
    bytes = worldLoader.getChunks(-4, -4, 9, 9, 'bytes')
    file_like = BytesIO(bytes)
    nbtfile = nbt.nbt.NBTFile(buffer=file_like)
    dicochunk = {}
    for y in range(81):
        for x in range(1024):
            if f"{nbtfile['Chunks'][y]['Level']['Biomes'].value[x]}" in dicochunk:
                dicochunk[f"{nbtfile['Chunks'][y]['Level']['Biomes'].value[x]}"] = int(dicochunk[f"{nbtfile['Chunks'][y]['Level']['Biomes'].value[x]}"]) + 1 
            else:
                dicochunk[f"{nbtfile['Chunks'][y]['Level']['Biomes'].value[x]}"] = "1"
    max = 0
    savedbiome = 0
    for x,y in dicochunk.items():
        if y > max:
            savedbiome = x
            max = y
    value = getNameBiome(savedbiome)
    return value
        
        
def getNameBiome(biome):
    filin = open("data/biome.txt")
    lignes = filin.readlines()
    biomename = lignes[int(biome)].split(":")[0]
    print(biomename)
    value = int(lignes[int(biome)].split(":")[1])
    return value


def parseVillagerNameInLines(names, lines, startIndex=0):
    currentLine = startIndex
    for person in names:
        partss = ("-" + person + "\n").split(" ")
        parts = []
        for i in range(len(partss)):
            if len(partss[i]) > 15:
                parts.append(partss[i][0:14])
                parts.append(partss[i][15:])
            else:
                parts.append(partss[i])
        i = 0
        while i < len(parts) and currentLine < len(lines):
            jumpLine = False
            if len(lines[currentLine]) > 0 :
                if len(parts[i]) + 1  <= 15 - len(lines[currentLine]):
                    if "\n" in parts[i]:
                        jumpLine = True
                    lines[currentLine] += " " + parts[i].replace("\n", "")
                    i += 1
                else :
                    jumpLine = True
            else :
                if len(parts[i])  <= 15 - len(lines[currentLine]):
                    if "\n" in parts[i]:
                        jumpLine = True
                    lines[currentLine] += parts[i].replace("\n", "")
                    i += 1
                else :
                    jumpLine = True
            
            if jumpLine :
                currentLine += 1


def addResourcesFromChunk(resources, settlementData, biome):
    if biome == "-1":
        return
        
    dictResources = resources.biomesBlocks[biome]
    if "woodResources" in dictResources:
        settlementData["woodResources"] += dictResources["woodResources"]
    if "dirtResources" in dictResources:
        settlementData["dirtResources"] += dictResources["dirtResources"]
    if "stoneResources" in dictResources:
        settlementData["stoneResources"] += dictResources["stoneResources"]


"""
Return result and word
result 0 -> No balise founded
result 1 -> Balise founded and replacement succeful
result -1 -> Error
"""
def changeNameWithBalise(name, changementsWord):
    index = name.find("*")
    if index != -1 :
        secondIndex = name.find("*", index+1)
        if secondIndex == -1:
            return [-1, name]

        word = name[index +1 : secondIndex]
        added = False
        for key in changementsWord.keys():
            if key == word:
                added = True
                return [1, name.replace("*" + word + "*", changementsWord[key])]
                        
        # If the balise can't be replace
        if not added:
            return [-1, name]
    
    else:
        return  [0, name]


def addBookToLectern(x, y, z, bookData):
    command = (f'data merge block {x} {y} {z} '
                    f'{{Book: {{id: "minecraft:written_book", '
                    f'Count: 1b, tag: {bookData}'
                    '}, Page: 0}')

    response = interfaceUtils.runCommand(command)
    if not response.isnumeric():
        print(f"{lookup.TCOLORS['orange']}Warning: Server returned error "
            f"upon placing book in lectern:\n\t{lookup.TCOLORS['CLR']}"
            f"{response}")

"""
Spawn a villager at his house if unemployed or at his building of work
"""
def spawnVillagerForStructure(settlementData, structureData, position):
    for id in structureData["villagersId"]:
        if (structureData["type"] == "houses" and settlementData["villagerProfession"][id] == "Unemployed") or (structureData["type"] != "houses" and settlementData["villagerProfession"][id] != "Unemployed") : 
            # get a random level for the profession of the villager (2: Apprentice, 3: Journeyman, 4: Expert, 5: Master)
            randomProfessionLevel = rd.randint(2, 5)

            spawnVillager(position[0], position[1] + 1, position[2], "minecraft:villager", 
                settlementData["villagerNames"][id], settlementData["villagerGameProfession"][id], randomProfessionLevel, settlementData["biomeName"])


def spawnVillager(x, y, z, entity, name, profession, level, type):
    command = "summon " + entity + " " + str(x) + " " + str(y) + " " + str(z) + " "
    command += "{VillagerData:{profession:" + profession + ",level:" + str(level) + ",type:" + type + "},CustomName:""\"\\" + '"' + str(name) + "\\" +'""' + "}"

    interfaceUtils.runCommand(command)
    

# Add items to a chest
# Items is a list of [item string, item quantity]
def addItemChest(x, y, z, items):
    for id,v in enumerate(items):
        command = "replaceitem block {} {} {} {} {} {}".format(x, y, z,
                                                               "container."+str(id),
                                                               v[0],
                                                               v[1])
        interfaceUtils.runCommand(command)


def getHighestNonAirBlock(cx, cy, cz):
    cy = 255
    IGNORED_BLOCKS = [
        'minecraft:air', 'minecraft:cave_air', 'minecraft:water', 'minecraft:lava',
        'minecraft:oak_leaves',  'minecraft:leaves',  'minecraft:birch_leaves', 'minecraft:spruce_leaves', 'minecraft:dark_oak_leaves'
        'minecraft:oak_log',  'minecraft:spruce_log',  'minecraft:birch_log',  'minecraft:jungle_log', 'minecraft:acacia_log', 'minecraft:dark_oak_log',
        'minecraft:grass', 'minecraft:snow', 'minecraft:poppy', 'minecraft:pissenlit', 'minecraft:seagrass' , 'minecraft:dandelion' ,'minecraft:blue_orchid',
        'minecraft:allium', 'minecraft:azure_bluet', 'minecraft:red_tulip', 'minecraft:orange_tulip', 'minecraft:white_tulip', 'minecraft:pink_tulip',
        'minecraft:oxeye_daisy', 'minecraft:cornflower', 'minecraft:lily_of_the_valley', 'minecraft:brown_mushroom', 'minecraft:red_mushroom',
        'minecraft:sunflower', 'minecraft:peony', 'minecraft:dead_bush', "minecraft:cactus", "minecraft:sugar_cane", 'minecraft:fern']
    ## Find highest non-air block
    while interfaceUtils.getBlock(cx, cy, cz) in IGNORED_BLOCKS:
        cy -= 1
    return cy

# Create a book item from a text
def makeBookItem(text, title = "", author = "", desc = ""):
    booktext = "pages:["
    while len(text) > 0:
        page = text[:15*23]
        text = text[15*23:]
        bookpage = "'{\"text\":\""
        while len(page) > 0:
            line = page[:23]
            page = page[23:]
            bookpage += line + "\\\\n"
        bookpage += "\"}',"
        booktext += bookpage

    booktext = booktext + "],"

    booktitle = "title:\""+title+"\","
    bookauthor = "author:\""+author+"\","
    bookdesc = "display:{Lore:[\""+desc+"\"]}"
    return "written_book{"+booktext+booktitle+bookauthor+bookdesc+"}"

def strToDictBlock(block):
    expended = {}
    parts = block.split["["]
    expended["Name"] = parts[0]
    expended["Properties"] = {}

    if len(parts) > 1:
        subParts = parts[1].split(",")
        for i in subParts:
            subsubParts = i.split("=")
            expended["Properties"][subsubParts[0]] = subsubParts[1]

    return expended

def compareTwoDictBlock(a, b):
    if a["Name"] != b["Name"]:
        return False
    if len(a.keys()) != len(b.keys()):
        return False

    for key in a.keys() :
        if not b.keys().contains(key):
            return False
        
        if a[key] != b[key]:
            return False

    return True
