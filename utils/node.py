
class Node:
    def __init__(self, point: list):
        self.point: list = point
        self.parent: Node = None
        self.cost: int = 0
        self.H: int = 0

    def move_cost(self, other):
        return 1

    def manhattan(self, point2) -> int:
        return abs(point2.point[0] - self.point[0]) + abs(point2.point[1] - self.point[1])

    def children(self) -> list:
        x, z = self.point
        links: list = []

        for d in [(x - 1, z), (x, z - 1), (x, z + 1), (x + 1, z)]:
            links.append(Node([d[0], d[1]]))

        return links

    def compareTo(self, node2) -> int:
        if self.H < node2.H:
            return 1
        elif self.H == node2.H:
            return 0
        else:
            return -1

    def isInClosedList(self, closed_list: list) -> bool:
        for i in closed_list:
            if self.point == i.point:
                return True

        return False

    def isInListWithInferiorCost(self, node_list: list) -> bool:
        for i in node_list:
            if self.point == i.point:
                if i.H < self.H:
                    return True

        return False


class LogNode:
    def __init__(self, point: list):
        self.point: list = point
        self.child = None
