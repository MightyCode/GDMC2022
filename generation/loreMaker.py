import random 


def alterSettlementDataWithNewStructures(settlementData, indexNewStructure):
    structureName = settlementData.structures[indexNewStructure]["name"]

    if structureName == "basictownhall":
        voteForColor(settlementData)


def voteForColor(settlementData):
    colors = ["white", "orange", "magenta", "light_blue", "yellow", "lime", "pink", "gray", "light_gray", "cyan", "purple", "blue", "brown", "green", "red", "black"]
    color = colors[random.randint(0, len(colors) - 1)]
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
    settlementData.setMaterialReplacement("banner",  "minecraft:" + color + "_banner")
    settlementData.setMaterialReplacement("wall_banner", "minecraft:" + color + "_wall_banner")
