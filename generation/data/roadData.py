from generation.data.loreStructure import LoreStructure

class roadData:
    def __init__(self, structure1: LoreStructure, structure2: LoreStructure):
        self.structure_ref_1: LoreStructure = structure1
        self.structure_ref_2: LoreStructure = structure2
        self.path: list = []

    def path(self, path: list):
        self.path = path

    def isAbandonnedRoad(self) -> bool:
        return self.structure_ref_1.destroyed or self.structure_ref_2.destroyed
