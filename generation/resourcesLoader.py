from generation.structures.generated.generatedWell import GeneratedWell
from generation.structures.generated.generatedQuarry import *
from generation.resources import Resources


def loadAllResources(resources: Resources) -> None:
    print("Begin load resources")
    # Load structures
    ## Load houses
    resources.loadStructures("houses/haybale/haybalehouse1.nbt", "houses/haybale/haybalehouse1.json", "haybalehouse1")
    resources.loadStructures("houses/haybale/haybalehouse2.nbt", "houses/haybale/haybalehouse2.json", "haybalehouse2")
    resources.loadStructures("houses/haybale/haybalehouse3.nbt", "houses/haybale/haybalehouse3.json", "haybalehouse3")
    resources.loadStructures("houses/haybale/haybalehouse4.nbt", "houses/haybale/haybalehouse4.json", "haybalehouse4")

    resources.loadStructures("houses/basic/basichouse1.nbt", "houses/basic/basichouse1.json", "basichouse1")
    resources.loadStructures("houses/basic/basichouse2.nbt", "houses/basic/basichouse2.json", "basichouse2")
    resources.loadStructures("houses/basic/basichouse3.nbt", "houses/basic/basichouse3.json", "basichouse3")

    resources.loadStructures("houses/medium/mediumhouse1.nbt", "houses/medium/mediumhouse1.json", "mediumhouse1")
    resources.loadStructures("houses/medium/mediumhouse2.nbt", "houses/medium/mediumhouse2.json", "mediumhouse2")
    resources.loadStructures("houses/medium/mediumhouse3.nbt", "houses/medium/mediumhouse3.json", "mediumhouse3")

    resources.loadStructures("houses/advanced/advancedhouse1.nbt", "houses/advanced/advancedhouse1.json",
                             "advancedhouse1")
    resources.loadStructures("houses/advanced/advancedhouse2.nbt", "houses/advanced/advancedhouse2.json",
                             "advancedhouse2")
    resources.loadStructures("houses/advanced/advancedhouse3.nbt", "houses/advanced/advancedhouse3.json",
                             "advancedhouse3")

    ## Load work structures : functionals

    resources.addGeneratedStructures(GeneratedQuarry(), "functionals/quarry/basicgeneratedquarry.json",
                                     "basicgeneratedquarry")

    resources.loadStructures("functionals/lumberjackhut/basiclumberjackhut.nbt",
                             "functionals/lumberjackhut/basiclumberjackhut.json", "basiclumberjackhut")
    resources.loadStructures("functionals/lumberjackhut/mediumlumberjackhut.nbt",
                             "functionals/lumberjackhut/mediumlumberjackhut.json", "mediumlumberjackhut")
    resources.loadStructures("functionals/lumberjackhut/advancedlumberjackhut.nbt",
                             "functionals/lumberjackhut/advancedlumberjackhut.json", "advancedlumberjackhut")

    resources.loadStructures("functionals/stonecutter/basicstonecutter.nbt",
                             "functionals/stonecutter/basicstonecutter.json", "basicstonecutter")
    resources.loadStructures("functionals/stonecutter/mediumstonecutter.nbt",
                             "functionals/stonecutter/mediumstonecutter.json", "mediumstonecutter")
    resources.loadStructures("functionals/stonecutter/advancedstonecutter.nbt",
                             "functionals/stonecutter/advancedstonecutter.json", "advancedstonecutter")

    resources.loadStructures("functionals/farm/basicfarm.nbt", "functionals/farm/basicfarm.json", "basicfarm")
    resources.loadStructures("functionals/farm/mediumfarm1.nbt", "functionals/farm/mediumfarm1.json", "mediumfarm1")
    resources.loadStructures("functionals/farm/mediumfarm2.nbt", "functionals/farm/mediumfarm2.json", "mediumfarm2")
    resources.loadStructures("functionals/farm/advancedfarm.nbt", "functionals/farm/advancedfarm.json", "advancedfarm")

    resources.loadStructures("functionals/windmill/basicwindmill.nbt", "functionals/windmill/basicwindmill.json",
                             "basicwindmill")
    resources.loadStructures("functionals/windmill/mediumwindmill.nbt", "functionals/windmill/mediumwindmill.json",
                             "mediumwindmill")
    resources.loadStructures("functionals/windmill/advancedwindmill.nbt", "functionals/windmill/advancedwindmill.json",
                             "advancedwindmill")

    resources.loadStructures("functionals/furnace/basicfurnace1.nbt", "functionals/furnace/basicfurnace1.json",
                             "basicfurnace1")
    resources.loadStructures("functionals/furnace/mediumfurnace1.nbt", "functionals/furnace/mediumfurnace1.json",
                             "mediumfurnace1")
    resources.loadStructures("functionals/furnace/advancedfurnace1.nbt", "functionals/furnace/advancedfurnace1.json",
                             "advancedfurnace1")

    resources.loadStructures("functionals/smeltery/basicsmeltery.nbt", "functionals/smeltery/basicsmeltery.json",
                             "basicsmeltery")
    resources.loadStructures("functionals/smeltery/mediumsmeltery.nbt", "functionals/smeltery/mediumsmeltery.json",
                             "mediumsmeltery")
    resources.loadStructures("functionals/smeltery/advancedsmeltery.nbt", "functionals/smeltery/advancedsmeltery.json",
                             "advancedsmeltery")

    resources.loadStructures("functionals/workshop/basicworkshop.nbt", "functionals/workshop/basicworkshop.json",
                             "basicworkshop")
    resources.loadStructures("functionals/workshop/mediumworkshop.nbt", "functionals/workshop/mediumworkshop.json",
                             "mediumworkshop")
    resources.loadStructures("functionals/workshop/advancedworkshop.nbt", "functionals/workshop/advancedworkshop.json",
                             "advancedworkshop")

    resources.loadStructures("functionals/weaverhouse/basicweaverhouse.nbt",
                             "functionals/weaverhouse/basicweaverhouse.json", "basicweaverhouse")
    resources.loadStructures("functionals/weaverhouse/mediumweaverhouse.nbt",
                             "functionals/weaverhouse/mediumweaverhouse.json", "mediumweaverhouse")
    resources.loadStructures("functionals/weaverhouse/advancedweaverhouse.nbt",
                             "functionals/weaverhouse/advancedweaverhouse.json", "advancedweaverhouse")

    resources.loadStructures("functionals/shop/basicshop.nbt",
                             "functionals/shop/basicshop.json", "basicshop")
    resources.loadStructures("functionals/shop/mediumshop.nbt",
                             "functionals/shop/mediumshop.json", "mediumshop")
    resources.loadStructures("functionals/shop/advancedshop.nbt",
                             "functionals/shop/advancedshop.json", "advancedshop")

    resources.loadStructures("functionals/exchanger/basicexchanger.nbt",
                             "functionals/exchanger/basicexchanger.json", "basicexchanger")
    resources.loadStructures("functionals/exchanger/mediumexchanger.nbt",
                             "functionals/exchanger/mediumexchanger.json", "mediumexchanger")
    resources.loadStructures("functionals/exchanger/advancedexchanger.nbt",
                             "functionals/exchanger/advancedexchanger.json", "advancedexchanger")

    ## Load representatives structures for a village

    resources.loadStructures("representatives/townhall/basictownhall.nbt",
                             "representatives/townhall/basictownhall.json", "basictownhall")
    resources.loadStructures("representatives/townhall/mediumtownhall.nbt",
                             "representatives/townhall/mediumtownhall.json", "mediumtownhall")
    resources.loadStructures("representatives/townhall/mediumtownhall2.nbt",
                             "representatives/townhall/mediumtownhall.json", "mediumtownhall2")

    resources.loadStructures("representatives/townhall/advancedtownhall.nbt",
                             "representatives/townhall/advancedtownhall.json", "advancedtownhall")

    resources.loadStructures("representatives/jail/basicjail.nbt", "representatives/jail/basicjail.json", "basicjail")
    resources.loadStructures("representatives/jail/mediumjail.nbt", "representatives/jail/mediumjail.json", "mediumjail")
    resources.loadStructures("representatives/jail/advancedjail.nbt", "representatives/jail/advancedjail.json", "advancedjail")

    resources.loadStructures("representatives/graveyard/basicgraveyard.nbt",
                             "representatives/graveyard/basicgraveyard.json", "basicgraveyard")
    resources.loadStructures("representatives/graveyard/mediumgraveyard.nbt",
                             "representatives/graveyard/mediumgraveyard.json", "mediumgraveyard")
    resources.loadStructures("representatives/graveyard/advancedgraveyard.nbt",
                             "representatives/graveyard/advancedgraveyard.json", "advancedgraveyard")

    resources.loadStructures("representatives/tavern/basictavern.nbt", "representatives/tavern/basictavern.json",
                             "basictavern")
    resources.loadStructures("representatives/tavern/mediumtavern.nbt", "representatives/tavern/mediumtavern.json",
                             "mediumtavern")
    resources.loadStructures("representatives/tavern/advancedtavern.nbt", "representatives/tavern/advancedtavern.json",
                             "advancedtavern")

    resources.loadStructures("representatives/barrack/basicbarrack.nbt", "representatives/barrack/basicbarrack.json",
                             "basicbarrack")
    resources.loadStructures("representatives/barrack/mediumbarrack.nbt", "representatives/barrack/mediumbarrack.json",
                             "mediumbarrack")
    resources.loadStructures("representatives/barrack/advancedbarrack.nbt", "representatives/barrack/advancedbarrack.json",
                             "advancedbarrack")

    resources.loadStructures("representatives/adventurerhouse/adventurerhouse.nbt",
                             "representatives/adventurerhouse/adventurerhouse.json", "adventurerhouse")

    # HorseBox

    resources.loadStructures("representatives/horsebox/basichorseboxl.nbt",
                             "representatives/horsebox/horsebox.json", "basichorseboxl")

    resources.loadStructures("representatives/horsebox/basichorseboxh.nbt",
                             "representatives/horsebox/horsebox.json", "basichorseboxh")

    resources.loadStructures("representatives/horsebox/mediumhorseboxl.nbt",
                             "representatives/horsebox/horsebox.json", "mediumhorseboxl")

    resources.loadStructures("representatives/horsebox/mediumhorseboxh.nbt",
                             "representatives/horsebox/horsebox.json", "mediumhorseboxh")

    resources.loadStructures("representatives/horsebox/advancedhorseboxl.nbt",
                             "representatives/horsebox/horsebox.json", "advancedhorseboxl")

    resources.loadStructures("representatives/horsebox/advancedhorseboxh.nbt",
                             "representatives/horsebox/horsebox.json", "advancedhorseboxh")

    resources.addGeneratedStructures(GeneratedWell(), "representatives/well/basicgeneratedwell.json",
                                     "basicgeneratedwell")

    ## Load additional structures that won't be generated without special conditions : decorations

    resources.loadStructures("decorations/murderercache/murderercache.nbt",
                             "decorations/murderercache/murderercache.json", "murderercache")

    resources.loadStructures("decorations/murderercache/completemurderercache.nbt",
                             "decorations/murderercache/completemurderercache.json", "completemurderercache")

    resources.loadStructures("decorations/statue/basicstatue.nbt",
                             "decorations/statue/statue.json", "basicstatue")
    resources.loadStructures("decorations/statue/mediumstatue.nbt",
                             "decorations/statue/statue.json", "mediumstatue")
    resources.loadStructures("decorations/statue/advancedstatue.nbt",
                             "decorations/statue/statue.json", "advancedstatue")

    wall_types: list = ["line", "door", "externcorner", "innercorner", "externcornerstairs2", "innercornerstairs2", "stairs2",
                                                                       "externcornerstairs4", "innercornerstairs4", "stairs4",
                                                                       "externcornerstairs6", "innercornerstairs6", "stairs6",
                                                                       "externcornerstairs8", "innercornerstairs8", "stairs8"]

    for wall_type in wall_types:
        resources.loadStructures("wall/basic/basicwall" + wall_type + ".nbt", "wall/basicwall.json", "basicwall" + wall_type)
        resources.loadStructures("wall/medium/mediumwall" + wall_type + ".nbt", "wall/mediumwall.json", "mediumwall" + wall_type)
        resources.loadStructures("wall/advanced/advancedwall" + wall_type + ".nbt", "wall/advancedwall.json", "advancedwall" + wall_type)

    # Load lootTable
    resources.loadLootTable("emptyloottable.json", "empty")

    resources.loadLootTable("houses/kitchenhouse.json", "kitchenhouse")
    resources.loadLootTable("houses/bedroomhouse.json", "bedroomhouse")

    resources.loadLootTable("functionals/windmill.json", "windmill")
    resources.loadLootTable("functionals/basiclumberjackhut.json", "basiclumberjackhut")
    resources.loadLootTable("functionals/basicfarm.json", "basicfarm")
    resources.loadLootTable("functionals/basicstonecutter.json", "basicstonecutter")
    resources.loadLootTable("functionals/smeltery.json", "smeltery")
    resources.loadLootTable("functionals/workshop.json", "workshop")
    resources.loadLootTable("functionals/weaverhouse.json", "weaverhouse")

    resources.loadLootTable("functionals/shop.json", "shop")

    resources.loadLootTable("representatives/townhall.json", "townhall")
    resources.loadLootTable("representatives/jail.json", "jail")
    resources.loadLootTable("representatives/tavern.json", "tavern")
    resources.loadLootTable("representatives/barrack.json", "barrack")
    resources.loadLootTable("representatives/adventurerhouse.json", "adventurerhouse")
    resources.loadLootTable("representatives/exchanger.json", "exchanger")

    resources.loadLootTable("decorations/murderercache.json", "murderercache")

    print("Load partial nbt file")
    print("End load ressources")
