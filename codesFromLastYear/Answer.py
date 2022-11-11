
import csv
from collections import defaultdict
import math

size=100

# this class is for dijkstras algorithm, it will get called when 
# the user trys to find shortest path through the findPath() function in the crocMonitor class.
class Graph():

    def __init__(self):

        # uses default dict to store all possible neighbouring spots
        self.edges = defaultdict(list)
        # stores weighting or distance between points
        self.weights = {}

    # appends to self.edges
    def add_edge(self, from_node, to_node, weight):
        # assumes edges are bi-directional
        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)
        self.weights[(from_node, to_node)] = weight
        self.weights[(to_node, from_node)] = weight

    def dijsktra(graph, initial, end):
        # shortest paths is a dict of nodes
        # whose value is a tuple of (previous node, weight)
        shortest_paths = {initial: (None, 0)}
        current_node = initial
        # visited nodes
        visited = set()
        # while there are still nodes/edges to be measured
        while current_node != end:
            visited.add(current_node)
            destinations = graph.edges[current_node]
            weight_to_current_node = shortest_paths[current_node][1]
            # tests separate paths to find least weighted edges
            for next_node in destinations:
                weight = graph.weights[(current_node, next_node)] + weight_to_current_node
                if next_node not in shortest_paths:
                    shortest_paths[next_node] = (current_node, weight)
                else:
                    current_shortest_weight = shortest_paths[next_node][1]
                    if current_shortest_weight > weight:
                        shortest_paths[next_node] = (current_node, weight)
            
            next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}
            if not next_destinations:
                return "Route Not Possible"
            # next node is the destination with the lowest weight
            current_node = min(next_destinations, key=lambda k: next_destinations[k][1])
        # Work back through destinations in shortest path
        shortpath = []
        while current_node is not None:
            shortpath.append(current_node)
            next_node = shortest_paths[current_node][0]
            current_node = next_node
        # Reverse path
        path1 = shortpath[::-1]
        return path1

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
    import csv
    def __init__(self, size):
        
        self.locationList = []
        self.matrix = [[0 for x in range(size)]for y in range(size)]
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

                self.locationList.append( [pointName,  x, y, number, edge, water] ) # etc
                
                if not pointName in self.points:
                   
                    self.points.append(pointName)
                index += 1
        
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
                              
                                distance = self.computeDistance(startpoint, endpoint)
                           #store distance along path    
                                break
                        break


    def computePathDistanceQ1 (self,path,dist):     
    # Coded by Adam  
    #provide the distance between two points a and b, as the end points on a path. Assume not adjacent
        # baseline for distance
        kms=0
        # first point in shortest path list
        pointa = 0
        # second point in shortest path list
        pointb = 1  
        # loops through dist list which holds 2 croc spotting points and the distance in between         
        for y in range(len(dist)):
            # if pointb is the last node in list then break the loop
            if pointb == len(path):
                break 
            # makes sure the nodes are adjacent before adding the kms
            if path[pointa] == dist[y][0]:
                if path[pointb] == dist[y][1]:
                    # adds the distance between two nodes in shortest path 
                    kms = kms + dist[y][2]
                    # increment nodes in the shortest path list
                    pointa+=1
                    pointb+=1
        # returns the total distance from end nodes in shortest path
        return kms

    def computePathDistanceQ2 (self,path):
    # Coded by Ashish   
    #provide the distance between two points a and b, as the end points on a path. Assume not adjacent
        distance=0
        
        for i in range(0, len(path)-2):
            x=path[i]
            y=path[i+1]
            distance=self.computeDistanceQ2(x,y)
          
        return distance
    
    def findPathQ1(self,a,b):
    #Coded by Adam
    # this function will find the shortest path between two nodes
        # list - dist stores values of [0] croc spot location 1. [1] croc spot location 2. [2] distance in kms rounded to 2 decimal places.
        dist = []
        # loop through location list
        for i in range(len(self.locationList)):
            # makes sure node has a next neighbour
            if self.locationList[i][4]!="":
                # spot is orignal croc spot location
                spot = self.locationList[i][0]
                # x and y coordinate of node
                x = self.locationList[i][1]
                y = self.locationList[i][2]
                # next neighbouring node
                next = self.locationList[i][4]
                # loop through location list again to get coordinates of the neighbouring node
                for j in range(len(self.locationList)):
                    if self.locationList[j][0] == next:
                        # x and y coordinates of next node
                        xn = self.locationList[j][1]
                        yn = self.locationList[j][2]
                        # pythagoras theorem to find distance between nodes
                        a2 = (math.fabs(int(x) - (int(xn))))**2
                        b2 = (math.fabs(int(y)- (int(yn))))**2
                        # distance between nodes rounded to 2 decimals
                        distance = round(math.sqrt(a2 + b2),2)
                        # append the data to the list
                        dist.append([spot,next,distance]) 
        # next section calls graph class - dijstras algo 
        graph = Graph()
        for edge in dist:
            # calls add_edge in graph, adds the data (node1, node2, distance)
            graph.add_edge(*edge)
        # shortest path is result of this function
        path = graph.dijsktra(a,b)
        # shortest path total distance is result of this function
        kms = cm.computePathDistanceQ1(path,dist)
        # returns the shortest path and its total distance
        return f'The shortest route between {a} and {b} is {path} and the total distance is {kms}kms'

    def findPathQ2(self,a,b):
    # Coded by Ashish
        path=[]
        s1=a
        path.append(s1)
        for index in range(0, len(self.locationList)-1):
            if self.locationList[index][0]==s1:
                s1=self.locationList[index][4]
                for indexa in range(0, len(self.locationList)-1):
                    if self.locationList[indexa][0]==s1:
                        e1=self.locationList[indexa][4]
                        path.append(s1)  
                        path.append(e1)  
                if e1==b:
                    break
        print("The findpath2",path)       
                
        #returns shortest path a to b
        return path

    def computeDistance (self, a, b):      
    # Coded by Adam 
    # provide the distance between two points a and b on a path. Assume adjacent
        locations = {}
        for i in range(len(self.locationList)):
            # makes sure node has a next neighbour
            locations[self.locationList[i][0]] = ([self.locationList[i][1],self.locationList[i][2]])
        x = locations[a][0]
        y = locations[a][1]
        xn = locations[b][0]
        yn = locations [b][1]
        # pythagoras theorem to estimate distance
        a2 = (math.fabs(int(x) - (int(xn))))**2
        b2 = (math.fabs(int(y)- (int(yn))))**2
        distance = round(math.sqrt(a2 + b2),2)

        return distance

    def computeDistanceQ2 (self, a, b):
    # Coded by Ashish
    # provide the distance between two cordinatepoints a and b on a path. Assume adjacent  
        point1=[]
        point2=[]
        for index in range(0, len(self.locationList)-1):
   
            if self.locationList[index][0]==a and not point1:
                point1.append(self.locationList[index][1])
                point1.append(self.locationList[index][2])
            if self.locationList[index][0]==b and not point2:
                point2.append(self.locationList[index][1])
                point2.append(self.locationList[index][2])  
        distance=math.sqrt( ((int(point1[0])-int(point2[0]))**2)+((int(point1[1])-int(point2[1]))**2) )
        return distance    

    def computeCosting(self, a, b):
    # Coded by Adam
    # unit costs for scanning all points on all paths between two locations and give exhaustive path for rangers to follow, returned as an list
        edges = {}
        for i in range(len(self.locationList)):
            # makes sure node has a next neighbour
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
        costing = 0.00
        for i in range(len(path)):
            if indexb == (len(path)):
                break
            if path[indexa] < path[indexb]:
                costing = costing + (self.computeDistance((path[indexa]),(path[indexb])))
                indexa +=1
                indexb +=1
            elif path[indexa] > path[indexb]:
                indexa +=1
                indexb +=1
        costing = round(costing, 2)

        return f'The exhaustive cost is {costing}kms and the path is {path}'
    
    def improveDistance (self, a, b):
    # Coded by Ashish
    #return point blocked as a value on map (eg A1) and scaled increase in distance between points
        point="A1"
        scaledImprovement=0
        path=self.findPathQ2(a,b)
        print("The improved path", path)
        distance=self.computePathDistanceQ2(path)
        newpath=[]
        s1=a
        for index in range(0, len(self.locationList)-1):
            if self.locationList[index][0]==s1:
                newpath.append(s1)  
                s1=self.locationList[index][4]
        print("The newPath", newpath)
        newdistance=self.computePathDistanceQ2(newpath)
        scaledImprovement=newdistance/distance
        point=self.locateOptimalBlockage(a,b)
        return point, scaledImprovement

    def countCroc(self, beach, x):
    #count the number of crocs likely in a x mile radius of a beach. Return an array [location, number]
        number=0    #number of crocs in radius x of beach
        beachToCrocs = []
        for croc in self.points:
            if not "B" in croc and not "A" in croc and not "a" in croc:
                if cm.computeDistance(beach, croc)[0] <= x:
                    beachToCrocs.append(croc)
                    number +=float(self.locationList[int(croc)][3])

        #go through locationList & find closest neighbour to beach - block this point
        minDist = 1000
        blocked = '' 
        for location in self.locationList:
            if location[4] == beach:
                if location[5] < minDist:
                    minDist = location[5]
                    blocked = location[0]

        return number,blocked
            

    def locateOptimalBlockage(self,a,b):
    # Coded by Ashish
    # return the point blocked eg A1 and the increase in protection provided using some weighting
        point="A1"
        protection=1
        path=self.findPathQ2(a,b)
        newpath=[]
        s1=a
        for index in range(0, len(self.locationList)-1):
            if self.locationList[index][0]==s1:
                newpath.append(s1)  
                s1=self.locationList[index][4]
        for index in range(0, len(path)-1):
            if path[index]!=newpath[index]:
                point=path[index-1]
                break
        return point




    def minTime(self,a,b):
    #return list of points trevelled and the time required
        path=[]
        return path

if __name__ == '__main__':
   
    cm=CrocMonitor(size) 
    #print (cm.locationList)
    

    print('optimal blockage: ',cm.locateOptimalBlockage("15","18"))
    # this function is for finding the distance between two adjacent spots 
    # if the user enters non-neighbouring spots it will output direct distance between two points not measure through other points
    print('compute distance:',cm.computeDistance('15','18'))
    print('compute costing:',cm.computeCosting('15','18'))
 
 
    #return 17 as other points have alternatives to bypass 
    print('improve distance:',cm.improveDistance('15','18'))
    print("ASDFGHJKL",cm.locateOptimalBlockage('15','18'))

    # exhaustive path is  [15,16, 17,16, 18] so return length of this as unit cost - note data changes in Locations.csv
    # 8,10,16
    #returns 16 as other routes have alternative paths
    #may use other data to decide optimum path, but explain in requirements for this method
    print("ASDFG",cm.findPathQ1('15','18'))
