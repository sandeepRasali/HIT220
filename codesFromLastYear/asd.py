from typing import Sized
import csv

import math
import numpy as np
size=100
class CrocMonitor:
    locationList =[]
    import csv
    def __init__(self, size):
        
        self.locationList = []
        self.matrix = [[0 for x in range(size)]for y in range(size)]
        self.points=[]
        self.readData()
        self.storeDistance()

    def readData(self):
        with open('Locations1.csv') as f:
            csv_reader = csv.reader(f)
            index = 0
            next(csv_reader)
            for line in csv_reader:
                
                pointName=line[0]
                x=line[1]
                y=line[2]
                number=line[3]
                edge=line[4]
                
                water=False
                if line[5] == "W":
                    water=True

                self.locationList .append( [pointName,  x, y, number, edge, water] ) # etc
                
                if not pointName in self.points:
                   
                    self.points.append(pointName)
                    
                index += 1
        #  print(self.locationList)
        # print("self point is",self.points)
        
        f.close()
       

    def storeDistance(self):
    
        for index in range(0, len(self.locationList)-1):
   
            if self.locationList[index][4]!="":
                startpoint = self.locationList[index][0]
                endpoint = self.locationList[index][4]
           
                for indexa in range (0, len(self.points)-1):
                    if self.points[indexa] == startpoint:
                        indexPointa=indexa
                
                        for indexb in range(0, len(self.points)-1):
                            if self.points[indexb] == endpoint:
                                indexPointb = indexb
                              
                                distance = self.computePathDistance(startpoint, endpoint)
                                self.matrix[indexPointa][indexPointb] = distance
                                self.matrix[indexPointb][indexPointa] = distance
                           #store distance along path    
                                break
                        break
        print(self.matrix)
        print(len(self.matrix))
   
      

    def computePathDistance (self,a,b):
        for index in range(0,size-1):
            if self.locationList[index][0] == a:
                indexa=index
            if self.locationList[index][0]==b:
                indexb=index
        point = a
        
        
       
    #     #provide the distance between two points a and b on a paths. Assume not adjacent
       
        
    #     # provide the distance between two points a and b on a path. Assume adjacent
       
         
    #     # for i in range (0,len(dist_cord)-1):
        
    
        
  

    def findPath(self,a,b):
        path=[]*size
        for index in range(0,size-1):
            if self.locationList[index][0] == a:
                indexa=index 
            if self.locationList[index][0]==b:
                indexb=index
        point = a
        while point!=b:
            point = self.locationList[indexa][4]
            path.append[a]
    #     #returns shortest path a to b
        return path
        
        
        
        
        

    def computePathDistance (self,a,b):
        for index in range(0,size-1):
            try:
                
                if self.locationList[index][0] == a:
                    i=index
                if self.locationList[index][0]==b:
                    j=index
            except Exception:
                continue
        dis_x_axis =(int(self.locationList[i][1])-int(self.locationList[j][1]))
        dis_y_axis=(int(self.locationList[i][2])-int(self.locationList[j][2]))
        distance = math.sqrt(((dis_x_axis)**2)+((dis_y_axis)**2))
        return distance
 

# Python3 program to find the shortest
# path between any two nodes using
# Floyd Warshall Algorithm.

# Initializing the distance and
# Next array
def initialise(V):
	global dis, Next

	for i in range(V):
		for j in range(V):
			dis[i][j] = graph[i][j]

			# No edge between node
			# i and j
			if (graph[i][j] == INF):
				Next[i][j] = -1
			else:
				Next[i][j] = j

# Function construct the shortest
# path between u and v
def constructPath(u, v):
	global graph, Next
	
	# If there's no path between
	# node u and v, simply return
	# an empty array
	if (Next[u][v] == -1):
		return {}

	# Storing the path in a vector
	path = [u]
	while (u != v):
		u = Next[u][v]
		path.append(u)

	return path

# Standard Floyd Warshall Algorithm
# with little modification Now if we find
# that dis[i][j] > dis[i][k] + dis[k][j]
# then we modify next[i][j] = next[i][k]
def floydWarshall(V):
	global dist, Next
	for k in range(V):
		for i in range(V):
			for j in range(V):
				
				# We cannot travel through
				# edge that doesn't exist
				if (dis[i][k] == INF or dis[k][j] == INF):
					continue
				if (dis[i][j] > dis[i][k] + dis[k][j]):
					dis[i][j] = dis[i][k] + dis[k][j]
					Next[i][j] = Next[i][k]

# Print the shortest path
def printPath(path):
	n = len(path)
	for i in range(n - 1):
		print(path[i], end=" -> ")
	print (path[n - 1])

# Driver code
if __name__ == '__main__':
	MAXM,INF = 100,10**7
	dis = [[-1 for i in range(MAXM)] for i in range(MAXM)]
	Next = [[-1 for i in range(MAXM)] for i in range(MAXM)]

	V = size
	graph = [ [ 0, 3, INF, 7 ],
			[ 8, 0, 2, INF ],
			[ 5, INF, 0, 1 ],
			[ 2, INF, INF, 0 ] ]

	# Function to initialise the
	# distance and Next array
	initialise(V)

	# Calling Floyd Warshall Algorithm,
	# this will update the shortest
	# distance as well as Next array
	floydWarshall(V)
	path = []

	# Path from node 1 to 3
	print("Shortest path from 1 to 3: ", end = "")
	path = constructPath(1, 3)
	printPath(path)

	# Path from node 0 to 2
	print("Shortest path from 0 to 2: ", end = "")
	path = constructPath(0, 2)
	printPath(path)

	# Path from node 3 to 2
	print("Shortest path from 3 to 2: ", end = "")
	path = constructPath(3, 2)
	printPath(path)

	# This code is contributed by mohit kumar 29
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        
#     def computeCosting(self, a, b):
#     # unit costs for scanning between two locations and give path for rangers to follow, returned as an array
#         path=[]
#         costing=0
#         return costing,path
    
#     def improveDistance (self, a, b):
#     #return point blocked as a value on map (eg A1) and scaled increase in distance between points
#         point="A1"
#         scaledImprovement=0
#         return point, scaledImprovement

#     def countCroc(self):
#     #count the number of crocs likely in a x mile radius of a beach. Return an array [location, number]
#         for index in range (0,size-1):
#             if self.locationList[index][0][:1]=="B":
#                 return self.locationList[index]
   

#     def locateOptimalBlockage(self,a,b):
#     # return the point blocked eg A1 and the increase in protection provided using another weighting
#         point="A1"
#         protection=1
#         return point, protection

#     def minTime(self,a,b):
#     #return array of points trevelled and the time required
#         path=[]
#         return path

# if __name__ == '_main_':
    
   
#     cm=CrocMonitor
#     print (cm.storeDistance())
#     print(cm.countCroc(5))
#     print(cm.computePathDistance(3,5))
#     print(cm.findPath("15", "18"))
    
    
#     print(cm.locateOptimalBlockage("15","18"))
#     #return 17 as other points have alternatives to bypass 
#     cm.computeCosting("15","18")
#     # minimal path is  [15,17,18] so return length of this as unit cost

#     cm.locateOptimalBlockage("15", "18")
#     #returns 17 as other routes have alternative paths
#     #may use other data to decide optimum path, but explain in requirements for this method