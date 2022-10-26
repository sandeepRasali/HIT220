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
        self.graph = [None] * self.vertices # vertex list
    
    def add_edge(self, v1, v1_weights, v2, v2_weights):
        # connect second vertex to first vertex at first vertex's position in vertex list
        node = Node(v2, v2_weights)
        node.next = self.graph[v1 - 1]
        self.graph[v1 - 1] = node

        # connect second vertex to first vertex at second vertex's position in vertex list
        node = Node(v1, v1_weights)
        node.next = self.graph[v2 - 1]
        self.graph[v2 - 1] = node
  
   # Function to print a BFS of graph
    def BFS(self, startNode):
 
        # Mark all the vertices as not visited
        visited = [False] * (max(self.graph) + 1)
 
        # Create a queue for BFS
        queue = []
 
        # Mark the source node as
        # visited and enqueue it
        queue.append(s)
        visited[s] = True
 
        while queue:
 
            # Dequeue a vertex from
            # queue and print it
            s = queue.pop(0)
            print (s, end = " ")
 
            # Get all adjacent vertices of the
            # dequeued vertex s. If a adjacent
            # has not been visited, then mark it
            # visited and enqueue it
            for i in self.graph[s]:
                if visited[i] == False:
                    queue.append(i)
                    visited[i] = True
class CrocMonitor:
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

            vertex = self.graph.graph[i] # get vertex

            while vertex:
                print(" -> {}".format(vertex.data) + ", {}".format(vertex.weights), end = "")
                vertex = vertex.next

            print("\n")

def add_sighting():
    pass

# Driver Code
if __name__ == '__main__':
    cm = CrocMonitor()
    cm.import_data('CrocDataNodes.csv')
    # print("Croc Data:")
    # cm.read_data()

    # print("\n")

    cm.create_graph()
    edges = CrocMonitor()
    edges.import_data('CrocDataEdges.csv')

    graph = Graph()
    graph.BFS(2)