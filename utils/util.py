from generation.data.villager import Villager

import lib.interfaceUtils as interfaceUtils
import lib.worldLoader as worldLoader
import lib.lookup as lookup

import math
import requests
from io import BytesIO
import nbt

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
        # return "minecraft:plains"
    biomeId = response.text.split(":")
    biome_info = biomeId[6].split(";")
    biome = biome_info[1].split(",")
    return biome[0]


def getAllBiome():
    bytes_information = worldLoader.getChunks(-4, -4, 9, 9, 'bytes')
    file_like = BytesIO(bytes_information)
    nbt_file = nbt.nbt.NBTFile(buffer=file_like)
    discovered_chunks = {}
    for y in range(81):
        for x in range(1024):
            if f"{nbt_file['Chunks'][y]['Level']['Biomes'].value[x]}" in discovered_chunks:
                discovered_chunks[f"{nbt_file['Chunks'][y]['Level']['Biomes'].value[x]}"] = int(
                    discovered_chunks[f"{nbt_file['Chunks'][y]['Level']['Biomes'].value[x]}"]) + 1
            else:
                discovered_chunks[f"{nbt_file['Chunks'][y]['Level']['Biomes'].value[x]}"] = "1"
    max = 0
    saved_biome = 0
    for x, y in discovered_chunks.items():
        if y > max:
            saved_biome = x
            max = y
    value = getNameBiome(saved_biome)

    return value


def getNameBiome(biome):
    file_in = open("data/biome.txt")
    lines = file_in.readlines()
    biome_name = lines[int(biome)].split(":")[0]
    print(biome_name)
    value = int(lines[int(biome)].split(":")[1])

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
            if len(lines[currentLine]) > 0:
                if len(parts[i]) + 1 <= 15 - len(lines[currentLine]):
                    if "\n" in parts[i]:
                        jumpLine = True
                    lines[currentLine] += " " + parts[i].replace("\n", "")
                    i += 1
                else:
                    jumpLine = True
            else:
                if len(parts[i]) <= 15 - len(lines[currentLine]):
                    if "\n" in parts[i]:
                        jumpLine = True
                    lines[currentLine] += parts[i].replace("\n", "")
                    i += 1
                else:
                    jumpLine = True

            if jumpLine:
                currentLine += 1


def addResourcesFromChunk(resources, settlementData, biome):
    if biome == "-1":
        return

    dictResources = resources.biomesBlocks[biome]
    if "woodResources" in dictResources:
        settlementData.resources["woodResources"] += dictResources["woodResources"]
    if "dirtResources" in dictResources:
        settlementData.resources["dirtResources"] += dictResources["dirtResources"]
    if "stoneResources" in dictResources:
        settlementData.resources["stoneResources"] += dictResources["stoneResources"]


"""
Return result and word
result 0 -> No replacement pattern founded
result 1 -> Replacement pattern founded and replacement successful
result -1 -> Error
"""


def changeNameWithReplacements(name: str, replacements: dict):
    index = name.find("*")
    if index != -1:
        secondIndex = name.find("*", index + 1)
        if secondIndex == -1:
            return [-1, name]

        word = name[index + 1: secondIndex]
        replaced: bool = True
        for key in replacements.keys():
            if key == word:
                return [1, name.replace("*" + word + "*", replacements[key])]

        # If the replacement pattern can't be replaced
        if not replaced:
            return [-1, name]

    return [0, name]


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


def spawnVillagerForStructure(settlementData, structure, position: list):
    for villager in structure.villagers:
        if (structure.type == "houses" and villager.job == "Unemployed") or (
                structure.type != "houses" and villager.job != "Unemployed"):
            spawnVillager(position[0], position[1] + 1, position[2], villager, settlementData.biome_name)


def spawnVillager(x: int, y: int, z: int, villager: Villager, villagerType: str):
    command = "summon minecraft:villager " + str(x) + " " + str(y) + " " + str(z) + " "
    command += "{VillagerData:{profession:" + villager.minecraftJob + ",level:" + str(villager.jobLevel) + ",type:" \
               + villagerType + "},CustomName:""\"\\" + '"' + str(villager.name) + "\\" + '""' \
               + createOffer(villager) + "}"

    # print(command)

    interfaceUtils.runCommand(command)


def createOffer(villager: Villager, isFirstArgument: bool = False) -> str:
    if villager.hasNoTrade():
        return ""

    result: str = "Offers:{Recipes:["

    first: bool = True
    for trade in villager.trades:
        result += trade.toStr(first)

        first = False

    result += "]}"

    if not isFirstArgument:
        result = "," + result
    return result


