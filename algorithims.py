from graph import *
import time

def find_largest_army(player, current_largest, player_list):

	'''
	simple alogrithim to find the largest_army
	takes in the index of current player that holds largest army 
	and index of player whos turn just ended as well as the
	player list dictionary. Calculates largest army and allocates
	victory points appropriately

	'''
	# case for when someone holds largest army
	if current_largest != None:
		largest = player_list[current_largest]._armysize

	# else no one holds it so it size to beat is 2
	# default catan rule
	else:
		largest = 2
	# size of the current players army
	player_army = player_list[player]._armysize

	# checks if greater then the current largest
	if player_army > largest:
		# if no one holds largest army
		# it only changes one players vp stat
		if current_largest == None:
			player_list[player]._vp += 2
			return player
		# if someone does hold it
		# changes both players appropriately
		if current_largest != None:
			player_list[current_largest]._vp -= 2
			player_list[player]._vp += 2
		return 
	# returns same player if player was not challenged
	return current_largest



def _populate_edges(graph, vertices):
	'''
	takes in a graph class object and a list of vertices.
	returns a list of edges (tuple)
	'''
	edges = []

	for v in vertices:
		neighbours = graph.neighbours(v)
		for neighbour in neighbours:
			edges.append((v, neighbour))
			edges.append((neighbour, v))

	return edges



def graph_roads(roads):
	network = Graph()
	# what if we did populate a graph?
	for edge in roads:
		for vertex in edge:
			if not network.is_vertex(vertex):
				network.add_vertex(vertex)
				#already_populated.append(vertex)
		# now graph just needs to edges/road segments
		network.add_edge(edge)
		network.add_edge((edge[1], edge[0]))

	return network


def make_set(roads, network):
	'''
	function that takes in the list of the active roads
	of a player and the graph(network) that the roads make up
	and sorts the roads into lists that represent a connected
	segment. These lists are then placed into another list
	and returned

	'''

	# our list of vertices
	vertice_list = network.vertices()
	vertice_list = list(vertice_list)
	# what we will return
	vertice_segments = []
	# goes through every element
	while vertice_list != []:
		# pop a random vertice
		random_vertice = vertice_list.pop()
		# segment that we will make now
		segment = []
		# add its first element
		segment.append(random_vertice)
		if vertice_list != []:
			# now check if random element is connected to the rest
			for vertice in vertice_list:
				# check if its connected
				path = find_path(network, random_vertice, vertice)
				# if its not connected do nothing
				if path == None:
					pass
				else:
					# it must be connected add to current segment
					segment.append(vertice)
			# remove the connected elements from the original list
			i = 1
			while i != len(segment):
				vertice_list.remove(segment[i])
				i += 1
		# append to the list
		vertice_segments.append(segment)
	return vertice_segments
	
	'''
	print("roads:")
	print(roads)
	# make our list of all vertices
	vertice_list = network.vertices()
	vertice_list2 = network.vertices()
	vertice_list = list(vertice_list)

	print("vertice list:")
	print(vertice_list)
	# segment of vertices that are connected
	vertice_segments = []
	segments = []

	poor_fit = []

	curr = vertice_list.pop()
	print('curr (first): ' + str(curr))
	while len(vertice_list) > 0 and len(poor_fit) > 0:

		if len(vertice_list) is 0:
			# then this segment is finished
			vertice_list = poor_fit
			poor_fit = []
			if len(segments) > 0:
				vertice_segments.append(segments)
				segments = []
				curr = vertice_list.pop()
				print('curr (pop): ' + str(curr))

		segment.append(curr) # start new segment
		succ = vertice_list.pop()
		path = find_path(network, curr, succ)
		if path is None:
			poor_fit.append(succ) # doesnt fit, don't need it
			print('doesnt fit')
		else:
			# does fit
			# add to segment
			segment.append(succ)
			curr = succ # check these neighbours now
			print('curr: ' + str(curr))


	return vertice_segments
	'''

'''
		while vertice_list != []:
		poor_fit = []
		curr = vertice_list.pop() # start with random vertex
		#vertice_list2 = list(vertice_list)
		for vertices in vertice_list:
			succ = vertice_list.pop()
			path = find_path(network, curr, vertices)
			if path is None:
				poor_fit.append()
			else:
				curr = vertices
				#vertice_list.remove(vertices)
				#segments.append(temp)
		
		if segments != []:
			vertice_segments.append(segments)

	return vertice_list
'''

