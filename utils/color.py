class Color:

    COLOR = ["white", "orange", "magenta", "light_blue", "yellow", "lime", "pink", "gray", "light_gray",
             "cyan", "purple", "blue", "brown", "green", "red", "black"]

    @staticmethod
    def strToId(color: str) -> int:
        return Color.COLOR.index(color)
