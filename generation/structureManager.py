import utils.util as util
import utils.book as book
import json
import random

class StructureManager:
    PATH = "data/structures/dependencies.json"
    HOUSES = "houses"
    FUNCTIONALS = "functionals"
    REPRESENTATIVES = "representatives"

    def __init__(self, settlementData, resources):
        with open(StructureManager.PATH) as json_file:
           self.dependencies = json.load(json_file)
        self.settlementData = settlementData
        self.resources = resources

        self.numberOfStructuresForEachGroup = {}
        for group in self.dependencies.keys():
            self.numberOfStructuresForEachGroup[group] = 0

        self.villagerFirstNamesList = book.getFirstNamelist()
        self.villagerLastNamesList = book.getLastNamelist()

        self.checkDependencies()


    """
    Set the name of the last append structure in the table, attribute villager to it too if needed
    """
    def chooseOneStructure(self):
        # No more structures placeable
        if len(self.allStructures) == 0:
            return 2

        self.settlementData["structures"].append({})
        sumWeight = 0
        for structure in self.allStructures :
            if "priority" in self.dependencies[structure["group"]] :
                if self.dependencies[structure["group"]]["priority"] == "full":
                    #print("priority to " + structure["name"])
                    self.choosedStructure(structure)
                    # Normal exit
                    return 0

            sumWeight += structure["weight"]

        randomValue = random.randint(0, sumWeight)

        for structure in self.allStructures :
            randomValue -= structure["weight"]
            if randomValue <= 0:
                self.choosedStructure(structure)
                structure["weight"] -= 1
                if structure["weight"] < 1 : 
                    structure["weight"] = 1
                    
                # Normal exit
                return 0


    def choosedStructure(self, structure):
        self.settlementData["structures"][-1]["name"] = structure["name"]
        self.settlementData["structures"][-1]["type"] = structure["type"]
        self.settlementData["structures"][-1]["group"] = structure["group"]
        
        self.numberOfStructuresForEachGroup[structure["group"]] += 1

        struct = self.resources.structures[structure["name"]]

        # Houses structure
        if structure["type"] == StructureManager.HOUSES:
            numberToAdd = struct.info["villageInfo"]["villager"]
            self.settlementData["structures"][-1]["villagersId"] = []
            size = len(self.settlementData["villagerNames"])
            for i in range(numberToAdd):
                self.settlementData["villagerNames"].append(
                            book.getRandomVillagerNames(self.villagerFirstNamesList, 1)[0] + 
                            " " + book.getRandomVillagerNames(self.villagerLastNamesList, 1)[0]
                )
                
                self.settlementData["villagerProfession"].append("Unemployed")
                self.settlementData["villagerGameProfession"].append("nitwit")

                self.settlementData["structures"][-1]["villagersId"].append(size + i)
            self.settlementData["freeVillager"] += numberToAdd
        
        # Functionnals or representatives structure
        elif structure["type"] == StructureManager.FUNCTIONALS or structure["type"] == StructureManager.REPRESENTATIVES:
            numberToAttribute = struct.info["villageInfo"]["villager"]
            self.settlementData["structures"][-1]["villagersId"] = []
            size = len(self.settlementData["villagerNames"])
            idFound = 0
            for i in range(numberToAttribute):
                # Find unemployed villager

                while idFound < len(self.settlementData["villagerProfession"]) :
                    if self.settlementData["villagerProfession"][idFound] == "Unemployed" :
                        break
                    idFound += 1


                self.settlementData["villagerProfession"][idFound] = struct.info["villageInfo"]["profession"]
                self.settlementData["villagerGameProfession"][idFound] = struct.info["villageInfo"]["gameProfession"]

                self.settlementData["structures"][-1]["villagersId"].append(idFound)

            self.settlementData["freeVillager"] -= numberToAttribute
    

    def removeLastStructure(self):
        group = self.settlementData["structures"][-1]["group"]
        self.numberOfStructuresForEachGroup[group] -= 1

        type = self.settlementData["structures"][-1]["type"]
        if type == StructureManager.HOUSES:
            number = len(self.settlementData["structures"][-1]["villagersId"])
            for villagerIndex in self.settlementData["structures"][-1]["villagersId"]:
                self.removeOneVillager(villagerIndex)
                
            self.settlementData["freeVillager"] -= number
        elif type == StructureManager.REPRESENTATIVES or type == StructureManager.FUNCTIONALS:
            number = len(self.settlementData["structures"][-1]["villagersId"])
            for villagerIndex in self.settlementData["structures"][-1]["villagersId"]:
                self.settlementData["villagerProfession"][villagerIndex] = "Unemployed"
                self.settlementData["villagerGameProfession"][villagerIndex] = "nitwit"

            self.settlementData["freeVillager"] += number
        

        del self.settlementData["structures"][-1]
    

    def removeOneVillager(self, index):
        del self.settlementData["villagerNames"][index]
        del self.settlementData["villagerProfession"][index]
        del self.settlementData["villagerGameProfession"][index]

        for structureData in self.settlementData["structures"]:
            for i in range(len(structureData["villagersId"])):
                if structureData["villagersId"][i] > index:
                    structureData["villagersId"][i] -= 1

    def checkDependencies(self):
        # Make arrays empty
        self.houses = []
        self.functionals = []
        self.reprentatives = []
        self.allStructures = []

        # For each node of our structures tree
        for group in self.dependencies.keys():
            # Check if the group can be add
            conditions = True
            for condition in self.dependencies[group]["conditions"] :

                if not self.checkOneCondition(condition, self.dependencies[group]["conditions"][condition]):
                    # Go to the next group
                    conditions = False
                    break

            if not conditions:
                continue
            
            # Add all the structure of this group
            for structure in self.dependencies[group]["structures"]:
                weight = 1
                if self.dependencies[group]["type"] == StructureManager.FUNCTIONALS:
                    weight = 10
                elif self.dependencies[group]["type"] == StructureManager.REPRESENTATIVES:
                    weight = 15

                #Reduce weight of structure
                if len(self.settlementData["structures"]) >= 1 :
                    if structure == self.settlementData["structures"][-1]["name"]:
                        weight = weight / 1.5

                if len(self.settlementData["structures"]) >= 2 :
                    if structure == self.settlementData["structures"][-2]["name"]:
                        weight = weight / 1.3
                weight = int(weight)

                data = { "name" : structure, "group" : group, "type" : self.dependencies[group]["type"], "weight" : weight }

                if data["type"] == StructureManager.HOUSES :
                    self.houses.append(data)
                elif data["type"] == StructureManager.FUNCTIONALS : 
                    self.functionals.append(data)
                elif data["type"] == StructureManager.REPRESENTATIVES : 
                    self.reprentatives.append(data)
                self.allStructures.append(data)


    def checkOneCondition(self, name, conditionValues):
        valueToCheck = 0

        if name == "villagerNeeded" :
            valueToCheck =  self.settlementData["freeVillager"]

        # Ex : dirtResources, woordResources
        elif "Resources" in name:
            valueToCheck =  self.settlementData[name]
        elif name == "previous":
            for previous in conditionValues:
                if not self.checkOneCondition("previousItem", previous):
                    return False
            return True

        elif name == "previousItem":
            valueToCheck = self.numberOfStructuresForEachGroup[conditionValues["name"]]

        if "min" in conditionValues:
            if valueToCheck < conditionValues["min"] :
                return False
        
        if "max" in conditionValues : 
            if valueToCheck >= conditionValues["max"] :
                return False

        return True

    def printStructureChoose(self):
        string = "\n["
        for structure in self.settlementData["structures"]:
            string = string + structure["name"] + ", " 
        print(string + "]") 
