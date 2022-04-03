from generation.data.village import Village
from generation.data.villager import Villager
from generation.data.trade import Trade

from generation.data.loreStructure import LoreStructure
from generation.chestGeneration import ChestGeneration
from generation.structures.blockTransformation.oldStructureTransformation import OldStructureTransformation
from generation.structures.blockTransformation.damagedStructureTransformation import DamagedStructureTransformation
from generation.structures.blockTransformation.burnedStructureTransformation import BurnedStructureTransformation
from generation.structures.blockTransformation.abandonedStructureTransformation import AbandonedStructureTransformation
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

structure_name: str = "mediumhouse1"
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
    block_transformation: list = [OldStructureTransformation(), DamagedStructureTransformation(), BurnedStructureTransformation(), AbandonedStructureTransformation()]

    # Create Village
    village: Village = Village()
    village.name = "TestLand"
    village.tier = 2

    villagers: list = [Villager(village), Villager(village), Villager(village), Villager(village), Villager(village)]
    villagers[0].name = "Rodriguez 1"
    villagers[1].name = "Rodriguez 2"
    villagers[2].name = "Rodriguez 3"
    villagers[2].minecraftJob = "leatherworker"
    villagers[2].job = "Mayor"
    villagers[3].name = "Rodriguez 4"

    deadVillagers: list = [Villager(village)]
    deadVillagers[0].name = "Rodriguez 5"

    village.villagers = villagers
    village.dead_villagers = deadVillagers

    resources: Resources = Resources()
    resLoader.loadAllResources(resources)
    chestGeneration: ChestGeneration = ChestGeneration(resources, interface)
    structure: BaseStructure = resources.structures[structure_name]
    structure.setupInfoAndGetCorners()

    lore_structure: LoreStructure = LoreStructure()
    lore_structure.age = 1
    lore_structure.flip = 1
    lore_structure.rotation = 1
    """lore_structure.destroyed = True
    lore_structure.causeDestroy = {"burned": "burned", "abandoned": "abandoned", "damaged": "damaged"}"""

    lore_structure.name = structure_name
    lore_structure.villagers = [villagers[0], villagers[2]]
    lore_structure.type = structure_type
    lore_structure.position = [build_area[0] + size_area[0] / 2, 63, build_area[2] + size_area[1] / 2]
    lore_structure.prebuildingInfo = structure.getNextBuildingInformation(lore_structure.flip, lore_structure.rotation)

    settlementData: SettlementData = generator.createSettlementData(build_area, village, resources)
    loreMaker.voteForColor(settlementData)

    generator.generateStructure(lore_structure, settlementData, resources, world_modifications, chestGeneration, block_transformation)
    for villager in lore_structure.villagers:
        if villager.job == Villager.DEFAULT_JOB:
            continue

        Trade.generateFromTradeTable(village, villager, resources.trades[villager.job], settlementData.getMatRepDeepCopy())

    util.spawnVillagerForStructure(settlementData, lore_structure, lore_structure.position)

    world_modifications.saveToFile(file)
else:
    if args.remove == "r":
        world_modifications.loadFromFile(file)
    else:
        world_modifications.loadFromFile(args.remove)
    world_modifications.undoAllModification()
