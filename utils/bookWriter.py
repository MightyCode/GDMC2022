import copy


class BookWriter:
    COLOR_BLUE = "blue"
    COLOR_DARK_BLUE = "dark_blue"
    COLOR_GREEN = "green"
    COLOR_DARK_GREEN = "dark_green"
    COLOR_AQUA = "aqua"
    COLOR_DARK_AQUA = "dark_aqua"
    COLOR_RED = "red"
    COLOR_DARK_RED = "dark_red"
    COLOR_PURPLE = "purple"
    COLOR_DARK_PURPLE = "dark_purple"
    COLOR_LIGHT_PURPLE = "light_purple"
    COLOR_GREY = "grey"
    COLOR_DARK_GREY = "dark_dark_grey"
    COLOR_BLACK = "black"
    COLOR_GOLD = "gold"
    COLOR_YELLOW = "yellow"
    COLOR_WHITE = "white"

    TEXT_OBFUSCATED = "obfuscated"
    TEXT_STRIKETHROUGH = "strikethrough"
    TEXT_UNDERLINE = "underlined"
    TEXT_ITALIC = "italic"

    def __init__(self):
        self.title: str = ""
        self.author: str = ""

        self.description = None
        self.descriptionColor: str = BookWriter.COLOR_GOLD

        self.textMode: dict = {
            self.TEXT_OBFUSCATED: False,
            self.TEXT_STRIKETHROUGH: False,
            self.TEXT_UNDERLINE: False,
            self.TEXT_ITALIC: False,
        }

        self.color: str = BookWriter.COLOR_BLACK
        self.texts: list = []

        self.text_created: bool = False

    def setInfo(self, title, author, description=None, description_color='gold'):
        self.title = title
        self.author = author
        self.description = description
        self.descriptionColor = description_color

    def printBook(self) -> str:
        result: str = '{title:\"' + self.title + '\", author: \"' + self.author + '\"'

        if self.description is not None:
            result += ', display:{Lore:[\'[{\"text\":\"' \
                      + self.description + '\",\"color\":\"' + self.descriptionColor + '\"}]\']}'

        result += ', pages:[\'['

        page = 0
        for text in self.texts:
            if text["newPage"] and page != 0:
                result = result[:-1] + ']\',\'['

            result += '{\"text\":\"' + text["text"] + "\", \"color\":\"" + text["color"] + "\""

            for key in text["form"].keys():
                if text["form"][key]:
                    result += ', \"' + key + '\" : \"true\"'

            result += '},'

            page += 1

        result = result[:-1] + ']\']}'

        return result

    def writeLine(self, message: str, breakLine: bool = True):
        self.texts[-1]["text"] += message + ("\\\\n" if breakLine else "")
        self.text_created = False

    def writeEmptyLine(self, number: int):
        for i in range(number):
            self.writeLine("")

    def writeSameSymbol(self, char: chr, number=1):
        self.writeLine(char * number)

    def fillLineWith(self, char: chr):
        self.writeSameSymbol(char, 19)

    def writeFirstPage(self, message: str, title: str):
        self.breakPage()
        self.resetFormat()

        self.fillLineWith("-")

        self.writeEmptyLine(2)
        self.writeLine(message)
        self.writeEmptyLine(1)
        self.writeLine(title)
        self.writeEmptyLine(4)
        self.fillLineWith("-")
        self.breakPage()

    def breakPage(self):
        self.newText()
        new = self.texts[-1]
        new["newPage"] = True

    def newText(self):
        if self.text_created:
            return

        new: dict = self.createInfoForText()
        self.texts.append(new)

        self.text_created = True

    def setTextMode(self, textMode: str, value: bool):
        self.newText()
        self.textMode[textMode] = value
        self.texts[-1]["form"][textMode] = value

    def resetTextMode(self):
        self.newText()
        self.textMode[BookWriter.TEXT_OBFUSCATED] = False
        self.textMode[BookWriter.TEXT_STRIKETHROUGH] = False
        self.textMode[BookWriter.TEXT_UNDERLINE] = False
        self.textMode[BookWriter.TEXT_ITALIC] = False

        self.texts[-1]["form"][BookWriter.TEXT_OBFUSCATED] = False
        self.texts[-1]["form"][BookWriter.TEXT_STRIKETHROUGH] = False
        self.texts[-1]["form"][BookWriter.TEXT_UNDERLINE] = False
        self.texts[-1]["form"][BookWriter.TEXT_ITALIC] = False

    def setColor(self, color: str):
        self.newText()
        self.color = color
        self.texts[-1]["color"] = color

    def resetFormat(self):
        self.newText()
        self.setColor(self.COLOR_BLACK)
        self.resetTextMode()

    def createInfoForText(self) -> dict:
        return {
            "newPage": False,
            "text": "",
            "color": self.color,
            "form": copy.deepcopy(self.textMode)
        }
