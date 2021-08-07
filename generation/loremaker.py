import random 


def alterSettlementDataWithNewStructures(settlementData, indexNewStructure):
    structureName = settlementData["structures"][indexNewStructure]["name"]

    if structureName == "basictownhall":
        voteForColor(settlementData)


def voteForColor(settlementData):
    colors = ["white", "orange", "magenta", "light_blue", "yellow", "lime", "pink", "gray", "light_gray", "cyan", "purple", "blue", "brown", "green", "red", "black"]
    color = colors[random.randint(0, len(colors) - 1)]
    fillSettlementDataWithColor(settlementData, color)
    

def fillSettlementDataWithColor(settlementData, color):
    settlementData["materialsReplacement"]["color"] = color
    settlementData["materialsReplacement"]["wool"] = "minecraft:" + color + "_wool"
    settlementData["materialsReplacement"]["terracota"] = "minecraft:" + color + "_terracota"
    settlementData["materialsReplacement"]["carpet"] = "minecraft:" + color + "_carpet"
    settlementData["materialsReplacement"]["stained_glass"] = "minecraft:" + color + "_stained_glass"
    settlementData["materialsReplacement"]["shulker_box"] = "minecraft:" + color + "_shulker_box"
    settlementData["materialsReplacement"]["glazed_terracota"] = "minecraft:" + color + "_glazed_terracota"
    settlementData["materialsReplacement"]["stained_glass_pane"] = "minecraft:" + color + "_stained_glass_pane"
    settlementData["materialsReplacement"]["concrete"] = "minecraft:" + color + "_concrete"
    settlementData["materialsReplacement"]["concrete_powder"] = "minecraft:" + color + "_concrete_powder"
    settlementData["materialsReplacement"]["dye"] = "minecraft:" + color + "_dye"
    settlementData["materialsReplacement"]["bed"] = "minecraft:" + color + "_bed"
    settlementData["materialsReplacement"]["banner"] = "minecraft:" + color + "_banner"
    settlementData["materialsReplacement"]["wall_banner"] = "minecraft:" + color + "_wall_banner"
