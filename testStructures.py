from generation.data.village import Village
from generation.data.villager import Villager
from generation.data.villageInteraction import VillageInteraction

from generation.data.loreStructure import LoreStructure
from generation.chestGeneration import ChestGeneration
from generation.structures.blockTransformation.oldStructureTransformation import OldStructureTransformation
from generation.structures.blockTransformation.damagedStructureTransformation import DamagedStructureTransformation
from generation.structures.blockTransformation.burnedStructureTransformation import BurnedStructureTransformation
from generation.structures.blockTransformation.abandonedStructureTransformation import AbandonedStructureTransformation
from generation.resources import Resources
from utils.worldModification import WorldModification
from generation.data.murdererData import MurdererData
from generation.structures.baseStructure import BaseStructure
from generation.data.settlementData import SettlementData

from generation.wallConstruction import WallConstruction

import generation.resourcesLoader as resLoader
import utils.argumentParser as argParser
import lib.interfaceUtils as interfaceUtil
import generation.generator as generator
import utils.checkOrCreateConfig as chock

"""
Important information
"""

structure_name: str = "mediumhouse3"
structure_type: str = LoreStructure.TYPE_HOUSES

config: dict = chock.getOrCreateConfig()

file: str = "temp.txt"
interfaceUtil.setCaching(True)
interfaceUtil.setBuffering(True)
world_modifications: WorldModification = WorldModification(config)
args, parser = argParser.giveArgsAndParser()
build_area = argParser.getBuildArea(args)

if build_area == -1:
    exit()

build_area: tuple = (
    build_area[0], build_area[1], build_area[2], build_area[3] - 1, build_area[4] - 1, build_area[5] - 1)
size_area: list = [build_area[3] - build_area[0] + 1, build_area[5] - build_area[2] + 1]

if not args.remove:
    block_transformations: list = [OldStructureTransformation(), DamagedStructureTransformation(),
                                   BurnedStructureTransformation(), AbandonedStructureTransformation()]

    # Create Village
    village: Village = Village()
    village.name = "TestLand"
    village.tier = 2

    otherVillage: Village = Village()
    otherVillage.name = "TestLand 2"
    village.village_interactions[otherVillage] = (
        VillageInteraction(village, otherVillage)
    )
    # Force relation for tests
    village.village_interactions[otherVillage].economicalRelation = True

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
    village.murderer_data = MurdererData()
    """village.murderer_data.villagerTarget = villagers[2]
    village.murderer_data.villagerMurderer = villagers[0]"""

    from generation.wallConstruction import WallConstruction

    wallConstruction: WallConstruction = WallConstruction(village, 8)
    wallConstruction.setConstructionZone(build_area)

    wallConstruction.addRectangle([build_area[0] + 100, build_area[2] + 100, build_area[0] + 116, build_area[2] + 116])
    wallConstruction.addRectangle([build_area[0] + size_area[0] // 2 - 10, build_area[2] + size_area[1] // 2 - 10,
                                   build_area[0] + size_area[0] // 2 + 10, build_area[2] + size_area[1] // 2 + 10])
    wallConstruction.computeWall(WallConstruction.BOUNDING_RECTANGULAR)
    #wallConstruction.showImageRepresenting()
    wallConstruction.placeWall(world_modifications)
    exit()

    resources: Resources = Resources()
    resLoader.loadAllResources(resources)
    chestGeneration: ChestGeneration = ChestGeneration(resources)

    structure: BaseStructure = resources.structures[structure_name]
    """reference_structure: BaseStructure = resources.structures[structure_name]
    
    from generation.structures.generated.structureInConstruction import StructureInConstruction
    structure: BaseStructure = StructureInConstruction(reference_structure)
    print(structure.setupInfoAndGetCorners())"""

    lore_structure: LoreStructure = LoreStructure()
    lore_structure.age = 1
    lore_structure.flip = 0
    lore_structure.rotation = 0
    lore_structure.destroyed = True
    # lore_structure.causeDestroy = {"burned": "burned", "abandoned": "abandoned", "damaged": "damaged"}

    lore_structure.name = structure_name
    lore_structure.villagers = [villagers[0], villagers[2], villagers[2]]
    lore_structure.type = structure_type
    lore_structure.position = [build_area[0] + size_area[0] / 2, 66, build_area[2] + size_area[1] / 2]
    lore_structure.preBuildingInfo = structure.getNextBuildingInformation(lore_structure.flip, lore_structure.rotation)

    settlement_data: SettlementData = generator.createSettlementData(build_area, village, resources)

    village.lore_structures.append(lore_structure)
    import generation.loreMaker as loreMaker

    loreMaker.generateOrders(village)

    structure.block_transformation = block_transformations

    import utils.book as book

    for i in [0, 2]:
        villagers[i].diary = book.createBookForVillager(settlement_data.village_model, villagers[i])
        villagers[i].diary[0].setInfo(title="Diary of " + villagers[i].name, author=villagers[i].name,
                                      description="Diary of " + villagers[i].name)

        villagers[i].diary[0] = "minecraft:written_book" + villagers[i].diary[0].printBook()

    generator.generateStructure(lore_structure, settlement_data, resources, world_modifications,
                                chestGeneration, block_transformations)

    """
    from generation.data.trade import Trade
    for villager in lore_structure.villagers:
        if villager.job == Villager.DEFAULT_JOB:
            continue

        Trade.generateFromTradeTable(village, villager, resources.trades[villager.job], settlement_data.getMatRepDeepCopy())

    util.spawnVillagerForStructure(settlement_data, lore_structure, lore_structure.position)"""

    books: dict = generator.generateVillageBooks(settlement_data)
    generator.placeBooks(settlement_data, books, world_modifications)

    world_modifications.saveToFile(file)
else:
    if args.remove == "r":
        world_modifications.loadFromFile(file)
    else:
        world_modifications.loadFromFile(args.remove)
    world_modifications.undoAllModification()
