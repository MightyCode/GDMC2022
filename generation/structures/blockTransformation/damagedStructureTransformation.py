import random


class DamagedStructureTransformation:
    def __init__(self):
        super().__init__()
        self.lore_structure = None
        self.pre_requisites = False

    def setLoreStructure(self, lore_structure):
        self.lore_structure = lore_structure
        self.pre_requisites = self.lore_structure.destroyed and "damaged" in self.lore_structure.causeDestroy.keys()

    def replaceBlock(self, block: str) -> str:
        if not self.pre_requisites:
            return block

        if "_door" in block:
            return block

        if "torch" in block \
                or "lantern" in block:
            return "minecraft:air"

        if random.randint(1, 10) == 1:
            return "minecraft:air"

        return block
