from generation.structures.generated.generatedWell import GeneratedWell
from generation.structures.generated.generatedQuarry import * 
from generation.resources import Resources

def loadAllResources(resources:Resources) : 
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

    resources.loadStructures("houses/advanced/advancedhouse1.nbt", "houses/advanced/advancedhouse1.json", "advancedhouse1")

    ## Load work structures : functionnals

    resources.addGeneratedStructures(GeneratedQuarry(), "functionals/quarry/basicgeneratedquarry.json", "basicgeneratedquarry")

    resources.loadStructures("functionals/lumberjachut/basiclumberjachut.nbt", "functionals/lumberjachut/basiclumberjachut.json", "basiclumberjachut")

    resources.loadStructures("functionals/stonecutter/basicstonecutter.nbt", "functionals/stonecutter/basicstonecutter.json", "basicstonecutter")
    
    resources.loadStructures("functionals/farm/basicfarm.nbt", "functionals/farm/basicfarm.json", "basicfarm")

    resources.loadStructures("functionals/farm/mediumfarm1.nbt", "functionals/farm/mediumfarm1.json", "mediumfarm1")

    resources.loadStructures("functionals/windmill/basicwindmill.nbt", "functionals/windmill/basicwindmill.json", "basicwindmill")
    resources.loadStructures("functionals/windmill/mediumwindmill.nbt", "functionals/windmill/mediumwindmill.json", "mediumwindmill")

    resources.loadStructures("functionals/furnace/basicfurnace1.nbt", "functionals/furnace/basicfurnace1.json", "basicfurnace1")

    resources.loadStructures("functionals/smeltery/basicsmeltery.nbt", "functionals/smeltery/basicsmeltery.json", "basicsmeltery")

    resources.loadStructures("functionals/workshop/basicworkshop.nbt", "functionals/workshop/basicworkshop.json", "basicworkshop")

    resources.loadStructures("functionals/weaverhouse/basicweaverhouse.nbt", "functionals/weaverhouse/basicweaverhouse.json", "basicweaverhouse")

    ## Load representatives structures for a village

    resources.loadStructures("representatives/townhall/basictownhall.nbt", "representatives/townhall/basictownhall.json", "basictownhall")

    resources.loadStructures("representatives/jail/basicjail.nbt", "representatives/jail/basicjail.json", "basicjail")
    resources.loadStructures("representatives/graveyard/basicgraveyard.nbt", "representatives/graveyard/basicgraveyard.json", "basicgraveyard")

    resources.loadStructures("representatives/tavern/basictavern.nbt", "representatives/tavern/basictavern.json", "basictavern")
    resources.loadStructures("representatives/barrack/basicbarrack.nbt", "representatives/barrack/basicbarrack.json", "basicbarrack")

    resources.loadStructures("representatives/adventurerhouse/adventurerhouse.nbt", "representatives/adventurerhouse/adventurerhouse.json", "adventurerhouse")

    resources.addGeneratedStructures(GeneratedWell(), "representatives/well/basicgeneratedwell.json", "basicgeneratedwell")

    ## Load additionnal structures that won't be generated : decorations

    resources.loadStructures("decorations/murderercache.nbt", "decorations/murderercache.json", "murderercache")

    # Load lootTable
    resources.loadLootTable("houses/kitchenhouse.json", "kitchenhouse")
    resources.loadLootTable("houses/bedroomhouse.json", "bedroomhouse")

    resources.loadLootTable("functionals/windmill.json", "windmill")
    resources.loadLootTable("functionals/basiclumberjachut.json", "basiclumberjachut")
    resources.loadLootTable("functionals/basicfarm.json", "basicfarm")
    resources.loadLootTable("functionals/basicstonecutter.json", "basicstonecutter")
    resources.loadLootTable("functionals/smeltery.json", "smeltery")
    resources.loadLootTable("functionals/workshop.json", "workshop")

    resources.loadLootTable("representatives/townhall.json", "townhall")
    resources.loadLootTable("representatives/jail.json", "jail")
    resources.loadLootTable("representatives/tavern.json", "tavern")
    resources.loadLootTable("representatives/barrack.json", "barrack")
    resources.loadLootTable("representatives/adventurerhouse.json", "adventurerhouse")

    resources.loadLootTable("decorations/murderercache.json", "murderercache")

    print("End load ressources")