import csv
import math

# Node Representation
class Node:
    def __init__(self, data, weights):
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
        node = Node(v2, v2_weights)
        node.next = self.list[v1 - 1]
        self.list[v1 - 1] = node

        # connect second vertex to first vertex at second vertex's position in vertex list
        node = Node(v1, v1_weights)
        node.next = self.list[v2 - 1]
        self.list[v2 - 1] = node

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
            print("Vertex " + str(i + 1) + ":", end = "")

            vertex = self.graph.list[i] # get vertex

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
            # prepare weights with
            previous_sightings = 0

            for i in range(graph.vertices):
                vertex = graph.list[i]

                while vertex:
                    if vertex.data == source:
                        previous_sightings = vertex.weights["sightings"]

                        break
                
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
            

# Driver Code
if __name__ == '__main__':
    # Import Datasets
    cm = CrocData()
    cm.import_data('CrocDataNodes.csv')
    # print("Croc Nodes Data:\n")
    # cm.read_data()
    # print("\n")

    edges = CrocData()
    edges.import_data('CrocDataEdges.csv')
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
    
    # print("Croc Adjacency List:")
    # cm.display_graph()

    add_sighting(cm.graph, 33, 32)

    print("Croc Adjacency List with Added Sightings:\n")
    cm.display_graph()
