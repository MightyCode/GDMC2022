from generation.structures.generated.generatedWell import GeneratedWell
from generation.structures.generated.generatedQuarry import *
from generation.resources import Resources


def loadAllResources(resources: Resources) -> None:
    print("Begin load ressources")
    # Loads structures
    ## Load houses
    resources.loadStructures("houses/haybale/haybalehouse1.nbt", "houses/haybale/haybalehouse1.json", "haybalehouse1")
    resources.loadStructures("houses/haybale/haybalehouse2.nbt", "houses/haybale/haybalehouse2.json", "haybalehouse2")
    resources.loadStructures("houses/haybale/haybalehouse3.nbt", "houses/haybale/haybalehouse3.json", "haybalehouse3")
    resources.loadStructures("houses/haybale/haybalehouse4.nbt", "houses/haybale/haybalehouse4.json", "haybalehouse4")

    resources.loadStructures("houses/basic/basichouse1.nbt", "houses/basic/basichouse1.json", "basichouse1")
    resources.loadStructures("houses/basic/basichouse2.nbt", "houses/basic/basichouse2.json", "basichouse2")
    resources.loadStructures("houses/basic/basichouse3.nbt", "houses/basic/basichouse3.json", "basichouse3")

    resources.loadStructures("houses/medium/mediumhouse1.nbt", "houses/medium/mediumhouse1.json", "mediumhouse1")
    resources.loadStructures("houses/medium/mediumhouse2.nbt", "houses/medium/mediumhouse1.json", "mediumhouse2")
    resources.loadStructures("houses/medium/mediumhouse3.nbt", "houses/medium/mediumhouse3.json", "mediumhouse3")

    resources.loadStructures("houses/advanced/advancedhouse1.nbt", "houses/advanced/advancedhouse1.json",
                             "advancedhouse1")

    ## Load work structures : functionnals

    resources.addGeneratedStructures(GeneratedQuarry(), "functionals/quarry/basicgeneratedquarry.json",
                                     "basicgeneratedquarry")

    resources.loadStructures("functionals/lumberjackhut/basiclumberjackhut.nbt",
                             "functionals/lumberjackhut/basiclumberjackhut.json", "basiclumberjackhut")

    resources.loadStructures("functionals/lumberjackhut/mediumlumberjackhut.nbt",
                             "functionals/lumberjackhut/mediumlumberjackhut.json", "mediumlumberjackhut")

    resources.loadStructures("functionals/stonecutter/basicstonecutter.nbt",
                             "functionals/stonecutter/basicstonecutter.json", "basicstonecutter")

    resources.loadStructures("functionals/farm/basicfarm.nbt", "functionals/farm/basicfarm.json", "basicfarm")

    resources.loadStructures("functionals/farm/mediumfarm1.nbt", "functionals/farm/mediumfarm1.json", "mediumfarm1")

    resources.loadStructures("functionals/windmill/basicwindmill.nbt", "functionals/windmill/basicwindmill.json",
                             "basicwindmill")
    resources.loadStructures("functionals/windmill/mediumwindmill.nbt", "functionals/windmill/mediumwindmill.json",
                             "mediumwindmill")

    resources.loadStructures("functionals/furnace/basicfurnace1.nbt", "functionals/furnace/basicfurnace1.json",
                             "basicfurnace1")

    resources.loadStructures("functionals/furnace/mediumfurnace1.nbt", "functionals/furnace/mediumfurnace1.json",
                             "mediumfurnace1")

    resources.loadStructures("functionals/furnace/advancedfurnace1.nbt", "functionals/furnace/advancedfurnace1.json",
                             "advancedfurnace1")

    resources.loadStructures("functionals/smeltery/basicsmeltery.nbt", "functionals/smeltery/basicsmeltery.json",
                             "basicsmeltery")

    resources.loadStructures("functionals/workshop/basicworkshop.nbt", "functionals/workshop/basicworkshop.json",
                             "basicworkshop")

    resources.loadStructures("functionals/weaverhouse/basicweaverhouse.nbt",
                             "functionals/weaverhouse/basicweaverhouse.json", "basicweaverhouse")

    resources.loadStructures("functionals/shop/basicshop.nbt",
                             "functionals/shop/basicshop.json", "basicshop")

    resources.loadStructures("functionals/shop/mediumshop.nbt",
                             "functionals/shop/mediumshop.json", "mediumshop")

    resources.loadStructures("functionals/exchanger/basicexchanger.nbt",
                             "functionals/exchanger/basicexchanger.json", "basicexchanger")

    resources.loadStructures("functionals/exchanger/mediumexchanger.nbt",
                             "functionals/exchanger/mediumexchanger.json", "mediumexchanger")

    ## Load representatives structures for a village

    resources.loadStructures("representatives/townhall/basictownhall.nbt",
                             "representatives/townhall/basictownhall.json", "basictownhall")

    resources.loadStructures("representatives/jail/basicjail.nbt", "representatives/jail/basicjail.json", "basicjail")
    resources.loadStructures("representatives/graveyard/basicgraveyard.nbt",
                             "representatives/graveyard/basicgraveyard.json", "basicgraveyard")

    resources.loadStructures("representatives/tavern/basictavern.nbt", "representatives/tavern/basictavern.json",
                             "basictavern")

    resources.loadStructures("representatives/barrack/basicbarrack.nbt", "representatives/barrack/basicbarrack.json",
                             "basicbarrack")

    resources.loadStructures("representatives/barrack/mediumbarrack.nbt", "representatives/barrack/mediumbarrack.json",
                             "mediumbarrack")

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

    resources.loadStructures("decorations/statue/mediumstatue.nbt",
                             "decorations/statue/mediumstatue.json", "mediumstatue")

    # Load lootTable
    resources.loadLootTable("houses/kitchenhouse.json", "kitchenhouse")
    resources.loadLootTable("houses/bedroomhouse.json", "bedroomhouse")

    resources.loadLootTable("functionals/windmill.json", "windmill")
    resources.loadLootTable("functionals/basiclumberjackhut.json", "basiclumberjackhut")
    resources.loadLootTable("functionals/basicfarm.json", "basicfarm")
    resources.loadLootTable("functionals/basicstonecutter.json", "basicstonecutter")
    resources.loadLootTable("functionals/smeltery.json", "smeltery")
    resources.loadLootTable("functionals/workshop.json", "workshop")

    resources.loadLootTable("functionals/shop.json", "shop")

    resources.loadLootTable("representatives/townhall.json", "townhall")
    resources.loadLootTable("representatives/jail.json", "jail")
    resources.loadLootTable("representatives/tavern.json", "tavern")
    resources.loadLootTable("representatives/barrack.json", "barrack")
    resources.loadLootTable("representatives/adventurerhouse.json", "adventurerhouse")
    resources.loadLootTable("representatives/exchanger.json", "exchanger")

    resources.loadLootTable("decorations/murderercache.json", "murderercache")

    print("End load ressources")
