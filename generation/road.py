from generation.data.settlementData import SettlementData
from generation.floodFill import FloodFill
import utils.projectMath as projectMath
import lib.interfaceUtils as iu
from utils.worldModification import WorldModification

NODE_IN_ROAD:tuple = []
POSITION_OF_LANTERN:tuple = []


class Node:
	def __init__(self, point:tuple):
		self.point:tuple = point
		self.parent:Node = None
		self.cost:int = 0
		self.H:int  = 0

	def move_cost(self, other):
		return 1


class logNode:
	def __init__(self, point:tuple):
		self.point:tuple = point
		self.child = None


def manhattan(point:Node, point2:Node) -> int:
	return abs(point2.point[0] - point.point[0]) + abs(point2.point[1] - point.point[1])


def manhattanForCoord(point:tuple, point2:tuple):
	return abs(point2[0] - point[0]) + abs(point2[1] - point[1])


def children(point) -> tuple:
	x, z = point.point
	links:tuple = []
	for d in [(x - 1, z), (x, z - 1), (x, z + 1), (x + 1,z)]:
		links.append(Node([d[0], d[1]]))

	return links


def compareNode(node1:Node, node2:Node) -> int:
	if node1.H < node2.H:
		return 1
	elif node1.H == node2.H:
		return 0
	else:
		return -1


def isInClosedList(node:Node, closedlist:tuple) -> bool:
	for i in closedlist:
		if node.point == i.point:
			return True

	return False


def isInListWithInferiorCost(node:Node, list:tuple) -> bool:
	for i in list:
		if node.point == i.point:
			if i.H < node.H:

				return True
	return False


def isInRoad(coord:tuple) -> bool:
	for index in NODE_IN_ROAD:
		if coord in index:
			return True

	return False


def isInLantern(coord):
	for index in POSITION_OF_LANTERN:
		if coord in index:
			return True
	return False


def findClosestNodeInRoad(coordstart, coordgoal):
	closestdistance = manhattanForCoord(coordstart, coordgoal)
	coordclosestdistance = coordgoal
	for index in NODE_IN_ROAD:
		for node in index:
			temp = manhattanForCoord(coordstart,node)
			if temp < closestdistance:
				closestdistance = temp
				coordclosestdistance = node
	#print(closestdistance)
	return coordclosestdistance


def astar(startcoord, goalcoord, squarelist):
	#the open and close set
	start = Node(startcoord)
	goal = Node(goalcoord)
	openlist = []
	closedlist = []
	#current point at start is the starting point
	current = start
	current.H = manhattan(current, goal)
	#add it to the openset
	openlist.append(current)

	while openlist:
		#find the item in the open set with the lowest G+H score
		temp = openlist[0].H
		for i in openlist:
			if i.H <= temp:
				temp = i.H
				current = i
		openlist.remove(current)
		# If we are at the goal
		if current.point == goal.point:
			path = [current.point]
			while current.parent:
				path.append(current.parent.point)
				current = current.parent
			NODE_IN_ROAD.append(path)

			return path[::-1] # To reverse the path
		# For every neighbourg of current node
		
		for node in children(current):
			#test here if the children is in a house
			#print(node.point)
			if node.point == goalcoord:
				#print("TROUVE")
				openlist.append(node)
			notinsquare = True
			for squarehouse in squarelist:
				if projectMath.isPointInSquare(node.point, squarehouse):
					notinsquare = False
			#if abs(floodFill.getHeight(node.point[0],node.point[1],ws) - floodFill.getHeight(current.point[0],current.point[1],ws)) > 2:
			#	notinsquare = False

			if notinsquare:
				if not(isInClosedList(node, closedlist)) and not(isInListWithInferiorCost(node, openlist)):
					node.cost = current.cost + 1
					node.H = node.cost + manhattan(node,goal)
					node.parent = current
					openlist.append(node)
		closedlist.append(current)
	raise ValueError('No Path Found')


def computeXEntry(xLocalPosition:int, cornerProjection, facingStruct, cornerStruct):
	x:int = xLocalPosition
	x += cornerProjection[facingStruct][0] * cornerStruct[0]
	x += cornerProjection[facingStruct][2] * cornerStruct[2]
	x += -cornerProjection[facingStruct][0] + cornerProjection[facingStruct][2]

	return x


def computeZEntry(zLocalPosition:int, cornerProjection, facingStruct, cornerStruct):
	z:int = zLocalPosition
	z += cornerProjection[facingStruct][1] * cornerStruct[1]
	z += cornerProjection[facingStruct][3] * cornerStruct[3]
	z += -cornerProjection[facingStruct][1] + cornerProjection[facingStruct][3]

	return z


