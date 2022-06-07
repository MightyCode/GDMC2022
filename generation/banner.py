import random

from utils.color import Color


class Banner:
    SYMBOLS = ["mc", "bl", "br", "tl", "tr", "hh", "hbb", "bs", "ts", "vh", "vhr", "ls", "cs", "rs", "ms", "sc", "dls",
               "drs", "cr", "ld", "rud", "lud", "rd", "tt", "bt", "mr", "tts", "bts"]

    OVER_SYMBOLS = ["cre", "sku", "flo", "moj", "glb", "pig"]
    UNDER_SYMBOLS = ["cbo", "bo", "ss", "bri", "gra", "gru"]

    TO_BAN = {
        "tr": ["hh", "ts", "vhr"],
        "tl": ["hh", "ts", "vh"],
        "ts": ["hh"],
        "br": ["hhb", "bs", "vhr"],
        "bl": ["hhb", "bs", "vh"],
        "bs": ["hhb"],
        "ms": ["hh", "hhb"],
        "ls": ["vh"],
        "rs": ["vhr"],
        "dls": ["ld", "rd"],
        "drs": ["rud", "lud"],
        "mc": ["mr"]
    }

    @staticmethod
    def createJsonFromSymbolLists(symbols, name_info):
        result: str = "{Patterns:["

        for i in range(len(symbols)):
            symbol: list = symbols[i]
            result += "{Pattern:" + symbol[0] + ",Color:" + str(symbol[1]) + "}"

            if i != len(symbols) - 1:
                result += ","

        result += "]"

        if name_info != {}:
            result += ",CustomName:'{"

            for key in name_info.keys():
                result += f'"{key}":'

                if isinstance(name_info[key], str):
                    result += f'"{name_info[key]}"'
                else:
                    result += str(name_info[key])

                result += ","

            result = result[0:-1] + "}'"

        result += "}"

        return result

    @staticmethod
    def giveWarBanner():
        name_info: dict = {
            "text": "War banner",
            "color": "dark_red",
            "bold": True,
            "underlined": True
        }

        return Banner.createJsonFromSymbolLists(
            [["flo", 15], ["cr", 14], ["cs", 3], ["tt", 15], ["ts", 15], ["cbo", 14], ["tl", 14], ["tr", 14]],
            name_info
        )

    @staticmethod
    def generateBanner(village, alliance=None):
        name_info: dict = {
            "text": village.name + " banner",
            "color": "gold"
        }

        remaining: list = Banner.SYMBOLS.copy()

        symbols: list = []
        if alliance != None:
            symbols.append(alliance.banner_under_symbols)

        for layer in range(village.tier + 1):
            color: int = random.randint(0, 15)
            if color == Color.strToId(village.color):
                color = (color + 1) % 16

            symbol: str = remaining[random.randint(0, len(remaining) - 1)]

            symbols.append([symbol, color])

            if symbol in Banner.TO_BAN.keys():
                for to_remove in Banner.TO_BAN[symbol]:
                    if to_remove in remaining:
                        index = remaining.index(to_remove)
                        del remaining[index]

            del remaining[remaining.index(symbol)]

        if alliance != None:
            symbols.append(alliance.banner_over_symbols)

        return Banner.createJsonFromSymbolLists(symbols, name_info)
