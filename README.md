# GDMC2022
by Maxence Bazin and by Melvin Cledat, second builder.

This repository is the continuation of my [work last year with the tsukuba team done with Lucien Mocrete and Yusuf Senel](https://github.com/MightyCode/GDMC2021Tsukuba)

## How to run this project:
- Make sure to have the [http interface mod](https://github.com/nilsgawlik/gdmc_http_interface) installed;
- Open the minecraft world, and run the `setbuildarea x0 y0 z0 x1 y1 z1` command.
- Run the python script in this repository: `python generatesettlement.py'
## Requirements
- This project requires python3 
- Make sure to install the libraries listed in `requirements.txt`
## Alternative ways to run the project
There are several ways you can use to define a build are for this generator, depending on the parameters given to the generator:
-p, --player          build the settlement around the player's current location
-c x0 y0 z0 x1 y1 z1, --coordinates x0 y0 z0 x1 y1 z1
   build the settlement on the area defined by these coordinates</p>
-b, --buildarea       Build the settlement using a pre-existing buildArea (equivalent to not putting any argument
-a A, --radius A      Radius for building area, only meaningful with -p
-r [R], --remove [R]  Remove all structure if debug was activated, temp.txt if r specified, elsewhere file name: -r temp_0.txt

## Description of the Generator
This Minecraft Settlement Generator creates a coherent minecraft village. 
The main purpose is to create a better version of existing village. So the generator will not use or place
game breaking blocks or items.

The village you will encounter after the generation can be a basic, a medium or an advanced one. 
It will have relations with surrounded settlements, the relation will be from very close relation to war.
The war relation is very important because if your village has only one war relation, it will enter
the __war__ status.
Your village can be destroyed too. By many cause such as war or pillager raid.

In that village, there are unique interactions between villagers using diaries on their house.
There is a system of death, with a death book in the village and one the graveyard. 

One murderer/Spy often takes place in the village with war status, so be sure to look around for any clue.
The murderer will be happy on a destroyed village by the war. Its hiding place will get bigger. 

Each village has its own money system, which villagers use to sell items to the player. 
In addition, villages can be linked by trade pacts.
The material system is not fully used but is represents the power of the village for commercial purposes.

__A chest will be placed 20 blocks above the ground containing information about generated settlement(s)__
The position of all village will be indicated on the terminal too.
### What it does concretely
Based on the size of the area the player has set, the generator will decide if it will 
generate X village if the area is larger than 500 block.
For example:
- Zone of 450 X 450, the generator will generate one village in X and Z of size 450 X 450.
- Zone of 600 X 450, the generator will generate two village in X and one Z. Both of size of 300 X 450.
So the logical minimal size of a village is 256 by 256.

The lore of multiple village is created.

Then for each village :

The generator will decide the location of the first house of the first village. 
From that, it will then place houses at a random distance (but acceptable) 
from each other in connected area, discovering new chunks and adding materials to the village.
The wall will be created.

### Config: 
You can run checkOrCreateConfig script on util folder if you want to create the file before
any generation.
Or run a generation of a settlement will automatically create it.

There are two types of values. __Descriptive values__ which is values that are currently used by the
generator. __Overwhelming value__ which is a dictionary containing two field, does the generator used the
overwhelmed value : "state", what is the value: "value". Overwhelming values are used to fix changeable
values.

Here is an explanation of all fields:
- "maxVillageStructure" (number) defines the maximum number of main structure per village. Per default 55.
- "minVillageStructure" (number) defines the minimum number of main structure per village. Per default 25.
- "numberStructures" (_Overwhelming value_) set the number of main structure per village. 
- "saveConstructionInFile" (boolean) defines if the generator saved the modification to the world in a file. 
Notice that all generation will be very much slower with saveConstructionInFile activated. Per default false.
- "shouldShowWallSchematic" (boolean) defines if the generator should a schematic of the wall 
in a pyplot graph. Notice that the time continues to run on when the window is open, 
but the generation is blocked until the window is closed. Per default false
- "timeLimit" (number) set the time until the generator stop if it's not finished. Per default 720 (12 min.).
- "villageAge" (_Overwhelming value_) set the age of village (young : 0 | old : 1), modify the aspect of the village.
- "villageColor" (_Overwhelming value_) set the color liked by the village.
(white, orange, magenta, light_blue, yellow, lime, pink, gray, light_gray, cyan, purple, blue, brown, green), modify the aspect of the village.
- "villageDestroyed" (_Overwhelming value_) indicates if the village should be generated destroyed (true | false), modify the aspect of the village.
- "villageDestroyedCause" (_Overwhelming value_) indicates the cause of the destruction of the village (war | pillager), modify the aspect of the village.
- "villageName" (_Overwhelming value_) set the name of the village (what you want but < 19 characters)
- "villageRelationShip" (_Overwhelming value_) set the relationship with other village, change the lore.
(war : 0 | tension : 1 | neutral : 2 | friendship : 3 | close relation : 5 )
- "villageStatus" (_Overwhelming value_) set status of the village (war, peaceful), modify the aspect of the village.
- "villageTier" (_Overwhelming value_) set the tier of the village (basic : 0 | medium : 1 | advanced : 2)
- "villageWall" (_Overwhelming value_) set the shape of the village's war (convexHull | rectangular)


### Future of this program:
Now we have many placeholder structure. It could be cool to replace for example the generation of the 
town hall from a nbt file to a script, the system is already prepare to handle this. The well and 
the quarry are generated via a script.

###Contact Information

If you want to contact us for any question, you can do so via discord :

Tamalou-Max#0432
