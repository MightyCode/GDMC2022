import random


class AbandonedStructureTransformation:
    def __init__(self):
        super().__init__()
        self.lore_structure = None
        self.pre_requisites = False

    def setLoreStructure(self, lore_structure):
        self.lore_structure = lore_structure
        self.pre_requisites = self.lore_structure.destroyed and "abandoned" in self.lore_structure.causeDestroy.keys()

    def replaceBlock(self, block: str) -> str:
        if not self.pre_requisites:
            return block

        if "_door" in block:
            return block

        if "chest" in block \
                or "shulker" in block \
                or "lectern" in block \
                or "barrel" in block\
                or "ladder" in block\
                or "torch" in block \
                or "lantern" in block \
                or "wool" in block \
                or "carpet" in block \
                or "leaves" in block:
            return "minecraft:air"

        if "potted" in block:
            return "minecraft:potted_dead_bush"

        if random.randint(1, 10) == 1 and "air" not in block:
            if random.randint(1, 2) == 1:
                return "minecraft:cobweb"
            return "minecraft:air"

        return block