def initRoad(floodFill:FloodFill, settlementData:SettlementData, worldModif:WorldModification):
	NODE_IN_ROAD.clear()
	POSITION_OF_LANTERN.clear()

	cornerProjection:dict = { 
		"north" : [ 0, 1, 0, 0], 
		"south" : [ 0, 0, 0, 1 ], 
		"west" : [ 1, 0, 0, 0 ], 
		"east" : [ 0, 0, 1, 0 ] 
	}
	
	squarelist:list = []

	for index in range(0, len(settlementData.structures)):
		entrytemp:tuple = []
		entrytemp.append(floodFill.listHouse[index][0])
		entrytemp.append(floodFill.listHouse[index][1])
		entrytemp.append(floodFill.listHouse[index][2])

		squarelist.append([entrytemp[0] + floodFill.listHouse[index][3][0] , entrytemp[2] + floodFill.listHouse[index][3][1], 
			entrytemp[0] + floodFill.listHouse[index][3][2], entrytemp[2] + floodFill.listHouse[index][3][3]])


	#print(squarelist)
	for indexFrom in range(0, len(settlementData.structures)):
		# To know if the house doesn't have parent...
		start:tuple = [0, 0]
		goal:tuple = [0, 0]
		
		indexTo:int = floodFill.listHouse[indexFrom][5]
		if indexTo == -1:
			continue
		
		# House From
		facingStructFrom = settlementData.structures[indexFrom]["prebuildingInfo"]["entry"]["facing"]
		cornerStructFrom = settlementData.structures[indexFrom]["prebuildingInfo"]["corner"]
		entryStructFrom = [floodFill.listHouse[indexFrom][0], floodFill.listHouse[indexFrom][1], floodFill.listHouse[indexFrom][2]]

		x = computeXEntry(entryStructFrom[0], cornerProjection, facingStructFrom, cornerStructFrom)
		y = entryStructFrom[1]
		z = computeZEntry(entryStructFrom[2], cornerProjection, facingStructFrom, cornerStructFrom)
		
		while not(floodFill.is_air(x, y + 2, z)) or floodFill.is_air(x, y + 1, z):
			if floodFill.is_air(x, y + 1, z):
				y -=1

			if not(floodFill.is_air(x, y + 2, z)):
				y += 1
		start = [x, z]

		# House to
		facingStructTo = settlementData.structures[indexTo]["prebuildingInfo"]["entry"]["facing"]
		cornerStructTo = settlementData.structures[indexTo]["prebuildingInfo"]["corner"]

		entryStructTo = [floodFill.listHouse[indexTo][0], floodFill.listHouse[indexTo][1] - 1, floodFill.listHouse[indexTo][2]]

		x = computeXEntry(entryStructTo[0], cornerProjection, facingStructTo, cornerStructTo)
		y = entryStructTo[1]
		z = computeZEntry(entryStructTo[2], cornerProjection, facingStructTo, cornerStructTo)
	
		goal = [x, z]
		goal = findClosestNodeInRoad(start, goal)

		while not(floodFill.is_air(x, y + 2, z)) or floodFill.is_air(x, y + 1, z):
			if floodFill.is_air(x, y + 1, z):
				y -=1
			if not(floodFill.is_air(x, y + 2, z)):
				y += 1
				#print("stuck1")

		try:
			generateRoad(worldModif, floodFill, start, goal, squarelist, settlementData, entryStructFrom)		
		except ValueError:
			print("ValueError, path can't be implemented there")

"""
Generating the path among 2 houses
"""
def generateRoad(worldModif, floodFill, start, goal, squarelist, settlementData, entryStructFrom):

	path = astar(start, goal, squarelist)
	temp = 1

	yTemp =  entryStructFrom[1]
	for block in path:
		y = yTemp
		material = 'minecraft:grass_path'
		while not(floodFill.is_air(block[0], y + 1, block[1])) or floodFill.is_air(block[0], y, block[1]):
			if floodFill.is_air(block[0], y, block[1]):
				y -=1
			if not(floodFill.is_air(block[0], y + 1, block[1])):
				y += 1

		while iu.getBlock(block[0], y, block[1]) == 'minecraft:water':
			y = y + 1
			material = "minecraft:" + settlementData.getMatRep("woodType") + "_planks"
		while iu.getBlock(block[0], y, block[1]) == 'minecraft:lava':
			y = y + 1
			material = "minecraft:nether_bricks"

		# Here, we need to check if there is a tree above the path, and if yes, we want to remove it 
		worldModif.setBlock(block[0], y, block[1], "minecraft:air")
		worldModif.setBlock(block[0], y + 1, block[1], "minecraft:air")
		worldModif.setBlock(block[0], y + 2, block[1], "minecraft:air")
		worldModif.setBlock(block[0], y - 1, block[1], material)
		yTemp = y

	yTemp = entryStructFrom[1]
	for block in path:
		y = yTemp
		while not(floodFill.is_air(block[0], y + 1, block[1])) or floodFill.is_air(block[0], y, block[1]):
			if floodFill.is_air(block[0], y, block[1]):
				y -=1
				
			if not(floodFill.is_air(block[0], y + 1, block[1])):
				y += 1

		while iu.getBlock(block[0], y, block[1]) == 'minecraft:water' or iu.getBlock(block[0], y, block[1]) == 'minecraft:lava':
			y = y + 1

		if temp % 12 == 0 and temp < len(path) - 3:
			diffX = [-1, 0, 1, 0]
			diffZ = [0, -1, 0, 1]

			for i in [0, 1, 2, 3]:
				position = [block[0] + diffX[i], block[1] + diffZ[i]]
				if not position in path and not floodFill.isInHouse(position) and not isInRoad(position):
					POSITION_OF_LANTERN.append([block[0], block[1]])
					worldModif.setBlock(position[0], y - 1, position[1], 'minecraft:cobblestone')
					worldModif.setBlock(position[0], y, 	position[1], 'minecraft:cobblestone_wall')
					worldModif.setBlock(position[0], y + 1, position[1], 'minecraft:torch')
					break
			
		temp += 1
		yTemp = y
