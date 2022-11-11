#  Question C

# Pseudocoded answer:



# # this function calculates the croc travel time either in water or environment
# def crocTravelTime(self, distance, isWater):  # isWater = 1 if the route is through the water
#                                                 #and 0 if it is through land
    
#     travelTime = 0
#     crocSpeed = 0
    
#     if route is through Water:
#         crocSpeed = 16 # km/hr
    
#     else route is through Environmen:
#         crocSpeed = 5   #km/hr
        
    
#     travelTime = distance/crocSpeed   #(speed = distance / time)
#     return travelTime

# def calculateDistance(self, v1, v2):
#     for i in range(0, len(edges.node_list)):
#         # for creating edges between vertices
#         v1 = int(edges.node_list[i][0])
#         v2 = int(edges.node_list[i][1])

#         # for adding distance to edge as a weight
#         v1_coordinates = [float(cd.node_list[v1 - 1][1]), float(cd.node_list[v1 - 1][2])]
#         v2_coordinates = [float(cd.node_list[v2 - 1][1]), float(cd.node_list[v2 - 1][2])]
#         distance = round(math.dist(v1_coordinates, v2_coordinates), 1) # calculate the distance and round to one decimal place
#         return distance
        
# def storeDistance(self):
    
#     edgeList = []
#     for i in range (0, len(edges.node_list)-1):
#        startPoint = self.edges[i][0]       # nodes in the graph
#        endPoint =  self.edges[i][1]     # neighbor (adjacent nodes)
#        iswater = self.edges[i][2]
#        distance = self.calculateDistance(startNode, endNode)   #calculates the distance between two nodes
#        edgeList.append(startPoint, endPoint, distance, iswater)
       
# def minTime(self, a, b): # this function returns array of sites travelled and time required btween two points a and b
#   route = [] # assigning list variable to store the paths between two given points
#   totalTravelTime = 0
  
  
#   for edge in self.edgeList:
#       edge.append(self.crocTravelTime(edge[2], edge[3])) # calculating crocTraveltime and appending in the edge
      
      
#   #using dijkstra's algorithm to find the shortest routes
  
#   path = self.graph.dijkstra(self, a)   
#   target = b   
#   for i in range (0, len(path)-1):
#       totalTravelTime += graph.weights[path[i], path[i+1]]
#       return path and totalTravelTime




# def point_no_pass(self, safeLocation, radius): # this function return the point to be blocked to ensure the location is safer
#     crocNumber = 0
#     locationIndex = 0
#     locationDistanceList = {}
#     inRange = {}
    
#     for i in range (0, len(self.node_list)):
#         if self.node_list[i][0] == safeLocation:
#             locationIndex = i
            
#     for i in range(0, len(self.node_list)):
#             locationDistanceList[self.node_list[i][0]] = self.computeDistance1(safeLocation, self.node_list[i][0],
#                                                                                     locationIndex, i)

#     for key in locationDistanceList:
#             if locationDistanceList.get(key) <= radius:
#                 inRange[key] = locationDistanceList.get(key)

#     for node in self.node_list:
#             if node[0] in inRange.keys() and node[3] != '':
#                 crocNumber += float(node[3])
#     print("The croc number in the given points is:", crocNumber)
    
#     path = self.dijkstras(self) # calling dijkstras to find the shortest path between two location
#     newPath = []
   
#     for i in range(0, len(self.edge_list)-1):
#          if self.edge_list[i][0]==s1:
#             newPath.append(s1)  
                        
#     for i in range(0, len(path)-1):
#          if path[i]!=newPath[i]:
#             point=path[i-1]
#             break
#     return point   # return points to be blocked         
       
    
    
            
    
            
        
