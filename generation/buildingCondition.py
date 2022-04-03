from generation.data.loreStructure import LoreStructure


class BuildingCondition:
    def __init__(self) -> None:
        self.size: list = [0, 0, 0]
        self.position: list = [0, 0, 0]
        self.referencePoint: list = [0, 0, 0]
        self.rotation: int = 0
        self.flip: int = 0
        self.replaceAirMethod: int = 0
        self.replacements: dict = {}
        self.loreStructure: LoreStructure = None
        self.preBuildingInfo: dict = {}
        self.special: dict = {}
