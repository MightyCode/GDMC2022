import random


class BurnedStructureTransformation:
    def __init__(self):
        super().__init__()
        self.lore_structure = None
        self.pre_requisites = False

    def setLoreStructure(self, lore_structure):
        self.lore_structure = lore_structure
        self.pre_requisites = self.lore_structure.destroyed and "burned" in self.lore_structure.causeDestroy.keys()

    def replaceBlock(self, block: str) -> str:
        if not self.pre_requisites:
            return block

        if "_door" in block \
                or "chest" in block \
                or "shulker" in block \
                or "lectern" in block \
                or "barrel" in block \
                or "ladder" in block \
                or "torch" in block \
                or "lantern" in block \
                or "wool" in block \
                or "carpet" in block:
            return "minecraft:air"

        if "potted" in block:
            return "minecraft:flower_pot"

        if "plank" in block or "stripped" in block:
            if random.randint(1, 5) == 1:
                return "minecraft:coal_block"

        if "log" in block and "stripped" not in block:
            if random.randint(1, 5) == 1:
                return "minecraft:stripped_" + block.replace("minecraft:", "")

        if "minecraft:acacia_slab" == block \
                or "minecraft:spruce_slab" == block \
                or "minecraft:oak_slab" == block \
                or "minecraft:birch_slab" == block \
                or "minecraft:jungle_slab" == block \
                or "minecraft:dark_oak_slab" == block \
                or "minecraft:crimson_slab" == block \
                or "minecraft:warped_slab" == block:
            if random.randint(1, 15) == 1:
                return "minecraft:nether_brick_slab"

        if "minecraft:acacia_stairs" == block \
                or "minecraft:spruce_stairs" == block \
                or "minecraft:oak_stairs" == block \
                or "minecraft:birch_stairs" == block \
                or "minecraft:jungle_stairs" == block \
                or "minecraft:dark_oak_stairs" == block \
                or "minecraft:crimson_stairs" == block \
                or "minecraft:warped_stairs" == block:
            if random.randint(1, 15) == 1:
                return "minecraft:nether_brick_stairs"

        if random.randint(1, 15) == 1:
            return "minecraft:air"

        return block
