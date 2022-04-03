from generation.data.village import Village

import random
import utils.projectMath as projectMath


class VillageInteraction:
    MAX_DISTANCE_TO_MAKE_RELATIONS = 2000

    STATE_WAR = 0
    STATE_TENSION = 1
    STATE_NEUTRAL = 2
    STATE_FRIENDSHIP = 3
    STATE_LOVE = 4

    CHANCE_WAR = 0.12
    CHANCE_TENSION = 0.18
    CHANCE_NEUTRAL = 0.40
    CHANCE_FRIENDSHIP = 0.28
    CHANCE_LOVE = 0.12

    # Relation reason
    UNKNOWN_REASON = 0

    # Why war
    REASON_SAME_COLOR = 1

    # Why neutral
    REASON_TWO_FRIENDS_WENT_IN_WAR = 2

    def __init__(self, village1: Village, village2: Village) -> None:
        self.village1: Village = village1
        self.village2: Village = village2

        self.distance = projectMath.euclideanDistance2D(self.village1.position, self.village2.position)

        self.state = self.computeState()

        self.brokeTheirRelation: bool = False

        self.reason: int = VillageInteraction.UNKNOWN_REASON

    def computeState(self) -> int:
        if self.distance >= VillageInteraction.MAX_DISTANCE_TO_MAKE_RELATIONS:
            return VillageInteraction.STATE_NEUTRAL

        temp: list = [[VillageInteraction.CHANCE_WAR, VillageInteraction.STATE_WAR],
                      [VillageInteraction.CHANCE_TENSION, VillageInteraction.STATE_TENSION],
                      [VillageInteraction.CHANCE_NEUTRAL, VillageInteraction.STATE_NEUTRAL],
                      [VillageInteraction.CHANCE_FRIENDSHIP, VillageInteraction.STATE_FRIENDSHIP],
                      [VillageInteraction.CHANCE_LOVE, VillageInteraction.STATE_LOVE]]

        sum_weight: int = 0
        for category in temp:
            sum_weight += category[0]

        result: int = random.uniform(0, sum_weight)

        for category in temp:
            result -= category[0]
            if result <= 0:
                return category[1]

        return VillageInteraction.STATE_NEUTRAL