def longest_road(roads):
	"""
	finds the longest road

	From http://stackoverflow.com/questions/3191460/finding-the-longest-road-in-a-settlers-of-catan-game-algorithmically

	^ some algorithm ideas which lead to the pseudo code commented below

	^ didnt actually use that
	Dijstra's is normally )(ElogE)
	but this does not make use of a binary tree, because there are no weightings
	meaning we decided to pop onto queue randomly as opposed to min/maxs

	this means we have to explore all possibilities and this becomes a NP
	problem. ie no polynomial time

	Would be O(2^n) because we must explore a possibility of length n (number
		of nodes) but the worst case is branching between two choices 'n' times


	"""
	network = graph_roads(roads)
	sets = make_set(roads, network)

	if len(roads) < 1:
		return 0
	if len(roads) < 2:
		return 1
	network = graph_roads(roads)
	nodes = []
	for v in network.vertices():
		if len(network.neighbours(v)) == 1:
			nodes.append(v)
	if len(nodes) == 0:
		# then we know its a loop
		length = len(network.vertices())
		return length
	# if we broke, we have an endpoint. 
	# if we didn't, we have a random
	try:
		node = nodes[0]
		dest = nodes[1]
	except IndexError:
		return 1

	# let's adapt least_cost_path from a1 because I am out of ideas
	visited = dict()
	dist    = dict()

	length = 0

	Queue = list() # NOT a priority queue, since there are no weights :P

	Queue.append(((node, node), 0)) # add starting node

	while len(Queue) > 0:
		((prev, curr), val) = Queue.pop() # random since no weight
		if curr not in visited.keys():
			visited[curr] = prev # then add it
			dist[curr] = val # save the distance 

			for succ in network.neighbours(curr):
				# add each tuple and corresponding length to Q
				temp_dist = val + 1
				Queue.append(((curr, succ), temp_dist))
	vertex = dest # starting value (reverse)
	while vertex != node:
		length += 1 # increment length 
		try:
			vertex = visited[vertex]
		except KeyError:
			break

	return length 












	'''
	some pseudo code:
	assuming we start with sets of connected vertices
	start from endpoint 
	traverse until a decision must be made 
	when a decision must be made, what should we do? 
	sub-problem:
	call the function again (once for each possible decision)
	add the larger value to your current counter
	'''



	'''
	if len(roads) is 0:
		return 0
	networks = graph_roads(roads) # populate graph
	list_of_sets = make_set(roads, networks) # populate sets of connected edge
	print("lists of sets:")
	print(list_of_sets)
	lengths = []
	# do this for each list of sets
	for road in list_of_sets:
		lengths.append(_longest_road(road, networks))
	return max(lengths)




def _longest_road(road_set, network):
	print('road set: ')
	print(road_set)
	length = 0 # start length
	# find endpoint 
	# note that later I'll have to account for circular loops
	node = None
	for v in road_set:
		node = v
		if network.neighbours(v) == 1:
			break
	# if we broke, we have an endpoint. 
	# if we didn't, we have a random

	# now to traverse until a decision
	# while it's NOT an endpoint...
	neighbours = list(network.neighbours(node))
	visited = []
	visited.append(node)
	while len(neighbours) > 0:
		# in a perfect world, they all have two neighbours...
		# one of them is the vertex we came from, the other is the next
		# vertex.
		# let's envision that perfect world for a moment.
		# strip neighbours of any nodes already visited
		for neighbour in neighbours:
			print("neighbour: " + str(neighbour))
			if neighbour in visited:
				neighbours.remove(neighbour)
			#print(neighbours)

		# now follow on to the next neighbour!
		# some quick checking to see if we are still in this perfect world
		if len(neighbours) < 1 and len(neighbours) > 0:
			# we have visited this neighbour:
			visited.append(neighbour)
			# increment length
			print("increasing len")
			length += 1

		# well that's great and dandy, what if there is a decision to 
		# make???
		elif len(neighbours) >= 2:
			temp_len = [] # we are going to need to save all possible vals
			for neighbour in neighbours:
				# populate a sub-road list
				new_vert_list = []
				visited.append(neighbour)
				for new_v in road_set:
					if new_v not in visited:
						new_vert_list.append(new_v)

				new_road_list = _populate_edges(network, new_vert_list)
				print(new_road_list)


				# recurrrrrrrrrrrrrrrrrrrrrrrrrrrrrrsion!!!!!!
				print("about to recursively call")
				temp_len.append(longest_road(new_road_list))

			# take longest sub path
			length += max(temp_len)
			neighbours = []
		neighbours = network.neighbours(neighbour)


	print("length: " + str(length))
	return length



	'''

























	''' meh
	network = graph_roads(roads)

	vertice_list = network.vertices()
	for vertex in vertice_list:
		v = vertex
		neighbours = network.neighbours(v)
		for neighbour in neighbours:

			visited = list(v)
			while neighbour not in visited:
				# find neighbours of v
				neighbour = network.neighbours(v)
				visited.append(v)
	'''






















































	'''
	Useless failure of an attempt:
	Joey is a failure
	# list of tuples, each is a road segment
	# start with the first one
	while(len(roads) > 0):
		road = roads.pop() # take a random segement 
		curr_node = road[0] # starting node
		possible_directions = []
		possibe_directions.append(road[1])

		for next_road in roads:
			if next_road[1] is curr_node:
				possible_directions.append(next_road[1])
	'''












	'''
	road_length = 0
	prev_node = 0
	edges = road_graph.edges()
	start = find_start(edges, road_graph)

	for starts in start:
		curr_node = starts
		prev_node = starts
		while len(v) != 1 and v not in start:

			v = road_graph.neighbours(curr_node)

			if len(v) == 1:
				road_length += 1
			if len(v) == 2:
				if v[0] != prev_node:
					road_length += 1
					curr_node = v[0]
				if v[1] != prev_node:
					road_length += 1
					curr_node = v[1]
			if len(v) == 3:
				if v[0] != prev_node:
					road_length += 1
					curr_node = v[0]
				if v[1] != prev_node:
					road_length += 1
					curr_node = v[1]
				if v[2] != prev_node:
					road_length += 1
					curr_node = v[2]


'''

def find_starts(edges, graph):

	starting_pts = []
	for e in edges:
		vertice1 = e[0]
		vertice2 = e[1]

		if len(graph.neighbours(vertice1)) == 1:
			if vertice1 not in starting_pts:
				starting_pts.append(vertice1)

		if len(graph.neighbours(vertice2)) == 1:
			if vertice2 not in starting_pts:
				starting_pts.append(vertice1)

	return starting_pts


	"""
	Function which takes in a list of consecutive road "segments" and
	returns the index of the largest one
	"""
	'''
	max_road = roads[0]
	i = 0
	max_index = 0
	for segments in roads:
		if segment > max_road:
			max_road = segment
			max_index = i
		i = i + 1

	return max_index, max_road
	'''
