from generation.data.loreStructure import LoreStructure
import copy


class BuildingCondition:
    # replaceAllAir : 0 no air placed, 1 place all air block, 2 place all chosen air block, 3 take the preferred replacement air from info file
    NO_AIR_PLACEMENT = 0
    ALL_AIR_PLACEMENT = 1
    CHOSEN_AIR_PLACEMENT = 2
    FILE_PREFERENCE_AIR_PLACEMENT = 3

    """
    size : size of the structure
    position : the of the referencePoint in the real world
    referencePoint : point x, z where the building will rotate around, the block at the reference point will be on position point
    flip : No flip = 0, Flip x = 1, flip z = 2, Flip xz = 3
    rotation : No rotation = 0, rotation 90° = 1, rotation 180° = 2, rotation 270° = 3
    replaceAllAir : 0 no air placed, 1 place all air block, 2 place all chosen air block, 3 take the preferred replacement air from info file
    replacements : change one type of block to another
    preBuildingInfo
    special : dict to put very specific information
    """
    def __init__(self) -> None:
        self.size: list = [0, 0, 0]
        self.position: list = [0, 0, 0]
        self.referencePoint: list = [0, 0, 0]
        self.rotation: int = 0
        self.flip: int = 0
        self.replaceAirMethod: int = BuildingCondition.NO_AIR_PLACEMENT
        self.replacements: dict = {}
        self.loreStructure: LoreStructure = None
        self.preBuildingInfo: dict = {}
        self.special: dict = {}

    def setLoreStructure(self, lore_structure: LoreStructure):
        self.loreStructure = lore_structure
        self.flip = lore_structure.flip
        self.rotation = lore_structure.rotation
        self.position = lore_structure.position

        self.referencePoint = lore_structure.preBuildingInfo["entry"]["position"]
        self.size = lore_structure.preBuildingInfo["size"]
        self.preBuildingInfo = lore_structure.preBuildingInfo

    def __copy__(self):
        new = self.__class__()
        new.size = self.size.copy()
        new.position = self.position.copy()
        new.referencePoint = self.referencePoint.copy()
        new.rotation = self.rotation
        new.flip = self.flip
        new.replaceAirMethod = self.replaceAirMethod
        new.replacements = copy.deepcopy(self.replacements)
        new.loreStructure = self.loreStructure
        new.preBuildingInfo = copy.deepcopy(self.preBuildingInfo)
        new.special = copy.deepcopy(self.special)

        return new
