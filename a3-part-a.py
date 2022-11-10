import csv
import math

# Node Representation
class Node:
    def __init__(self, source, data, weights):
        self.source = source
        self.data = data
        self.weights = weights
        self.next = None

# Graph Representation - Adjacency List
class Graph:
    def __init__(self, vertices):
        self.vertices = vertices # total number of vertices
        self.list = [None] * self.vertices # vertex list

    def add_edge(self, v1, v2, v1_weights = None, v2_weights = None):
        # connect second vertex to first vertex at first vertex's position in vertex list
        node = Node(v1, v2, v2_weights)
        node.next = self.list[v1 - 1]
        self.list[v1 - 1] = node

        # connect second vertex to first vertex at second vertex's position in vertex list
        node = Node(v2, v1, v1_weights)
        node.next = self.list[v2 - 1]
        self.list[v2 - 1] = node

    # **Psuedocoded** Find Next Site Algorithm:

    # Breadth First Search to find the adjacent nodes in the graph
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

    # def next_site(previous_site, previous_number):
    #     # call bfs() to get the adjacent sites of previous_site
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
            
    #     # call bfs() recursively to start searching from new node.   
    #     bfs(newNode)  # newNode = node with highest weight
        
    #     nearest_site = node

    #     return node and location

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
    
    def read_data(self):
        print(self.node_list)

    def create_graph(self):
        self.graph = Graph(len(self.node_list))
    
    def display_graph(self):
        for i in range(self.graph.vertices):
            vertex = self.graph.list[i]
            print("Vertex " + str(vertex.source) + ":", end = "")

            while vertex:
                print(" -> {}".format(vertex.data) + ", {}".format(vertex.weights), end = "")
                vertex = vertex.next

            print("\n")

def add_sighting(graph, site: int, source: int = None, distance: float = 1, water: bool = False):
    if site <= graph.vertices:
        for i in range(graph.vertices):
            vertex = graph.list[i]

            while vertex:
                if vertex.data == site:
                    vertex.weights["sightings"] += 1
            
                vertex = vertex.next
    else:
        if source <= graph.vertices:
            # prepare weights of new edge
            previous_sightings = 0

            for i in range(graph.vertices):
                vertex = graph.list[i]

                while vertex:
                    if vertex.data == source:
                        previous_sightings = vertex.weights["sightings"]

                        break # break loop early if matching vertex is found
                
                    vertex = vertex.next

            previous_weights = {"distance": distance, "water": water, "sightings": previous_sightings}
            location_weights = {"distance": distance, "water": water, "sightings": 1}

            # add temporarily empty vertex to end of list
            graph.vertices += 1
            graph.list += [None]

            # create edge with weight between new vertex and existing vertex
            graph.add_edge(site, source, location_weights, previous_weights)
        else:
            print("\033[91m{}\033[00m".format("add_sighting() error: source site does not exist\n"))

# Merge Sort Algorithm adapted from https://www.geeksforgeeks.org/merge-sort/
def merge_sort(array): # input should be an adjacency list with a "sightings" weight on edges
    if len(array) > 1: # base case
        mid = len(array) // 2 # midpoint
        left = array[:mid] # left half
        right = array[mid:] # right half

        merge_sort(left) # sort left half
        merge_sort(right) # sort right half

        i = j = k = 0 # iterators
        
        while i < len(left) and j < len(right):
            if left[i].weights["sightings"] > right[j].weights["sightings"]:
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
if __name__ == '__main__':
    # Import Datasets
    cm = CrocData()
    cm.import_data('CrocDataNodes.csv')
    print("Croc Nodes Data:\n")
    cm.read_data()
    # print("\n")

    edges = CrocData()
    edges.import_data('CrocDataEdges.csv')

    # Show Data (comment/uncomment as needed)
    # print("Croc Edges Data:\n")
    # edges.read_data()
    # print("\n")

    # Implement Datasets as Adjacency List
    cm.create_graph()

    for i in range(0, len(edges.node_list)):
        # for creating edges between vertices
        v1 = int(edges.node_list[i][0])
        v2 = int(edges.node_list[i][1])

        # for adding distance to edge as weight
        v1_coordinates = [float(cm.node_list[v1 - 1][1]), float(cm.node_list[v1 - 1][2])]
        v2_coordinates = [float(cm.node_list[v2 - 1][1]), float(cm.node_list[v2 - 1][2])]
        distance = round(math.dist(v1_coordinates, v2_coordinates), 1) # calculate the distance and round to one decimal place

        # for adding if water exists to edge as weight
        water = bool(int(edges.node_list[i][2]))

        # for adding sightings to edge as weight
        v1_sightings = int(cm.node_list[v1 - 1][4])
        v2_sightings = int(cm.node_list[v2 - 1][4])

        # create edges with weights between vertices
        v1_weights = {"distance": distance, "water": water, "sightings": v1_sightings}
        v2_weights = {"distance": distance, "water": water, "sightings": v2_sightings}
        cm.graph.add_edge(v1, v2, v1_weights, v2_weights)
    
    # Show Graph (comment/uncomment as needed)
    # print("Croc Adjacency List:\n")
    # cm.display_graph()

    add_sighting(cm.graph, 12) # update an existing site with a new sighting (compare old graph with updated graph to see the change)
    add_sighting(cm.graph, 33, 12, 2.4, False) # add a new site with a new sighting and connect it to Vertex 12

    # Show Graph (comment/uncomment as needed)
    # print("Croc Adjacency List with Added Sightings:\n")
    # cm.display_graph()

    merge_sort(cm.graph.list)
    print("Merge Sorted Adjacency List:\n")
    cm.display_graph()