import os
import lib.interfaceUtils as interfaceUtils


# Class which serve to save all modification, do undo actions
from utils.checkOrCreateConfig import Config


class WorldModification:
    DEBUG_MODE = False

    DEFAULT_PATH = "logs/"
    BLOCK_SEPARATOR = "$"
    PARTS_SEPARATOR = "°"

    def __init__(self):
        self.before_modification: list = []
        self.after_modification: list = []
        self.stateBefore: bool = False

        WorldModification.DEBUG_MODE = Config.LOADED_CONFIG["saveConstructionInFile"]

    def setBlock(self, x, y, z, block, place_immediately=False, compare_block_state=False):
        if WorldModification.DEBUG_MODE:
            previous_block = interfaceUtils.getBlock(x, y, z)

            # We won't replace block by same one, 
            # option to compare or not the state of both blocks -> [...]
            if block.split("[")[0] == previous_block.split("[")[0]:
                if compare_block_state:
                    pass
                    # TODO
                else:
                    return

            self.before_modification.append([x, y, z, previous_block])
            self.after_modification.append([x, y, z, block])

        if place_immediately:
            self.stateBefore = interfaceUtils.globalinterface.isBuffering()
            if self.stateBefore:
                interfaceUtils.setBuffering(False)

            interfaceUtils.setBlock(x, y, z, block)

            if self.stateBefore:
                interfaceUtils.setBuffering(True)
        else:
            interfaceUtils.setBlock(x, y, z, block)

    def fillBlocks(self, from_x, from_y, from_z, to_x, to_y, to_z, block, compare_block_state=False):
        if WorldModification.DEBUG_MODE:
            if from_x > to_x:
                to_x, from_x = from_x, to_x
            if from_y > to_y:
                to_y, from_y = from_y, to_y
            if from_z > to_z:
                to_z, from_z = from_z, to_z

            for z in range(from_z, to_z + 1):
                for x in range(from_x, to_x + 1):
                    for y in range(from_y, to_y + 1):
                        # We won't replace block by same one, 
                        # option to compare or not the state of both blocks -> [...]
                        previous_block = interfaceUtils.getBlock(x, y, z)
                        if block.split("[")[0] == previous_block.split("[")[0]:
                            if compare_block_state:
                                pass
                                # TODO
                            else:
                                continue

                        self.before_modification.append([x, y, z, previous_block])
                        self.after_modification.append([x, y, z, block])

        # interfaceUtils.fill(from_x, from_y, from_z, to_x, to_y, to_z, block)

        interfaceUtils.runCommand("fill " +
                                  str(from_x) + " " +
                                  str(from_y) + " " +
                                  str(from_z) + " " +
                                  str(to_x) + " " +
                                  str(to_y) + " " +
                                  str(to_z) + " " +
                                  block + " replace")

    def undoLastModification(self):
        if not WorldModification.DEBUG_MODE:
            print("CAN'T UNDO IF DEBUG MODE NOT ACTIVATED")
            return

        index = len(self.before_modification) - 1
        interfaceUtils.setBlock(
            self.before_modification[index][0],
            self.before_modification[index][1],
            self.before_modification[index][2],
            self.before_modification[index][3],
        )

        self.before_modification.pop()
        self.after_modification.pop()

    def undoAllModification(self):
        if not WorldModification.DEBUG_MODE:
            print("CAN'T UNDO IF DEBUG MODE NOT ACTIVATED")
            return

        for i in range(len(self.before_modification)):
            self.undoLastModification()

    """
    Save into filename every changement done to the world
    """

    def saveToFile(self, file_name):
        if not WorldModification.DEBUG_MODE:
            print("CAN'T SAVE IF DEBUG MODE NOT ACTIVATED")
            return

        assert (len(self.before_modification) == len(self.after_modification))

        # Check if log path exists
        if not os.path.isdir(WorldModification.DEFAULT_PATH):
            os.makedirs(WorldModification.DEFAULT_PATH)

        if os.path.exists(WorldModification.DEFAULT_PATH + file_name):
            parts = file_name.split(".")
            if len(file_name.split("_")) > 1:
                self.saveToFile(parts[0].split("_")[0] + "_" + str(
                    int(file_name.split("_")[1].split(".")[0]) + 1
                ) + "." + parts[1])
            else:
                self.saveToFile(parts[0] + "_0." + parts[1])
            return

        f = open(WorldModification.DEFAULT_PATH + file_name, "w")
        f.truncate(0)
        for i in range(len(self.before_modification)):
            f.write(
                str(self.before_modification[i][0]) + WorldModification.BLOCK_SEPARATOR +
                str(self.before_modification[i][1]) + WorldModification.BLOCK_SEPARATOR +
                str(self.before_modification[i][2]) + WorldModification.BLOCK_SEPARATOR +
                str(self.before_modification[i][3]) + WorldModification.PARTS_SEPARATOR +
                str(self.after_modification[i][0]) + WorldModification.BLOCK_SEPARATOR +
                str(self.after_modification[i][1]) + WorldModification.BLOCK_SEPARATOR +
                str(self.after_modification[i][2]) + WorldModification.BLOCK_SEPARATOR +
                str(self.after_modification[i][3])
            )

            if i < len(self.before_modification) - 1:
                f.write("\n")
        f.close()

    """
    Load every changement done to a world from a file
    """

    def loadFromFile(self, file_name):
        if not WorldModification.DEBUG_MODE:
            print("CAN'T LOAD IF DEBUG MODE NOT ACTIVATED")
            return

            # Check if log path exists
        if not os.path.isdir(WorldModification.DEFAULT_PATH):
            os.makedirs(WorldModification.DEFAULT_PATH)

        with open(WorldModification.DEFAULT_PATH + file_name) as f:
            for line in f:
                parts = line.split(WorldModification.PARTS_SEPARATOR)
                before_parts = parts[0].split(WorldModification.BLOCK_SEPARATOR)
                after_parts = parts[1].split(WorldModification.BLOCK_SEPARATOR)
                self.before_modification.append([
                    int(before_parts[0]),
                    int(before_parts[1]),
                    int(before_parts[2]),
                    before_parts[3]
                ])

                self.after_modification.append([
                    int(after_parts[0]),
                    int(after_parts[1]),
                    int(after_parts[2]),
                    after_parts[3]
                ])

        os.remove(WorldModification.DEFAULT_PATH + file_name)
