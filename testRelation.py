from representation.village import VillageInteraction
from utils.nameGenerator import NameGenerator
import generation.loreMaker as loremaker
import matplotlib.pyplot as plt
import math


def state_relation_to_color(state: int) -> str:
    if state == VillageInteraction.STATE_WAR:
        return "red"
    elif state == VillageInteraction.STATE_TENSION:
        return "yellow"
    elif state == VillageInteraction.STATE_FRIENDSHIP:
        return "blue"
    elif state == VillageInteraction.STATE_LOVE:
        return "green"

    return "black"


def plot_relation(positions_x, positions_y, interactions: list) -> None:
    for interaction in interactions:
        x = [positions_x[interaction.village1], positions_x[interaction.village2]]
        y = [positions_y[interaction.village1], positions_y[interaction.village2]]

        color = state_relation_to_color(interaction.state)

        plt.plot(x, y, color=color)


if __name__ == "__main__":
    nameGenerator: NameGenerator = NameGenerator()

    """Generate village involving on our generation"""

    number_to_generate = 10
    positions_of_village = []
    for i in range(number_to_generate):
        positions_of_village.append([500 * i, 0])

    villages: list = loremaker.initializedVillages(positions_of_village, nameGenerator)
    villageInteractions: list = loremaker.createVillageRelationAndAssign(villages)

    positions_x_on_graph: dict = {}
    positions_y_on_graph: dict = {}

    each_part = math.pi * 2 / number_to_generate

    for i in range(number_to_generate):
        village = villages[i]
        positions_x_on_graph[village] = math.cos(i * each_part)
        positions_y_on_graph[village] = math.sin(i * each_part)

    plt.subplot(1, 2, 1)
    plot_relation(positions_x_on_graph, positions_y_on_graph, villageInteractions)

    loremaker.checkForImpossibleInteractions(villages, villageInteractions)

    plt.subplot(1, 2, 2)
    plot_relation(positions_x_on_graph, positions_y_on_graph, villageInteractions)

    plt.show()
