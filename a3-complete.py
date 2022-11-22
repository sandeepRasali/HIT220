import csv
import math

# Node Representation
class Node:
    def __init__(self, data, source, weights):
        self.data = data
        self.source = source # stores what node this node is connected to
        self.weights = weights
        self.next = None

# Min Heap - for optimising Dijkstra's Algorithm in an Adjacency List.
# Note: adapted from https://www.geeksforgeeks.org/dijkstras-algorithm-for-adjacency-list-representation-greedy-algo-8/
class MinHeap:
    def __init__(self):
        self.size = 0
        self.array = []
        self.position = []

    def new_node(self, v, dist):
        node = [v, dist]
        
        return node

    def swap_nodes(self, v1, v2):
        temp = self.array[v1]
        self.array[v1] = self.array[v2]
        self.array[v2] = temp

    # call heapify to preserve the min heap order property
    def heapify(self, index):
        min = index
        left = 2 * index + 1 # left child
        right = 2 * index + 2 # right child

        # left child is the new min if the distance to the left child is less than the distance to the current min
        if left < self.size and self.array[left][1] < self.array[min][1]:
            min = left

        # right child is the new min if the distance to the right child is less than the distance to the current min
        if right < self.size and self.array[right][1] < self.array[min][1]:
            min = right

        if min != index:
            # swap heap nodes
            self.swap_nodes(min, index)

            # swap node positions
            self.position[self.array[min][0]] = index
            self.position[self.array[index][0]] = min

            self.heapify(min)
    
    def extract_min(self):
        if self.is_empty() == True:
            return

        # preserve root node
        root_node = self.array[0]

        # replace root node with last node
        last_node = self.array[self.size - 1]
        self.array[0] = last_node

        # update last node's position
        self.position[last_node[0]] = 0
        self.position[root_node[0]] = self.size - 1

        # decrement heap size and heapify
        self.size -= 1
        self.heapify(0)

        return root_node

    def decrease_key(self, v, dist):
        i = self.position[v]
        self.array[i][1] = dist

        while i > 0 and self.array[i][1] < self.array[(i - 1) // 2][1]:
            # swap this node with parent node
            self.position[self.array[i][0]] = (i - 1) // 2
            self.position[self.array[(i - 1) // 2][0]] = i
            self.swap_nodes(i, (i - 1) // 2)

            # move to parent index
            i = (i - 1) // 2

    def is_in_heap(self, v):
        return True if self.position[v] < self.size else False
    
    def is_empty(self):
        return True if self.size == 0 else False

# Graph Representation - Adjacency List
class Graph:
    def __init__(self, vertices):
        self.vertices = vertices
        self.list = [None] * self.vertices

    def add_edge(self, v1, v2, v1_weights, v2_weights):
        # connect second vertex to first vertex at first vertex's position in vertex list
        node = Node(v2, v1, v2_weights)
        node.next = self.list[v1 - 1]
        self.list[v1 - 1] = node

        # connect first vertex to second vertex at second vertex's position in vertex list
        node = Node(v1, v2, v1_weights)
        node.next = self.list[v2 - 1]
        self.list[v2 - 1] = node

    # Breadth First Search Algorithm !! NEEDS UPDATING !!
    # def bfs(self, startNode):
    #     visited = [False] * self.vertices # mark all the vertices as not visited

    #     queue = [] # queue for BFS

    #     append startNode to queue
    #     mark startNode as visited and enqueue it
        
    #     while queue:
    #         dequeue a vertex from queue and store in an array
    #         then get all adjacent veritices of the dequeued vertex

    #         if adjacent has not been visited:
    #             then mark it as visited and enqueue it
            
    #     return the adjacent vertices array

    # Depth First Search Algorithm - for finding the path of visiting all adjacent vertices from a starting vertex.
    def dfs(self, source, visited = []):
        visited.append(source)

        for i in range(self.vertices):
            vertex = self.list[i]

            if vertex.source == source:
                while vertex:
                    if vertex.data not in visited:
                        self.dfs(vertex.data, visited)

                    vertex = vertex.next
        
        return visited

    # Dijkstra's Algorithm - for finding the shortest path of a weighted graph.
    # Complexity: O(ElogV), where E is edge and V is vertex.
    # Note: adapted from https://www.geeksforgeeks.org/dijkstras-algorithm-for-adjacency-list-representation-greedy-algo-8/
    # Note: This algorithm is bugged currently as it sometimes does not calculate the shortest distance for all vertices depending on the source input.
    # Therefore, the functions reliant on this algorithm will be pseudocoded due to time constraints.
    def dijkstra(self, source):
        vertices = self.vertices
        dist = [] # stores distances
        path = [[]] * self.vertices # stores paths
        target = source - 1 # for indexing

        # construct min heap
        min_heap = MinHeap()

        min_heap.size = vertices

        for v in range(vertices):
            dist.append(1e7) # initialise with large distance to all nodes
            min_heap.array.append(min_heap.new_node(v, dist[v]))
            min_heap.position.append(v)

        dist[target] = 0 # set distance to source to 0
        min_heap.decrease_key(target, dist[target])

        while min_heap.is_empty() == False:
            min = min_heap.extract_min()
            node = min[0]

            # DEBUG CODE:
            # print("Vertex", node + 1)
            # print("Min Distance =", round(min[1], 1))
            # print("To\tDistance\tPrev Distance\t")

            for i in range(vertices):
                vertex = self.list[i]

                if vertex.source == node + 1:
                    while vertex:
                        data = vertex.data

                        # DEBUG CODE:
                        # print(f"{data}\t{round(vertex.weights['distance'] + dist[node], 1)}\t\t{round(dist[data - 1], 1)}")

                        # replace the existing distance for this vertex
                        # if the sum of the adjacent vertex's distance plus the calculated distance of this vertex from the source
                        # is less than existing distance for this vertex
                        if vertex.weights["distance"] + dist[node] < dist[data - 1]:
                            dist[data - 1] = vertex.weights["distance"] + dist[node]
                            min_heap.decrease_key(data - 1, dist[data - 1])
                            
                            # INSERT CODE: add adjancent vertex with shortest path to path list

                        vertex = vertex.next

        # DEBUG CODE:
        # print(f"Vertices\tDistance from {source}\t\tPath")
        # for i in range(vertices):
        #     print("%d\t\t%.1f" % (i + 1, dist[i]), f"\t\t\t{path[i]}")

        # The following is a temporary output for debugging; the real output should be:
        # output = [[i + 1, round(dist[i], 1), path[i]] for i in range(vertices)]
        output = [[i + 1, round(dist[i], 1), []] for i in range(vertices)] 
        merge_sort_dsc(output, 1)

        return output

# Data Handling
class CrocData:
    def __init__(self):
        self.node_list = []
    
    def import_data(self, file):
        with open(file) as f:
            csv_reader = csv.reader(f)
            next(csv_reader)

            for line in csv_reader:
                node = []

                for data in line:
                    if data:
                        node.append(data)
                    else:
                        node.append(None)
            
                self.node_list.append(node)

        f.close()

    def display_as_matrix(self):
        print(self.node_list, "\n")
    
    def create_graph(self):
        self.graph = Graph(len(self.node_list))
    
    def display_as_graph(self):
        try:
            for i in range(self.graph.vertices):
                vertex = self.graph.list[i]
                print("Vertex " + str(vertex.source) + ":", end = "")

                while vertex:
                    print(" -> {}".format(vertex.data) + ", {}".format(vertex.weights), end = "")
                    vertex = vertex.next

                print("\n")
        except:
            print("This dataset has no graph.")

    # PSEUDOCODE: The following code calculates and ouputs the closest site with the maximum number of sightings. !! NEEDS UPDATING !!
    # def next_site(previous_site, previous_number):
    #     call bfs() to get the adjacent sites of previous_site
    #     bfs(previous_site)
        
    #     for i in array:
    #         key = i
    #         row = node_list.get(key)
            
    #         for x in row:
    #             node_weight = row[1]  # getting the croc sighting value for each adjacent nodes
        
    #     then compare the nodes to get the node with the highest node_weight (croc sighting)
        
    #     if node_weight is similar for adjacent nodes
    #         for x in row:
    #             node_distance = row[2]
    #         get node with minimum distance
            
    #     call bfs() recursively to start searching from new node.   
    #     bfs(newNode)  # newNode = node with highest weight
        
    #     nearest_site = node

    #     return node and location

    def add_sighting(self, site: int, distance: float = None, water: bool = None, previous_location: int = None):
        vertices = self.graph.vertices

        if site <= vertices:
            for i in range(vertices):
                vertex = self.graph.list[i]

                while vertex:
                    if vertex.data == site:
                        # increment sightings of this vertex
                        vertex.weights["sightings"] += 1

                    vertex = vertex.next
        else:
            if previous_location <= vertices:
                # prepare sightings of connected vertex
                previous_sightings = 0

                for i in range(vertices):
                    vertex = self.graph.list[i]

                    while vertex:
                        if vertex.data == previous_location:
                            # retrieve sightings of connected vertex
                            previous_sightings = vertex.weights["sightings"]
                    
                        vertex = vertex.next
                
                previous_weights = {"distance": distance, "water": water, "sightings": previous_sightings}
                new_site_weights = {"distance": distance, "water": water, "sightings": 1}

                # add a temporarily empty vertex to the end of the vertices list
                self.graph.vertices += 1
                self.graph.list += [None]
                
                # create a weighted edge between the new site and previous location
                self.graph.add_edge(site, previous_location, new_site_weights, previous_weights)
            else:
                print("\033[91m{}\033[00m".format("add_sighting() error: The previous location specified does not exist\n"))
    
    # PSUEDOCODE: The following code computes the cost (in distance travelled) of performing an exhaustive search of all sites within an area bound by two sites.
    def compute_costing(self, top_left, bottom_right):
        subgraph = Graph(len(self.node_list))

        # INSERT CODE: create edges in the subgraph bound by sites top_left and bottom_right

        # INSERT CODE: sort adjacent vertices for each source vertex by shortest distance,
        # so that the adjacent vertex with the shortest distance to the source vertex is at the top of each linked list

        path = subgraph.dfs(top_left) # perform a depth first search to visit all sites in the subgraph, i.e., all sites in the area
        visited = [] # stores visited sites
        revisit = False # stores if sites will be revisited
        revisiting = [] # stores sites that will be revisited
        cost = 0 # stores overall cost in distance travelled

        visited.append(path[0]) # mark the starting site (top_left) as visited

        for i in range(0, len(path)):
            for j in range(subgraph.vertices):
                vertex = subgraph.list[j]

                if vertex.source == path[i]:
                    # use the distance of the first adjacent vertex, which is already the shortest distance in this vertex's linked list,
                    # as dfs() visits the first adjacent vertex in a linked list and moves on
                    cost += vertex.weights["distance"] # add distance of the first/closest adjacent vertex to the overall cost
                    visited.append(vertex.data) # mark the first/closest adjacent vertex as visited

                    # check if the adjacent vertex has been visited before
                    if vertex.data in visited:
                        revisit = True # a site will be revisited so return true
                        revisiting.append(vertex.data) # mark the site as a site that will be revisited

                    break # continue to next site in path

        print(f"Shortest Path: {path}")
        print(f"Minimum Cost: {cost}")
        print(f"Will sites be revisited? {revisit}")
        print(f"Which sites will be revisited? {revisiting}")

    # PSEUDOCODE: The following code determines where to place a blockage in the shortest route between two sites to maximise the shortest distance between them.
    def improve_distance(self, a, b):
        shortest = self.graph.dijkstra(a) # find the shortest distances and paths from a
        # Note: The output of dijkstra() is [site, shortest distance from source, shortest path from source]

        for i in range(0, len(shortest)):
            if shortest[i][0] == b:
                dist = shortest[i][1] # store the shortest distance from a to b
                path = shortest[i][2] # store the shortest path from a to b

                break

        alt_list = []

        for i in range(0, len(path)):
            if i == 0 or i == len(path):
                continue # skip first route and last route (see assumptions)
            else:
                # INSERT CODE: place blockage between site i and i + 1

                blocked = self.graph.dijkstra(a) # find the alternate shortest distances and paths from a with blockage in place
                
                for j in range(0, len(blocked)):
                    if blocked[j][0] == b:
                        alt_dist = blocked[j][1] # store the shortest alternate distance from a to b

                        break
                
                improvement = alt_dist / dist # alternate distance proportionate to original distance as the higher the ratio the better

                alt_list.append([path[i], improvement]) # store the improvement ratio of when the blockage is placed at site i

                # INSERT CODE: remove blockage between site i and i + 1
        
        merge_sort_dsc(alt_list, 1) # sort by largest ratio

        return f"By placing a blockage at location {alt_list[0][0]}, the distance between {a} and {b} is improved by a ratio of {alt_list[0][1]}."
    
    # PSUEDOCODE: The following code calculates the travel time of the shortest path between two locations.
    # Note: Optionally, you can calculate the travel time between two locations in an area by specifying a subgraph.
    def min_time(self, a, b, subgraph = None):
        if subgraph:
            shortest = subgraph.dijkstra(a)
        else:
            shortest = self.graph.dijkstra(a)

        for i in range(0, len(shortest)):
            if shortest[i][0] == b:
                path = shortest[i][2] # store the shortest path from a to b

        time = 0 # stores overall travel time

        # check the edge weights between each point in the shortest path list
        # and calculate the travel time between these points using crocTravelTime()
        for i in range(0, len(path)):
            for j in range(self.graph.vertices):
                vertex = self.graph.list[j]

                if vertex.source == path[i]:
                    while vertex:
                        if vertex.data == path[i + 1]: # out of indexing range?
                            distance = vertex.weights["distance"]
                            water = vertex.weights["water"]
                            time += crocTravelTime(distance, water)
            
                        vertex = vertex.next
        
        return path, time
    
    # PSEUDOCODE: The following code determines where to place a blockage in an area around a certain site to make it safer.
    # Assumption: The point is made safer by improving the travel time of the shortest path from the site in the area with the most sightings to the center.
    def point_no_pass(self, point, radius):
        subgraph = Graph(self.graph.vertices)

        # INSERT CODE: create edges in the subgraph connecting all the vertices with the area bound by the specified radius

        danger = subgraph.list[0] # stores the site with the most sightings; start with first vertex

        # determine which site in the subgraph has the most sightings
        for i in range(subgraph.vertices):
            vertex = subgraph.list[i]

            while vertex:
                if vertex.weights["sightings"] > danger.weights["sightings"]:
                    danger = vertex

                vertex = vertex.next

        travel_time = self.min_time(point, danger, subgraph) # calculate the base minimum travel time
        blockage = None # stores blockage location

        shortest = subgraph.dijkstra(point) # find the shortest paths to all sites from the center

        for i in range(0, len(shortest)):
            if shortest[i][0] == danger.data:
                path = shortest[i][2] # store the unblocked shortest route from the center to the site with most sightings 

                break

        # similar code to improve_distance(), adapted for travel time
        for i in range(0, len(path)):
            if i == 0 or i == len(path):
                continue # skip first route and last route (see assumptions)
            else:
                # INSERT CODE: place blockage between site i and i + 1

                new_time = self.min_time(point, danger, subgraph) # calculate minimum travel time with blockage in place

                # if the travel time with the blockage at this location is improved, update travel time and blockage location
                if new_time[1] > travel_time[1]:
                    travel_time = new_time
                    blockage = path[i]

                # INSERT CODE: remove blockage between site i and i + 1

        return blockage

# The following code calculates the travel time of a croc depending on the terrain its travelling in.
def crocTravelTime(distance, water):
    time = 0
    speed = 0
    
    if water == True:
        speed = 16 # km/h
    else:
        speed = 6 # km/h
    
    time = distance / speed # speed = distance / time

    return time

# Merge Sort Ascending - for sorting a two-dimensional matrix in ascending order by a specified index
# Note: adapted from https://www.geeksforgeeks.org/merge-sort/
def merge_sort_asc(array, index):
    if len(array) > 1: # base case
        mid = len(array) // 2 # midpoint
        left = array[:mid] # left half
        right = array[mid:] # right half

        merge_sort_asc(left) # sort left half
        merge_sort_asc(right) # sort right half

        i = j = k = 0 # iterators
        
        while i < len(left) and j < len(right):
            if left[i][index] < right[j][index]:
                array[k] = left[i]
                i += 1
            else:
                array[k] = right[j]
                j += 1
            k += 1

        while i < len(left):
            array[k] = left[i]
            i += 1
            k += 1
        
        while j < len(right):
            array[k] = right[j]
            j += 1
            k += 1

# Merge Sort Descending - for sorting a two-dimensional matrix in descending order by a specified index
# Note: adapted from https://www.geeksforgeeks.org/merge-sort/
def merge_sort_dsc(array, index):
    if len(array) > 1: # base case
        mid = len(array) // 2 # midpoint
        left = array[:mid] # left half
        right = array[mid:] # right half

        merge_sort_dsc(left) # sort left half
        merge_sort_dsc(right) # sort right half

        i = j = k = 0 # iterators
        
        while i < len(left) and j < len(right):
            if left[i][index] > right[j][index]:
                array[k] = left[i]
                i += 1
            else:
                array[k] = right[j]
                j += 1
            k += 1

        while i < len(left):
            array[k] = left[i]
            i += 1
            k += 1
        
        while j < len(right):
            array[k] = right[j]
            j += 1
            k += 1
                
# Driver Code
if __name__ == "__main__":
    cd = CrocData()
    cd.import_data("CrocDataNodes.csv")
    
    print("Croc Nodes Data:\n")
    cd.display_as_matrix()

    edges = CrocData()
    edges.import_data("CrocDataEdgesNew.csv")

    print("Croc Edges Data:\n")
    edges.display_as_matrix()

    # create adjacency list using datasets
    cd.create_graph()

    # workaround - manual code for creating edges because two datasets are being used
    for i in range(0, len(edges.node_list)):
        # for creating edges between vertices
        v1 = int(edges.node_list[i][0])
        v2 = int(edges.node_list[i][1])

        # for adding distance to edge as a weight
        v1_coordinates = [float(cd.node_list[v1 - 1][1]), float(cd.node_list[v1 - 1][2])]
        v2_coordinates = [float(cd.node_list[v2 - 1][1]), float(cd.node_list[v2 - 1][2])]
        distance = round(math.dist(v1_coordinates, v2_coordinates), 1) # calculate the distance and round to one decimal place

        # for adding if water exists to edge as a weight
        water = bool(int(edges.node_list[i][2]))

        # for representing sightings as an attribute of a vertex
        v1_sightings = int(cd.node_list[v1 - 1][4])
        v2_sightings = int(cd.node_list[v2 - 1][4])

        # create edges with weights between vertices
        v1_weights = {"distance": distance, "water": water, "sightings": v1_sightings}
        v2_weights = {"distance": distance, "water": water, "sightings": v2_sightings}
        cd.graph.add_edge(v1, v2, v1_weights, v2_weights)

    print("Croc Nodes Adjacency List:\n")
    cd.display_as_graph()
