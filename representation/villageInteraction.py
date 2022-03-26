from representation.village import Village

import random


class VillageInteraction:
    STATE_WAR = 0
    CHANCE_WAR = 0.10
    STATE_TENSION = 1
    CHANCE_TENSION = 0.10
    STATE_NEUTRAL = 2
    STATE_FRIENDSHIP = 3
    STATE_LOVE = 4

    # Why war
    REASON_SAME_COLOR = 1

    def __init__(self, village1: Village, village2: Village) -> None:
        self.village1: Village = village1
        self.village2: Village = village2

        self.state = random.randint(0, 4)

        self.brokeTheirRelation: bool = False

        self.reason: int = 0
