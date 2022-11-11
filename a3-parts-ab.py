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

    # Breadth First Search Algorithm - NEEDS UPDATING
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

    # Dijkstra's Algorithm - for finding the shortest path of a weighted graph,
    # in O(ElogV) time, where E is edge and V is vertex.
    # Note: adapted from https://www.geeksforgeeks.org/dijkstras-algorithm-for-adjacency-list-representation-greedy-algo-8/
    # Note: This algorithm is bugged currently as it sometimes does not calculate the shortest distance for all vertices depending on the source input.
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

    # PSEUDOCODE: The following code calculates and ouputs the closest site with the maximum number of sightings. - NEEDS UPDATING
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

    # PSUEDOCODE: The following code computes the costing (in distance travelled) of performing an exhaustive search of all sites within an area bound by two sites.
    def compute_costing(self, top_left, bottom_right):
        pass

    # PSEUDOCODE: The following code determines where to place a blockage in the shortest route between two points to maximise the shortest distance between them.
    def improve_distance(self, a, b):
        shortest = self.graph.dijkstra(a) # calculate the shortest distances and paths from a

        for i in range(0, len(shortest)):
            if shortest[i][0] == b:
                dist = shortest[i][1] # store the shortest distance from a to b
                path = shortest[i][2] # store the shortest path from a to b

                break

        alt = []

        for i in range(0, len(path)):
            if i == 0 or i == len(path):
                continue # skip site a and site b (see assumptions)
            else:
                # INSERT CODE: place blockage between site i and i + 1

                blocked = self.graph.dijkstra(a) # calculate the alternate shortest distances and paths from a with blockage in place
                
                for j in range(0, len(blocked)):
                    if blocked[j][0] == b:
                        alt_dist = blocked[j][1] # store the alternate distance from a to b

                        break
                
                improvement = round(alt_dist / dist, 1) # alternate distance proportionate to original distance as the higher the ratio the better

                alt.append([i, improvement]) # store the distance ratio of when the blockage is placed at i

                # INSERT CODE: remove blockage between site i and i + 1
        
        merge_sort_dsc(alt, 1) # sort by largest ratio

        return f"By placing a blockage at location {alt[0][0]}, the distance between {a} and {b} is improved by a ratio of {alt[0][1]}."



""" Question C

Pseudocoded answer:



# this function calculates the croc travel time either in water or environment
def crocTravelTime(self, distance, isWater):  # isWater = 1 if the route is through the water
                                                #and 0 if it is through land
    
    travelTime = 0
    crocSpeed = 0
    
    if route is through Water:
        crocSpeed = 16 # km/hr
    
    else route is through Environmen:
        crocSpeed = 5   #km/hr
        
    
    travelTime = distance/crocSpeed   #(speed = distance / time)
    return travelTime

def calculateDistance(self, v1, v2):
    for i in range(0, len(edges.node_list)):
        # for creating edges between vertices
        v1 = int(edges.node_list[i][0])
        v2 = int(edges.node_list[i][1])

        # for adding distance to edge as a weight
        v1_coordinates = [float(cd.node_list[v1 - 1][1]), float(cd.node_list[v1 - 1][2])]
        v2_coordinates = [float(cd.node_list[v2 - 1][1]), float(cd.node_list[v2 - 1][2])]
        distance = round(math.dist(v1_coordinates, v2_coordinates), 1) # calculate the distance and round to one decimal place
        return distance
        
def storeDistance(self):
    
    edgeList = []
    for i in range (0, len(edges.node_list)-1):
       startPoint = self.edges[i][0]       # nodes in the graph
       endPoint =  self.edges[i][1]     # neighbor (adjacent nodes)
       iswater = self.edges[i][2]
       distance = self.calculateDistance(startNode, endNode)   #calculates the distance between two nodes
       edgeList.append(startPoint, endPoint, distance, iswater)
       
def minTime(self, a, b): # this function returns array of sites travelled and time required btween two points a and b
  route = [] # assigning list variable to store the paths between two given points
  totalTravelTime = 0
  
  
  for edge in self.edgeList:
      edge.append(self.crocTravelTime(edge[2], edge[3])) # calculating crocTraveltime and appending in the edge
      
      
  #using dijkstra's algorithm to find the shortest routes
  
  path = self.graph.dijkstra(self, a)   
  target = b   
  for i in range (0, len(path)-1):
      totalTravelTime += graph.weights[path[i], path[i+1]]
      
      print ("Shortest path between a and b and minimum time taken to travel is: ", totalTravelTime, path)
"""

    
    def point_no_pass(point, radius):
        pass

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
    edges.import_data("CrocDataEdges.csv")

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
    cd.add_sighting(33, 3, True, 34)
    cd.display_as_graph()