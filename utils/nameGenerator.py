import random

class NameGenerator:
    VILLAGER_NAME_PATH = "data/names/"

    def __init__(self) -> None:
        self.nameToGenerate = []

        with open(NameGenerator.VILLAGER_NAME_PATH + "villagerFirstNames.txt", "r") as f:
            self.firstNames = f.read().replace("\n", "").split(";")
            f.close()

        with open(NameGenerator.VILLAGER_NAME_PATH + "villagerLastNames.txt", "r") as f:
            self.lastNames = f.read().replace("\n", "").split(";")
            f.close()

        for i in range(len(self.firstNames)):
            for j in range(len(self.lastNames)):
                self.nameToGenerate.append([i, j])

        with open(NameGenerator.VILLAGER_NAME_PATH + "villageNames.txt", "r") as f:
            self.villageNames = f.read().replace("\n", "").split(";")[0:-1]
            print(self.villageNames)
            f.close()


    def generateVillagerName(self, removeName:bool=True)->str:
        if len(self.nameToGenerate) <= 0:
            print("No name remaining to generate")
            exit()

        index = random.randint(0, len(self.nameToGenerate) - 1)
        name = self.firstNames[self.nameToGenerate[index][0]] + " " + self.lastNames[self.nameToGenerate[index][1]]
        if removeName:
            del self.nameToGenerate[index]
        return name


    def generateVillageName(self, removeName:bool=True)->str:
        index = random.randint(0, len(self.villageNames) - 1)
        name = self.villageNames[index]
        if removeName:
            del self.villageNames[index]
        return name