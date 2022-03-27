from representation.village import Village
from representation.villager import Villager
from representation.trade import Trade

from representation.loreStructure import LoreStructure
from generation.chestGeneration import ChestGeneration
from generation.structures.blockTransformation.oldStructureTransformation import OldStructureTransformation
from generation.resources import Resources
from utils.worldModification import WorldModification
from generation.structures.baseStructure import BaseStructure
from generation.data.settlementData import SettlementData

import generation.resourcesLoader as resLoader
import utils.util as util
import utils.argumentParser as argParser
import generation.loreMaker as loreMaker
import lib.interfaceUtils as interfaceUtil
import generation.generator as generator


"""
Important information
"""

structure_name: str = "mediumshop"
structure_type: str = "functionals"


file: str = "temp.txt"
interface: interfaceUtil.Interface = interfaceUtil.Interface(buffering=True, caching=True)
interface.setCaching(True)
interface.setBuffering(True)
interfaceUtil.setCaching(True)
interfaceUtil.setBuffering(True)
world_modifications: WorldModification = WorldModification(interface)
args, parser = argParser.giveArgsAndParser()
build_area = argParser.getBuildArea(args)

if build_area == -1:
    exit()

build_area: tuple = (
    build_area[0], build_area[1], build_area[2], build_area[3] - 1, build_area[4] - 1, build_area[5] - 1)
size_area: list = [build_area[3] - build_area[0] + 1, build_area[5] - build_area[2] + 1]

if not args.remove:
    block_transformation: list = [OldStructureTransformation()]

    # Create Village
    village: Village = Village()
    village.name = "TestLand"

    villagers: list = [Villager(village), Villager(village), Villager(village), Villager(village), Villager(village)]
    villagers[0].name = "Rodriguez 1"
    villagers[0].minecraftJob = "nitwit"
    villagers[1].name = "Rodriguez 2"
    villagers[2].name = "Rodriguez 3"
    villagers[2].minecraftJob = "leatherworker"
    villagers[3].name = "Rodriguez 4"

    deadVillagers: list = [Villager(village)]
    deadVillagers[0].name = "Rodriguez 5"

    village.villagers = villagers
    village.dead_villagers = deadVillagers

    trade: Trade = Trade()
    trade.offer = "minecraft:gold_nugget"
    trade.offer_quantity = 23

    trade.needing = "minecraft:gold_nugget"
    trade.needing_quantity = 1
    villagers[2].trades.append(trade)

    resources: Resources = Resources()
    resLoader.loadAllResources(resources)
    chestGeneration: ChestGeneration = ChestGeneration(resources, interface)
    structure: BaseStructure = resources.structures[structure_name]

    lore_structure: LoreStructure = LoreStructure()
    lore_structure.age = 1
    lore_structure.flip = 1
    lore_structure.rotation = 1
    lore_structure.name = structure_name
    lore_structure.villagers = [villagers[0], villagers[2]]
    lore_structure.type = structure_type
    lore_structure.position = [build_area[0] + size_area[0] / 2, 64, build_area[2] + size_area[1] / 2]
    lore_structure.prebuildingInfo = structure.getNextBuildingInformation(lore_structure.flip, lore_structure.rotation)

    settlementData: SettlementData = generator.createSettlementData(build_area, village, resources)
    loreMaker.voteForColor(settlementData)

    generator.generateStructure(lore_structure, settlementData, resources, world_modifications, chestGeneration, block_transformation)

    util.spawnVillagerForStructure(settlementData, lore_structure, lore_structure.position)
    world_modifications.saveToFile(file)
else:
    if args.remove == "r":
        world_modifications.loadFromFile(file)
    else:
        world_modifications.loadFromFile(args.remove)
    world_modifications.undoAllModification()
