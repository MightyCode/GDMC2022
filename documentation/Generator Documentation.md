# General explanation

The main file which makes the generation working is *generateSettlement.py*.
The generator works in 5 steps, *generator.py* is mainly used.


. The script generateSettlement initializes data of the main dictionary **settlementData**.
. Then the script searches what should be the next structure using *structureManager.py* and finds its position with *floodFill.py*.
. After that, the scripts creates the lore of the village, likes main books describing the village or a register of villagers.
. The creation of lore finished, generateSettlement uses *road.py* to create roads.
. Finally, each structure is finally built and decorations are placed. 

The idea is to :
-> Find every information for the village.
-> Then build.


Note : 
1. Structure = big construction which takes more than 3 blocks long.
2. Decoration = little structure with 1 or 2 blocks long (ex : haybale block). It makes the village more lively.


# Description of each file.

## generation/*resources.py*

These resources class stores each loaded files. 
To make the system easier, instance of generated structure class is also store on the structures.


## generation/*resourcesLoader.py*

This utility class preload the instance of resource class with every structure and lootTable used for the generation.


## *testStructures.py*

This test file if the most useful file to test one structure
You just have to change in this line **structure = resources.structures["xxx"]** where xxx is the name of your structure


## *benchmarkTimeForBuilding.py*

This test file will construct a certain amount of same structure and show time took for construction.


## *generateSettlement.py*

This script run the main procedure and main steps to create the village. 
The script check at many location in the code or at each iteration of every loop the time, to decide if stop or continue.


## generation/*generator.py*

This script gathers functionalities that could be in *generateSettlement.py* but placed here for more readability.


## generation/*chestGeneration.py*

This class file objective is to generate a chest's content located at certain position. 
It uses look table, and additional object which are items that must be added to the chest independently of the loot table.


## generation/*lore_maker.py*

This class alter settlementData to add lore for each chosen structures.


## generation/*structureManager.py*

This class will fill settlementData with the next structure that should be added. 
The method to choose structure is a technological tree.
Image of the technological tree is on documentation folder.
Each structure group has a prerequisite to be available.
 
After that, each structure available has a weight depending on its type, or if the previous chosen structure was the same; then the random choose the next.


## generation/*floodFill.py*

This class recognize where ground block is, with the goal of giving positions where structures could be placed.

For each test to fit the structure at given position, the script rotates and flips the structure, checks corners and if the structure not overlaps another one.

When there are no placed structure. The script will take a random position. Do a flood fill of x block(s) around the position. Then try y times if the given structure is placeable. 
For each structure placed, the script will do a flood fill around its position.
When there are at least on placed structure. The script will take a random structure, take a random position in its floodfill and try z times if the given structure is placeable.

To place decorations, the script take the square surrounding all the structures placed and takes random positions. 


## generation/*road.py*

Generate roads between the structures that are placed according to their parent. The script use an A* to find the path.