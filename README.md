# GDMC2021
by Tsukuba Team
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
To activate the debug mode and save world modification, you need to set debugMode as True in the config/config.json file
notice that it will be very much slower with debugMode.
## Description of the Generator
This Minecraft Settlement Generator is generating a coherent minecraft village. In that village, there are unique interaction between villagers using books in their house. There is a system of death, with a death record in the village and a cemetery. Murders often takes place in the village, so be sure to look around for any clue.
### What it does concretely
Based on the size of the area the player has set, the program will decide if it will try to generate X village within there is Y Houses if the area is larger than 500 block. Then it will decide on the location of the first house of the first village. From that, it will then place houses at a random distance (but acceptable) from each other in connected area, discovering new chunk after an other and adding materials unlocked thanks to that. When the program decide to place a new house, it will look at houses already built and ressources available to then decide which house will be built.
### Future of this program:
We want to work on interaction between villages, implement new houses, make more uniqueness villages based on more detailed ressources and use the interaction between villages to upgrade each villages "together" (or not if they are ennemies).
###Contact Information

If you want to contact us for any question, you can do so via discord :

Izzypizi#7987

Tamalou-Max#0432

Harckyl#0032
