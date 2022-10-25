#Group 9



from typing import Sized
import csv
from collections import defaultdict
import numpy as np
import math

size=100

#************Creating a graph class to create undirected weighted-graph*************
class Graph():
    #function for edge and weight 
    def __init__(self):
        self.edges = defaultdict(list)
        self.weights = {}

    #function creating the weighted edge of a the graph
    def add_edge(self, source, destin, weight):
        self.edges[source].append(destin)
        self.edges[destin].append(source)
        self.weights[(source, destin)] = weight
        self.weights[(destin, source)] = weight
    #dijkstra function to calculate the route having minimun weight and no cycle
    def dijsktra(graph, currVertx, endVendvertx):
        # route hving minimum weight is a dictnary  of nodes
        # whose value is a tuple of (previous node, weight)
        shortest_paths = {currVertx: (None, 0)}
        present_node = currVertx
        # visited nodes
        reached = set()
        # loop to measure the paths 
        while present_node != endVendvertx:
            reached.add(present_node)
            destinations = graph.edges[present_node]
            present_nodeWight = shortest_paths[present_node][1]
            
            # loop checking separate paths that result minimum weighted edges
            for next_node in destinations:
                weight = graph.weights[(present_node, next_node)] + present_nodeWight
                if next_node not in shortest_paths:
                    shortest_paths[next_node] = (present_node, weight)
                else:
                    current_shortest_weight = shortest_paths[next_node][1]
                    if current_shortest_weight > weight:
                        shortest_paths[next_node] = (present_node, weight)
            
            next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in reached}
            if not next_destinations:
                return "Route Not Possible"
            # next node is the destination with the lowest weight
            present_node = min(next_destinations, key=lambda k: next_destinations[k][1])
        # Work back through destinations in shortest path
        shortpath = []
        while present_node is not None:
            shortpath.append(present_node)
            next_node = shortest_paths[present_node][0]
            present_node = next_node
        # Reversing the route
        path1 = shortpath[::-1]
        return path1
    
#function to perform depth first search  for given graph with specified vertex
def DFS(graph,start,end,path=[]): 
    path=path+[start] 
    if start==end:
        return path 
    paths = []
    for node in graph[start]:
        if node not in path:
            newpaths = DFS(graph,node,end,path)
            for newpath in newpaths:
                paths.append(newpath)
    return paths


class CrocMonitor:
    locationList =[]
    
    #list used for Question 3
    edgeList = []
    import csv
    def __init__(self, size):
        
        self.locationList = []
        self.matrix = []
        self.points=[]
        self.readData()
        self.storeDistance()

    def readData(self):
        with open('Locations.csv') as f:
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
        
        f.close()
    #function storing weight of data in 2-d arrays edgelist and self.matrix 
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

                                distance = self.computeDistance(startpoint, endpoint)
                                #storing in matrix
                                self.matrix.append([startpoint,endpoint,distance])
                                
                                #storing in edgelist
                                self.edgeList.append([startpoint, endpoint, distance, self.locationList[indexa][5]])

                          #store distance along path    
                                break
                        break
#*****************************Question1*************************************************
#Assumption : Finding all the routes that crock can take to travel between two location 
#and calculating the distance of all those route taking unit distance as usit cost
    
    #function calculating total distance of a route
    #Taking a list it calculated the path between each vertexs and sums the distance
    #using coordinate of those vertex
    def computePathDistance(self,path):
        Path_distance = 0       
        for indx in range(0,len(path)-1):
            start = path[indx]
            next= path[indx+1]
            a_path = self.computeDistance(start, next)
            Path_distance += a_path
        
        return Path_distance


    #finds the mimimum weight route between two points of a graph 
    def findPath(self,a,b):
        #calling graph function defined above
        graph = Graph()
        #taking the nodes from the self.matrix to a graph
        for nodes in self.matrix:
            graph.add_edge(*nodes)
        #taking Route of minimum weight between a and b 
        route = graph.dijsktra(a,b)   
        #calculating the path between a nad b    
        Path_len = cm.computePathDistance(route)        
        print("The shortest path between",a ,"and",b, "is",route, ' and have distance', Path_len )      
     
    #function calculatin distance between a and b reading data from locationList           
    def computeDistance (self, a, b):
        for index in range(0,size-1):
            try:
                
                if self.locationList[index][0] == a:
                    indexi=index
                if self.locationList[index][0]==b:
                    indexj=index
            except Exception:
                continue
        #Using pythagerous distance to calculate distance
        dis_x_axis =(int(self.locationList[indexi][1])-int(self.locationList[indexj][1]))
        dis_y_axis=(int(self.locationList[indexi][2])-int(self.locationList[indexj][2]))
        distance = (math.sqrt(((dis_x_axis)**2)+((dis_y_axis)**2)))
        return distance
        
        

    
