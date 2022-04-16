from generation.structures.baseStructure import BaseStructure
from generation.buildingCondition import BuildingCondition
import utils.util as util
import copy


class StructureInConstruction(BaseStructure):
    def __init__(self, reference_structure: BaseStructure):
        super(BaseStructure, self).__init__()
        self.reference_structure = reference_structure
        self.setInfo(reference_structure.info)

    def setupInfoAndGetCorners(self):
        self.reference_structure.setupInfoAndGetCorners()

        self.setSize([
            self.reference_structure.size[0] + 1,
            self.reference_structure.size[1],
            self.reference_structure.size[2] + 1
        ])

        self.info["mainEntry"]["position"] = [
            self.reference_structure.info["mainEntry"]["position"][0] + 1,
            self.reference_structure.info["mainEntry"]["position"][1],
            self.reference_structure.info["mainEntry"]["position"][2] + 1,
        ]

        return self.getCornersLocalPositionsAllFlipRotation(self.info["mainEntry"]["position"])

    def getNextBuildingInformation(self, flip, rotation):
        info = {
            "size": self.size,
            "mainEntry": {
                "facing": "north"
            },
            "entry": {
                "position": self.info["mainEntry"]["position"],
                "facing": self.getFacingMainEntry(flip, rotation)
            },
            "corner": self.getCornersLocalPositions(self.info["mainEntry"]["position"].copy(), flip, rotation)
        }

        return info

    def build(self, world_modifications, building_conditions: BuildingCondition, chest_generation,
              block_transformations: list):
        pass
