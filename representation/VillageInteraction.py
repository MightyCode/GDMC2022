from representation.Village import Village

import random

class VillageInteraction:
    STATE_WAR = 0
    STATE_TENSION = 1
    STATE_NEUTRAL = 2
    STATE_FRIENDSHIP = 3
    STATE_LOVE = 4

    def __init__(self) -> None:
        self.village1:Village = None
        self.village2:Village = None

        # 0 WAR, 1 Tension, 2 Neutral
        self.state = int(random.randint(0, 4))