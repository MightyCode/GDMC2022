Objectives for the futur


# Lore

## Specialization

Make a specialization for each village.

## War and alliance - trade

If two villages has the same specialization it lauch a war between the two village. Each village can be ally with another.


# Aspect 

-> Adding many structures to existing ones.

## Wall

Add a wall around the village.

## House

Add a special item or special decoration to the house of mayor.

## Tree

Remove tree when encouteer one on road or structions construction.

## Decoration

Change the decoration depending of biome or tier of advancement of the village.

## Path

Upgrade looking of path, alter path or lantern depending of biome, tier of advancement of the village, or tier of advancement of the targeted structure.



# System

## Dependencies into token

Currently the dependencies only accept static value, should be better to include variables.

If math needed on structure group dependencies conditions.

Make the system of conditions tokenable, the system parses conditions into type of token then does math on it.
Like **villagerNeeded** : **currentVillagerNumber > (10 + 1) * 2**
List of tokens should be **[variable, comparator, open parenthesis, number, operator, number, close parenthesis, operator, number]**
Then the system does math on it. 