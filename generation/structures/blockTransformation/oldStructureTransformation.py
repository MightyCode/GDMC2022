import random


class OldStructureTransformation:
    def __init__(self):
        super().__init__()
        self.lore_structure = None
        self.pre_requisites = False

    def setLoreStructure(self, lore_structure):
        self.lore_structure = lore_structure
        self.pre_requisites = self.lore_structure.age == 1

    def replaceBlock(self, block: str) -> str:
        if not self.pre_requisites:
            return block

        if "minecraft:cobblestone" == block \
            or "minecraft:cobblestone_slab" == block \
            or "minecraft:cobblestone_stairs" == block \
                or "minecraft:cobblestone_wall" == block:
            if random.randint(1, 5) == 1:
                return block.replace("cobblestone", "mossy_cobblestone")

        if "minecraft:chiseled_stone_bricks" == block:
            if random.randint(1, 5) == 1:
                return block.replace("chiseled", "cracked")

        if "minecraft:stone" == block \
                or "minecraft:stone_slab" == block \
                or "minecraft:stone_stairs" == block \
                or "minecraft:stone_wall" == block:
            if random.randint(1, 5) == 1:
                return block.replace("stone", "cobblestone")

        if "minecraft:stone_brick" in block \
                or "minecraft:stone_brick_slab" in block \
                or "minecraft:stone_brick_stairs" in block \
                or "minecraft:stone_brick_wall" in block:
            if random.randint(1, 5) == 1:
                return block.replace("stone_brick", "mossy_stone_brick")

        return block