# Add items to a chest
# Items is a list of [item string, item quantity]
def addItemChest(x, y, z, items):
    for identifier, v in enumerate(items):
        command = "replaceitem block {} {} {} {} {} {}".format(x, y, z,
                                                               "container." + str(identifier),
                                                               v[0],
                                                               v[1])
        interfaceUtils.runCommand(command)


IGNORED_BLOCKS: list = ['minecraft:oak_leaves', 'minecraft:birch_leaves', 'minecraft:spruce_leaves',
                        'minecraft:dark_oak_leaves', 'minecraft:jungle_leaves', 'minecraft:acacia_leaves'
                        'minecraft:oak_log', 'minecraft:birch_log', 'minecraft:spruce_log', 'minecraft:jungle_log',
                        'minecraft:acacia_log', 'minecraft:dark_oak_log']

IGNORED_BLOCKS.extend(lookup.PLANTS)


def getHighestNonAirBlock(cx, cz, local_x, local_z):
    cy = interfaceUtils.globalWorldSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"][local_x, local_z] - 1

    ## Find highest non-air block
    while interfaceUtils.getBlock(cx, cy-1, cz) in IGNORED_BLOCKS:
        cy -= 1

    return cy


# Create a book item from a text
def makeBookItem(text, title="", author="", desc=""):
    booktext = "pages:["
    while len(text) > 0:
        page = text[:15 * 23]
        text = text[15 * 23:]
        bookpage = "'{\"text\":\""
        while len(page) > 0:
            line = page[:23]
            page = page[23:]
            bookpage += line + "\\\\n"
        bookpage += "\"}',"
        booktext += bookpage

    booktext = booktext + "],"

    booktitle = "title:\"" + title + "\","
    bookauthor = "author:\"" + author + "\","
    bookdesc = "display:{Lore:[\"" + desc + "\"]}"
    return "written_book{" + booktext + booktitle + bookauthor + bookdesc + "}"


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

    for key in a.keys():
        if not b.keys().contains(key):
            return False

        if a[key] != b[key]:
            return False

    return True


def applyBlockTransformation(block: str, block_transformations: list):
    for block_transformation in block_transformations:
        block = block_transformation.replaceBlock(block)

    return block


def applyBlockTransformationThenPlace(world_modification, position_x: int, position_y: int, position_z: int,
                                      block: str, block_transformations: list) -> None:
    world_modification.setBlock(position_x, position_y, position_z,
                                applyBlockTransformation(block, block_transformations))


def applyBlockTransformationThenFill(world_modification, from_x: int, from_y: int, from_z: int,
                                     to_x: int, to_y: int, to_z: int, block: str,
                                     block_transformations: list):
    for x in range(from_x, to_x):
        for y in range(from_y, to_y):
            for z in range(from_z, to_z):
                applyBlockTransformationThenPlace(world_modification, x, y, z, block, block_transformations)


def selectNWithChanceForOther(elements: list, chances: list, number: int, required_change_uniform=False):
    import random

    if number >= len(elements):
        return elements

    results: list = []
    cpy: list = elements.copy()
    cpy_chances: list = chances.copy()

    for i in range(number):
        index: int
        if required_change_uniform:
            chance_sum: float = 0
            for chance in cpy_chances:
                chance_sum += chance

            result: float = random.uniform(0, chance_sum)
            index = -1
            while result > 0:
                result -= cpy_chances[index]
                index += 1
        else:
            index: int = 0 if len(cpy) == 1 else random.randint(1, len(cpy) - 1)

        results.append(cpy[index])

        del cpy[index]
        del cpy_chances[index]

    for i in range(len(cpy)):
        if random.uniform(0, 1) < chances[i]:
            results.append(cpy[i])

    return results


def returnCurrencyItem(villageNameItem: str) -> str:
    return "minecraft:emerald{display:{Name:'{\"text\":\"" + villageNameItem + '"}\',Lore:[\'{"text":"Currency used on that village to trade","color":"dark_aqua"}\']}}'


def returnCurrencyTrade(villageNameItem: str) -> str:
    return "\"minecraft:emerald\", tag:{display:{Name:'{\"text\":\"" + villageNameItem + "\"}',Lore:['{\"text\":\"Currency used on that village to trade\",\"color\":\"dark_aqua\"}']}}"
