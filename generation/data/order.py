from generation.data.villager import Villager


class Order:
    def __init__(self):
        self.order_item: str = ""
        self.order_quantity: int = 0
        self.villager_ordering: Villager = None
        self.structure = None