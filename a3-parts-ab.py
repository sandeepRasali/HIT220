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

    def is_empty(self):
        return True if self.size == 0 else False

    def is_in_heap(self, v):
        return True if self.position[v] < self.size else False

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

    # Dijkstra's Algorithm - for finding the shortest path of a weighted graph,
    # in O(ElogV) time, where E is edge and V is vertex.
    # Note: adapted from https://www.geeksforgeeks.org/dijkstras-algorithm-for-adjacency-list-representation-greedy-algo-8/
    def dijkstra(self, source):
        vertices = self.vertices
        dist = []
        path = [[]] * self.vertices # stores paths
        target = source - 1 # for indexing

        # construct min heap
        min_heap = MinHeap()

        min_heap.size = vertices

        for v in range(vertices):
            dist.append(1e7) # initialise with large distance to all nodes
            min_heap.array.append(min_heap.new_node(v, dist[v]))
            min_heap.position.append(v)

        # distance to source equals 0
        dist[target] = 0
        min_heap.decrease_key(target, dist[target])

        while min_heap.is_empty() == False:
            min = min_heap.extract_min()
            node = min[0]

            # # for debugging
            # print("Vertex", node + 1)
            # print("Min Distance =", round(min[1], 1))
            # print("To\tDistance\tPrev Distance\t")

            for i in range(vertices):
                vertex = self.list[i]

                if vertex.source == node + 1:
                    while vertex:
                        data = vertex.data

                        # # for debugging
                        # print(f"{data}\t{round(vertex.weights['distance'] + dist[node], 1)}\t\t{round(dist[data - 1], 1)}")

                        if vertex.weights["distance"] + dist[node] < dist[data - 1]:
                            dist[data - 1] = vertex.weights["distance"] + dist[node]
                            min_heap.decrease_key(data - 1, dist[data - 1])
                            
                            # PSUEDOCODE
                            # add adjancent vertex with shortest path to path list

                        vertex = vertex.next

        # # for debugging
        # print(f"Vertices\tDistance from {source}\t\tPath")

        # for i in range(vertices):
        #     print("%d\t\t%.1f" % (i + 1, dist[i]), f"\t\t\t{path[i]}")

        output = [[i + 1, round(dist[i], 1)] for i in range(vertices)] # temporary output
        # OPTIMAL OUTPUT IN PSUEDOCODE: output = [[i + 1, round(dist[i], 1), path[i]] for i in range(vertices)]
        merge_sort(output)

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

# Merge Sort
# Note: adapted from https://www.geeksforgeeks.org/merge-sort/
def merge_sort(array):
    if len(array) > 1: # base case
        mid = len(array) // 2 # midpoint
        left = array[:mid] # left half
        right = array[mid:] # right half

        merge_sort(left) # sort left half
        merge_sort(right) # sort right half

        i = j = k = 0 # iterators
        
        while i < len(left) and j < len(right):
            if left[i][1] < right[j][1]:
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
    cd.display_as_graph()

    print(cd.graph.dijkstra(4))