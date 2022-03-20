from representation.village import Village

import random


class VillageInteraction:
    STATE_WAR = 0
    STATE_TENSION = 1
    STATE_NEUTRAL = 2
    STATE_FRIENDSHIP = 3
    STATE_LOVE = 4

    def __init__(self, village1: Village, village2: Village) -> None:
        self.village1: Village = village1
        self.village2: Village = village2

        # 0 WAR, 1 Tension, 2 Neutral
        self.state = int(random.randint(0, 4))
