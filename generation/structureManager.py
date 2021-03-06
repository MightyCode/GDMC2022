from generation.data.settlementData import SettlementData
from generation.data.village import Village
from generation.data.villager import Villager
from generation.data.loreStructure import LoreStructure
from generation.resources import Resources
from utils.nameGenerator import NameGenerator
import json
import random


class StructureManager:
    PATH = "data/structures/dependencies.json"

    def __init__(self, settlementData: SettlementData, resources: Resources, nameGenerator: NameGenerator):
        self.current_group_checked = ""
        self.houses: list = []
        self.functionals: list = []
        self.representatives: list = []

        with open(StructureManager.PATH) as json_file:
            self.dependencies = json.load(json_file)

        self.nameGenerator: NameGenerator = nameGenerator
        self.settlementData = settlementData
        self.village_model: Village = settlementData.village_model
        self.resources: Resources = resources

        self.numberOfStructuresForEachGroup = {}
        for group in self.dependencies.keys():
            self.numberOfStructuresForEachGroup[group] = 0

        self.allStructures = []

        self.checkDependencies()

    """
    Set the name of the last append structure in the table, attribute villager to it too if needed
    """

    def chooseOneStructure(self):
        # No more structures placeable
        if len(self.allStructures) == 0:
            return 2

        sumWeight = 0
        for structure in self.allStructures:
            if "priority" in self.dependencies[structure["group"]]:
                if self.dependencies[structure["group"]]["priority"] == "full":
                    # print("priority to " + structure["name"])
                    self.chosenStructure(structure)
                    # Normal exit
                    return 0

            sumWeight += structure["weight"]

        randomValue = random.randint(0, sumWeight)

        for structure in self.allStructures:
            randomValue -= structure["weight"]
            if randomValue <= 0:
                self.chosenStructure(structure)
                structure["weight"] -= 1
                if structure["weight"] < 1:
                    structure["weight"] = 1

                # Normal exit
                return 0

    def chosenStructure(self, structure: dict):
        self.village_model.lore_structures[-1].name = structure["name"]
        self.village_model.lore_structures[-1].type = structure["type"]
        self.village_model.lore_structures[-1].group = structure["group"]

        self.numberOfStructuresForEachGroup[structure["group"]] += 1

        struct = self.resources.structures[structure["name"]]

        # Houses structure
        if structure["type"] == LoreStructure.TYPE_HOUSES:
            numberToAdd = struct.info["villageInfo"]["villager"]

            for i in range(numberToAdd):
                villager: Villager = Villager(self.village_model)
                villager.name = self.nameGenerator.generateVillagerName(True)

                villager.job = "Unemployed"
                villager.minecraftJob = "nitwit"

                self.village_model.lore_structures[-1].villagers.append(villager)
                self.village_model.villagers.append(villager)

            self.village_model.free_villager += numberToAdd

        # Functionals or representatives structure
        elif structure["type"] == LoreStructure.TYPE_FUNCTIONALS or structure["type"] == LoreStructure.TYPE_REPRESENTATIVES:
            numberToAttribute = struct.info["villageInfo"]["villager"]

            idFound = 0
            for i in range(numberToAttribute):
                # Find unemployed villager

                while idFound < len(self.village_model.villagers):
                    if self.village_model.villagers[idFound].job == "Unemployed":
                        break

                    idFound += 1

                villager: Villager = self.village_model.villagers[idFound]

                villager.job = struct.info["villageInfo"]["profession"]
                villager.minecraftJob = struct.info["villageInfo"]["gameProfession"]

                self.village_model.lore_structures[-1].villagers.append(self.village_model.villagers[idFound])

            self.village_model.free_villager -= numberToAttribute

    def removeLastStructure(self):
        structure: LoreStructure = self.village_model.lore_structures[-1]

        group = structure.group
        self.numberOfStructuresForEachGroup[group] -= 1

        structure_type = structure.type

        if structure_type == LoreStructure.TYPE_HOUSES:
            number = len(structure.villagers)
            for villager in structure.villagers:
                self.removeOneVillager(villager)

            self.village_model.free_villager -= number
        elif structure_type == LoreStructure.TYPE_REPRESENTATIVES or structure_type == LoreStructure.TYPE_FUNCTIONALS:
            for villager in structure.villagers:
                villager.job = "Unemployed"
                villager.minecraftJob = "nitwit"

            self.village_model.free_villager += len(structure.villagers)

        del self.village_model.lore_structures[-1]

    def removeOneVillager(self, villager: Villager):
        self.village_model.villagers.remove(villager)

        for structure in self.village_model.lore_structures:
            if villager in structure.villagers:
                structure.villagers.remove(villager)

    def checkDependencies(self):
        # Make arrays empty
        self.houses.clear()
        self.functionals.clear()
        self.representatives.clear()
        self.allStructures.clear()

        # For each node of our structures tree
        for group in self.dependencies.keys():
            # Check if the group can be added
            conditions = True
            for condition in self.dependencies[group]["conditions"]:
                self.current_group_checked = group
                if not self.checkOneCondition(condition, self.dependencies[group]["conditions"][condition]):
                    # Go to the next group
                    conditions = False
                    break

            if not conditions:
                continue

            # Add all the structure of this group

            for structure in self.dependencies[group]["tier"][str(self.village_model.tier)]:
                weight = 1
                if self.dependencies[group]["type"] == LoreStructure.TYPE_FUNCTIONALS:
                    weight = 10
                elif self.dependencies[group]["type"] == LoreStructure.TYPE_REPRESENTATIVES:
                    weight = 15

                # Reduce weight of structure
                if len(self.village_model.lore_structures) >= 1:
                    if structure == self.village_model.lore_structures[-1].name:
                        weight = weight / 1.5

                if len(self.village_model.lore_structures) >= 2:
                    if structure == self.village_model.lore_structures[-1].name:
                        weight = weight / 1.3
                weight = int(weight)

                data = {"name": structure, "group": group, "type": self.dependencies[group]["type"], "weight": weight}

                if data["type"] == LoreStructure.TYPE_HOUSES:
                    self.houses.append(data)
                elif data["type"] == LoreStructure.TYPE_FUNCTIONALS:
                    self.functionals.append(data)
                elif data["type"] == LoreStructure.TYPE_REPRESENTATIVES:
                    self.representatives.append(data)
                self.allStructures.append(data)

    def checkOneCondition(self, name: str, conditionValues: dict):
        valueToCheck = 0

        # TODO taking into account relation

        if name == "villagerNeeded":
            valueToCheck = self.village_model.free_villager

        # Ex : dirtResources, woodResources
        elif "Resources" in name:
            valueToCheck = self.settlementData.resources[name]
        elif name == "previous":
            for previous in conditionValues:
                if not self.checkOneCondition("previousItem", previous):
                    return False
            return True

        elif name == "previousItem":
            group: str = self.current_group_checked if conditionValues["name"] == "self" else conditionValues["name"]
            valueToCheck = self.numberOfStructuresForEachGroup[group]

        if "min" in conditionValues:
            if valueToCheck < conditionValues["min"]:
                return False

        if "max" in conditionValues:
            if valueToCheck >= conditionValues["max"]:
                return False

        if name == "status":
            for oneStatus in conditionValues["values"]:
                if oneStatus == self.settlementData.village_model.status:
                    return True
            return False

        elif name == "tier":
            for oneStatus in conditionValues["values"]:
                if oneStatus == self.settlementData.village_model.tier:
                    return True
            return False

        elif name == "age":
            for oneStatus in conditionValues["values"]:
                if oneStatus == self.settlementData.village_model.age:
                    return True
            return False

        return True

    def printStructureChoose(self):
        string = ": ["
        for structure in self.village_model.lore_structures:
            string = string + structure.name + ", "

        print(string + "]")
