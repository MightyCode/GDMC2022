from generation.data.loreStructure import LoreStructure


class RoadData:
    def __init__(self, structure1: LoreStructure, structure2: LoreStructure):
        self.structure_ref_1: LoreStructure = structure1
        self.structure_ref_2: LoreStructure = structure2
        self.path: list = []

        self.yEntry1: int = 64
        self.yEntry2: int = 64

    def setPath(self, path: list, yEntry1, yEntry2):
        self.path = path
        self.yEntry1 = yEntry1
        self.yEntry2 = yEntry2

    def isAbandonedRoad(self) -> bool:
        return self.structure_ref_1.destroyed or self.structure_ref_2.destroyed
