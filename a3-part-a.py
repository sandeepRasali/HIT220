import csv

# Node Representation
class Node:
    def __init__(self, data, weight):
        self.data = data
        self.weight = weight
        self.next = None

# Graph Representation - Adjacency List
class Graph:
    def __init__(self, vertices):
        self.vertices = vertices # total number of vertices
        self.graph = [None] * self.vertices # vertex list
    
    def add_edge(self, v1, v1_weight, v2, v2_weight):
        # connect second vertex to first vertex at first vertex's position in vertex list
        node = Node(v2, v2_weight)
        node.next = self.graph[v1 - 1]
        self.graph[v1 - 1] = node

        # connect second vertex to first vertex at second vertex's position in vertex list
        node = Node(v1, v1_weight)
        node.next = self.graph[v2 - 1]
        self.graph[v2 - 1] = node

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
                print(" -> [{}".format(vertex.data) + ", {}]".format(vertex.weight), end = "")
                vertex = vertex.next

            print("\n")

# Driver Code
if __name__ == '__main__':
    cm = CrocMonitor()
    cm.import_data('CrocDataNodes.csv')
    print("Croc Data:")
    cm.read_data()

    print("\n")

    cm.create_graph()
    edges = CrocMonitor()
    edges.import_data('CrocDataEdges.csv')

    for i in range(0, len(edges.node_list)):
        v1 = int(edges.node_list[i][0])
        v2 = int(edges.node_list[i][1])
        v1_weight = int(cm.node_list[v1 - 1][4])
        v2_weight = int(cm.node_list[v2 - 1][4])
        cm.graph.add_edge(v1, v1_weight, v2, v2_weight)
    
    print("Croc Adjacent List:")
    cm.display_graph()

# Don't Use; this sort might need to be rewritten to work.

# Merge Sort Algorithm adapted from https://www.geeksforgeeks.org/merge-sort/
# def merge_sort_desc(array, sort_by_index: int):
#     if len(array) > 1:
#         mid = len(array) // 2 # midpoint
#         left = array[:mid] # left half
#         right = array[mid:] # right half

#         merge_sort_desc(left, sort_by_index) # sort left half
#         merge_sort_desc(right, sort_by_index) # sort right half

#         i = j = k = 0 # iterators

#         while i < len(left) and j < len(right):
#             if left[i][sort_by_index] > right[j][sort_by_index]:
#                 array[k] = left[i]
#                 i += 1
#             else:
#                 array[k] = right[j]
#                 j += 1
#             k += 1

#         while i < len(left):
#             array[k] = left[i]
#             i += 1
#             k += 1
        
#         while j < len(right):
#             array[k] = right[j]
#             j += 1
#             k += 1