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
### Debug mode: 
To activate the debug mode and save world modification, you need to set debugMode as True
in the config/config.json file.
You can run checkOrCreateConfig file if you want to create the file before any generation.
Notice that all generation will be very much slower with debugMode activated.
## Description of the Generator
This Minecraft Settlement Generator is generating a coherent minecraft village. 
The village will be of basic, medium or advanced village.
But more, the village is connected to surrounded villages, the relation will be from 
very close relation to war.
The war relation is very important because if a village has only one war relation, it will enter
the __war__ status.
A village can be destroyed too. By many cause such as war or pillager raid.

In that village, there are unique interactions between villagers using diaries on their house.
There is a system of death, with a death book in the village and one the graveyard. 

One murderer often takes place in the village in a war status, so be sure to look around for any clue.
### What it does concretely
Based on the size of the area the player has set, the generator will decide if it will 
generate X village if the area is larger than 500 block.
For example:
- Zone of 450 X 450, the generator will generate one village in X and Z of size 450 X 450.
- Zone of 600 X 450, the generator will generate two village in X and one Z. Both of size of 300 X 450.
So the logical minimal size of a village is 256 by 256.

Then it will decide on the location of the first house of the first village. 
From that, it will then place houses at a random distance (but acceptable) 
from each other in connected area, discovering new chunks and adding materials to the village.
The material system is not fully used but is represents the power of the village for commercial purposes.
### Future of this program:
Now we have many placeholder structure. It could be cool to replace for example the generation of the 
town hall from a nbt file to a script, the system is already prepare to handle this. The well and 
the quarry are generated via a script.

###Contact Information

If you want to contact us for any question, you can do so via discord :

Tamalou-Max#0432