#function that gives costing of the all the route between the point a and b 
    def computeCosting(self, a, b):
        #finding the edges between a and b to put as graph for Depth first search
        edges = {}
        for i in range(len(self.locationList)):
            if self.locationList[i][4] == '':
                edges[self.locationList[i][0]] = ''
            if self.locationList[i][4] != '':
                if self.locationList[i][0] not in edges:
                    edges[self.locationList[i][0]] = ([self.locationList[i][4]])
                else:
                    edges[self.locationList[i][0]].append(self.locationList[i][4]) 
    
        graph = edges
        path = DFS(graph,a,b)
        indexa = 0
        indexb = 1 
        #calculates the cost as distance of the route from DFS 
        cost = 0.00
        for i in range(len(path)):
            if indexb == (len(path)):
                break
            if path[indexa] < path[indexb]:
                cost = cost + (self.computeDistance((path[indexa]),(path[indexb])))
                indexa +=1
                indexb +=1
            elif path[indexa] > path[indexb]:
                indexa +=1
                indexb +=1
        cost = round(cost, 2)

        print('The minimum cost is', cost, 'for performing the exustive search between the locations', a, 'and', b, 'the path is' ,path)

################################Question2################################################################################################################   
    #Assumption: Finding the alternative routes and shortest route between two points
    #and calculationg their ratio Also finding blockage point 
    
    
    #function that gives the alternative path  and ratio of the path between 
    # a and b and shortest path a and b, also locates the optimallockage point   
    def improveDistance (self, a, b):
        point="A1"
        scaledImprovement=0
        path=[]
        first_point =a
        path.append(first_point)
        #loop to find the alternative paths between a and b from 2-d array
        for index in range(0, len(self.locationList)-1):
            if self.locationList[index][0]==first_point:
                first_point=self.locationList[index][4]
                for indexa in range(0, len(self.locationList)-1):
                    if self.locationList[indexa][0]==first_point:
                        last_point=self.locationList[indexa][4]
                        path.append(first_point)  
                        path.append(last_point)  
                if last_point==b:
                    break
        
        #calculating distance of the alternative route 
        path1=cm.computePathDistance(path)
        print("The Alternative path is", path,' and the alternative path distance is',path1)
        #calling graph and locating the minimum weight route between a and b
        graph = Graph()
        for nodes in self.matrix:
            graph.add_edge(*nodes)
        improvedPath = graph.dijsktra(a,b)
        
        #calculating the distance of the shortest route
        improvedPath_dist = cm.computePathDistance(improvedPath)
        print("The improved path is", improvedPath, 'and the improved path distance is',improvedPath_dist)
       
        scaledImprovement+=float(path1/improvedPath_dist)
        point=self.locateOptimalBlockage(a,b)
        print("\nThe blockage point is with protection is", point, 'and the ratio is',scaledImprovement)
           
    #function that locates the blockage point for the paths 
    def locateOptimalBlockage(self,a,b):
    # return the point blocked eg A1 and the increase in protection provided using some weighting
        
        protection=1
        path=[]
        first_point =a
        path.append(first_point)
        #finding the other possible routes
        for index in range(0, len(self.locationList)-1):
            if self.locationList[index][0]==first_point:
                first_point=self.locationList[index][4]
                for indexa in range(0, len(self.locationList)-1):
                    if self.locationList[indexa][0]==first_point:
                        last_point=self.locationList[indexa][4]
                        path.append(first_point)  
                        path.append(last_point)  
                if last_point==b:
                    break
        newpath=[]
        first_point=a
        #finding the point to block
        for index in range(0, len(self.locationList)-1):
            if self.locationList[index][0]==first_point:
                newpath.append(first_point)  
                first_point=self.locationList[index][4]
        for index in range(0, len(path)-1):
            if path[index]!=newpath[index]:
                point=path[index-1]
                break
        return point, protection
