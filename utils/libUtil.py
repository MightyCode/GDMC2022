import lib.interface as interface


# ------------ caranha functions

def makeBuildArea(width=128, height=128):
    interface.runCommand(
        "execute at @p run setbuildarea ~{} 0 ~{} ~{} 256 ~{}".format(int(-1 * width / 2), int(-1 * height / 2),
                                                                      int(width / 2), int(height / 2)))
    build_area = interface.requestBuildArea()
    x1 = build_area["xFrom"]
    z1 = build_area["zFrom"]
    x2 = build_area["xTo"]
    z2 = build_area["zTo"]
    return x1, z1, x2 - x1, z2 - z1


def setSignText(x, y, z, line1="", line2="", line3="", line4=""):
    l1 = 'Text1:\'{"text":"' + line1 + '"}\''
    l2 = 'Text2:\'{"text":"' + line2 + '"}\''
    l3 = 'Text3:\'{"text":"' + line3 + '"}\''
    l4 = 'Text4:\'{"text":"' + line4 + '"}\''
    block_nbt = "{" + l1 + "," + l2 + "," + l3 + "," + l4 + "}"
    return interface.runCommand("data merge block {} {} {} ".format(x, y, z) + block_nbt)


def addItemChest(x, y, z, items, places=None):
    if places is None:
        places = []

    if len(places) == 0:
        places = list(range(len(items)))

    for identifier, v in enumerate(items):
        identifier = places[identifier]
        command = "replaceitem block {} {} {} {} {} {}".format(x, y, z,
                                                               "container." + str(identifier),
                                                               v[0],
                                                               v[1])
        interface.runCommand(command)
