import csv

# Node Representation
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

# Graph Representation - Adjacency List
class Graph:
    def __init__(self, vertices):
        self.vertices = vertices # total number of vertices
        self.graph = [None] * self.vertices # vertex list
    
    def add_edge(self, v1, v2):
        # connect second vertex to first vertex at first vertex's position in vertex list
        node = Node(v2)
        node.next = self.graph[v1]
        self.graph[v1] = node

        # connect second vertex to first vertex at second vertex's position in vertex list
        node = Node(v1)
        node.next = self.graph[v2]
        self.graph[v2] = node

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
        print(self.graph.graph)

# Driver Code
if __name__ == '__main__':
    cm = CrocMonitor()
    
    cm.import_data('CrocDataNodes.csv')
    print("Croc Data:")
    cm.read_data()

    cm.create_graph()
    print("Croc Graph:")
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