############################Question 3#########################################################
   
   ###Asumption finding find the minimum distance between two locations and hence time for
   # croc to travel that distance and also find the number of crock on the beach
   
    #function to count the crock in given beach
    def countCroc(self, beach, x):
        number=0
        beachIndex=0
        beachDistanceList = {}
        inRange = {}

        for index in range(0, len(self.locationList)):
            if self.locationList[index][0] == beach:
                beachIndex = index

        for i in range(0, len(self.locationList)):
            beachDistanceList[self.locationList[i][0]] = self.computeDistance1(beach, self.locationList[i][0],
                                                                                    beachIndex, i)

        for key in beachDistanceList:
            if beachDistanceList.get(key) <= x:
                inRange[key] = beachDistanceList.get(key)

        for node in self.locationList:
            if node[0] in inRange.keys() and node[3] != '':
                number += float(node[3])
        print("The croc number in the given points is:")
        return number
    
    #computing distance of path used in countcroc function
    def computeDistance1 (self, a, b, indexa, indexb):
        
        distance=0
        x1 = int(self.locationList[indexa][1])
        x2 = int(self.locationList[indexb][1])
        y1 = int(self.locationList[indexa][2])
        y2 = int(self.locationList[indexb][2])

        # using Euclidean to find distance and rounding it to 2 decimal places
        distance = round(np.sqrt((x1-x2)**2 + (y1-y2)**2), 2)
        return distance
    def minTime(self,a,b):
    #time is calculated in hours (i.e. 0.62 is 37 minutes)
    #return list of points trevelled and the time required
        path=[]
        totalTime=0
        graph = Graph1()

        for edge in self.edgeList:
            edge.append(self.calculateCrocTravelTime(edge[2], edge[3]))
            graph.add_edge(edge[0], edge[1], edge[4])

        #using Dijsktra1 to find the route of coc
        path = self.dijsktra1(graph, a, b)
        for index in range(0, len(path) - 1):
            totalTime += graph.weights[(path[index], path[index+1])]

        print("The minimum time to travel shortest route between ",a, "and" ,b,"is", {totalTime: path})

    #function calculating the croc travel time
    def calculateCrocTravelTime(self, d, isWater):
        travelTime=0
        crocSpeed=0

        if isWater:
            crocSpeed = 16
        else:
            crocSpeed = 6

        travelTime = d/crocSpeed
        return travelTime



    def findScope(self, a, b):
        #provide start and end point of search, collect points to consider in search
        pointList=[a,b]
          
        #find location of a and b in points list
        for index in range(0, size-1):
            if self.points[index ]== a:
                indexa=index
            if self.points[index] == b:
                indexb = index 
        
        return pointList

    def dijsktra1(self, graph, start, end):
        shortestPaths = {start: (None, 0)}
        currentNode = start
        visited = set()

        while currentNode != end:
            visited.add(currentNode)
            destinations = graph.edges[currentNode]
            weightToCurrentNode = shortestPaths[currentNode][1]

            for next in destinations:
                weight = graph.weights[(currentNode, next)] + weightToCurrentNode
                if next not in shortestPaths:
                    shortestPaths[next] = (currentNode, weight)
                else:
                    currentShortestWeight = shortestPaths[next][1]
                    if currentShortestWeight > weight:
                        shortestPaths[next] = (currentNode, weight)

            nextDestinations = {node: shortestPaths[node] for node in shortestPaths if node not in visited}
            if not nextDestinations:
                return "no possible route"
            currentNode = min(nextDestinations, key=lambda k: nextDestinations[k][1])

        path = []
        while currentNode is not None:
            path.append(currentNode)
            next = shortestPaths[currentNode][0]
            currentNode = next

        path = path[::-1]
        return path

class Graph1():
    def __init__(self):
        self.edges = defaultdict(list)
        self.weights = {}

    def add_edge(self, from_node, to_node, weight):
        # Note: assumes edges are bi-directional
        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)
        self.weights[(from_node, to_node)] = weight
        self.weights[(to_node, from_node)] = weight
if __name__ == '__main__':
    
    
    cm=CrocMonitor(size) 
    #print (cm.locationList)
    #Changed examples
    # cm.computeDistance("15","18")
    print("\n Question1:")
    cm.computeCosting("15","18")
    # cm.findPath("15", "18")
    # exhaustive path is  [15,16, 17,16, 18] so return the length of this as unit cost - note data changes in Locations.csv
    #algorithm to find scope of spanning tree is provided as findScope()
    print("\nQuestion 2:")
    cm.improveDistance("15","18")
    #output will be 16  Ratio is "original distance on [15,16,18]:0"
    cm.locateOptimalBlockage("15", "18")
    #returns 16 as other routes have alternative paths
    #may use other data to decide optimum path, but explain in requirements for this method
    print("\nQuestion 3")
    print(cm.countCroc('B6',10))
    cm.minTime("15", "18") 
    #returns [15,16,18] and time to travel that path