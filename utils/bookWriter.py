import copy
import math

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
    TEXT_BOLD = "bold"

    NUMBER_LINE: int = 14
    NUMBER_CHAR_LINE: int = 19
    NUMBER_CHAR_PAGE: int = NUMBER_LINE * NUMBER_CHAR_LINE

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
            self.TEXT_BOLD: False
        }

        self.color: str = BookWriter.COLOR_BLACK
        self.texts: list = []

        self.text_created: bool = False

        self.count_char: int = 0

        self.newText()

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

    def computeLineSize(self, message):
        parts = message.split("\\\\n")

        size: int = 0

        if len(parts) > 1:
            for part in parts[:-1]:
                size += math.ceil(len(part) / BookWriter.NUMBER_CHAR_LINE) * BookWriter.NUMBER_CHAR_LINE

        size += len(parts[-1])

        return size

    def cutInFrom(self, message, position):
        parts = message.split("\\\\n")

        size: int = 0
        char_position: int = 0

        if len(parts) > 1:
            for part in parts[:-1]:
                size += math.ceil(len(part) / BookWriter.NUMBER_CHAR_LINE) * BookWriter.NUMBER_CHAR_LINE
                char_position += len(part) + 1

                if size >= position:
                    return [message[0: position], message[position:]]

        return [message[0: position], message[position:]]

    def writeLine(self, message: str, breakLine: bool = True):
        message += (" \\\\n" if breakLine else "")
        message_len = self.computeLineSize(message)
        print(message, self.count_char, message_len, message_len + self.count_char, BookWriter.NUMBER_CHAR_PAGE)

        if self.count_char + message_len <= BookWriter.NUMBER_CHAR_PAGE:
            self.texts[-1]["text"] += message
            self.count_char += message_len
        else:
            first, second = self.cutInFrom(message, BookWriter.NUMBER_CHAR_PAGE - self.count_char)
            print("decompoze", first, second)

            """if BookWriter.NUMBER_CHAR_PAGE != self.count_char:"""
            self.texts[-1]["text"] += first

            old_size: int = self.count_char
            self.breakPage()

            self.texts[-1]["text"] += second
            self.count_char += (old_size + message_len) - BookWriter.NUMBER_CHAR_PAGE

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

        self.count_char = 0
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
        self.textMode[BookWriter.TEXT_BOLD] = False

        self.texts[-1]["form"][BookWriter.TEXT_OBFUSCATED] = False
        self.texts[-1]["form"][BookWriter.TEXT_STRIKETHROUGH] = False
        self.texts[-1]["form"][BookWriter.TEXT_UNDERLINE] = False
        self.texts[-1]["form"][BookWriter.TEXT_ITALIC] = False
        self.texts[-1]["form"][BookWriter.TEXT_BOLD] = False

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
