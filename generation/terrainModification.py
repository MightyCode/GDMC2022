import utils.projectMath as pmath
import lib.interfaceUtils as iu


class TerrainModification:
    def __init__(self, area, wall_construction):
        self.area = area
        self.wall_construction = wall_construction

    def removeRecursivelyAt(self, world_modification, x, y, z):
        #removed: list = []
        remaining: list = []

        if self.shouldAdd(x, y, z):
            remaining.append([x, y, z])

        while len(remaining) > 0:
            x, y, z = remaining[0]
            world_modification.setBlock(x, y, z, "minecraft:air")
            #removed.append([x, y, z])

            del remaining[0]

            for x_offset in range(-1, 2):
                for y_offset in range(-1, 2):
                    for z_offset in range(-1, 2):
                        if x_offset == 0 and y_offset == 0 and z_offset == 0:
                            continue

                        """if self.isInStack(removed, [x + x_offset, y + y_offset, z + z_offset]):
                            continue"""

                        if self.isInStack(remaining, [x + x_offset, y + y_offset, z + z_offset]):
                            continue

                        if self.shouldAdd(x + x_offset, y + y_offset, z + z_offset):
                            remaining.append([x + x_offset, y + y_offset, z + z_offset])

    def isInStack(self, removed, ref):
        for block in removed:
            if pmath.is3DPointEqual(block, ref):
                return True

        return False

    def shouldAdd(self, x, y, z) -> bool:
        if not pmath.isPointInCube([x, y, z], self.area):
            return False

        if not self.wall_construction.isBlockInEnclosure(x, z):
            return False

        block: str = iu.getBlock(x, y, z)

        return "leaves" in block or "log" in block or block == "minecraft:bee_nest" or "vine" in block or "mushroom" in block
