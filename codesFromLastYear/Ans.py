import numpy as np
import csv


#line[0] = location of crocodile
#line[1] =  X axis
#line[2] = Y axis
#line[3] = number of crocodiles
#line[4] = number of neighbours
#line[5]= water or land route
locationList=[]
#locationList=np.array([])
class CrocMonitor:

    
    def __init__(self):
        assert True
        #choose which one you want
        #self.locationList = []
        #self.locationList=np.array ([])

    def readData(self):
        with open('Locations.csv') as f:
            csv_reader = csv.reader(f)
            x=1
            for line in csv_reader:
                l=[]
                l=line[0],line[1],line[2],line[3],line[4],line[5]
                if(x==1):
                    x=0
                    continue #removing header on excel
                locationList.append(l)
                #print(l)
                #etc
        
        # locationList created
        
        #print(int(locationList[1][1]))
        f.close()
        
    def computeDistance (self, a, b):
                
        if a==b:
            return print("Location cannot be same")

        flag=-1
        for i in locationList:
            if (i[0]) == a:
                flag=1
                x1=i[1]
                y1=i[2]
                break
         
        if flag==-1:
            return print("invalid location a")
        #print("x1 ",x1,y1)
        flag=-1
        for i in locationList:
            if (i[0]) == b:
                flag=1
                x2=i[1]
                y2=i[2]
                break
        if flag==-1:
            return print("invalid location b")
        

        
            
        x1,y1,x2,y2=int(x1),int(y1),int(x2),int(y2)
        
        if x1==x2 and y1==y2:
            print("Distance cannot be adjacent")
            return 0
            
        #print("Distance between two points ",((x2-x1)**2+(y2-y1)**2)**0.5)
        return int(((x2-x1)**2+(y2-y1)**2)**0.5)
        # provide the distance between two points a and b on the paths. They may not be adjacent
    
    def computeCosting(self, a, b):
        
        # To compute Minimum Distance between two given location
        # Exhaustively iterate and find every neighbour location, from a given location, and add it to the resultant array
        
        result = []
        if a==b:
            return 0
        #find location A in the locationList
        flag=-1
        for i in range(0,len(locationList)):
            #print(locationList[i][0])
            if (locationList[i][0])==a:
                flag=1
                break
        
        if(flag==-1):
            print("Location not found A")
        else:
            x = i
        
        flag=-1
        for i in range(0,len(locationList)):
            if (locationList[i][0])==b:
                flag=1
                break
        
        if(flag==-1):
            print("Location not found B")
        else:
            y = i
        
        
        
        minDistance = 99999
        result.append(int(locationList[x][0]))
        for i in range(x,y):
        
            xaxis_i = int(locationList[i][1])
            yaxis_i = int(locationList[i][2])
            pos = -1
            for j in range(x+1,y):
                
                xaxis_j = int(locationList[j][1])
                yaxis_j = int(locationList[j][2])
                
                compute = ((xaxis_j-xaxis_i)**2 + (yaxis_j-yaxis_i)**2)**0.5
                if compute <=minDistance:
                    minDistance=compute
                    pos = j
                
            if pos !=-1:
                result.append(int(locationList[pos][0]))
        
        result=list(set(result))        
        return result
    # unit costs for scanning between two locations and give path for rangers to to follow, returned as an array
    
    def improveDistance (self, a, b):
        
        # To improve the Distance, find the optimal path and the exhaustive path from it's neighbour, and return the ratio of these.
        exhaustive_path = self.computeDistance(a,b)
        optimal_path = self.computeCosting(a,b)
        optimal_distance = 0
        
        initial = optimal_path[0]
        for i in range(1,len(optimal_path)):
            compute = self.computeDistance(initial,optimal_path[i])
            optimal_distance+=compute
            initial=i
        print(exhaustive_path/optimal_distance)
        return [exhaustive_path/optimal_distance,optimal_path]
        
        
    #return edge blocked as a duple (c,d) and scalled increase in distance between points
    
    def countCroc(self, beach):
        print("Number of crocodile in given region")
        print(locationList[beach-1][3])
        return locationList[beach-1][3]
    #count the number of crocs likely in a 10 mile radius of a beach. Return an array of locations and numbers
    
    
    
    def minTime(self,a,b):
        # To find the Optimal Path and time taken by the crocodile to travel
        # Finding the total OptimalPath
        # Finding the total Time taken on Land and Water = Average Time taken by crocodile on Land + Average Time taken by Crocodile on Water
        
        optimal_path = self.computeCosting(a,b)
        optimal_distance = 0
        time_land = 0
        time_water = 0
        initial = optimal_path[0]
        #print(locationList[0][5])
        # 1 unit on map represents 5 KM, hence calculating distance accordingly
        for i in range(1,len(optimal_path)):
            compute = self.computeDistance(initial,optimal_path[i])
            optimal_distance+=compute
            
            if locationList[i][5]=='W':
                time_water += int((compute*5)/16)
                #print(time_water)
            elif locationList[i][5]=='L':
                time_land += int((compute*5)/6)
                
            initial=i
            total_time = time_land+time_water
    #return array of points trevelled and the time required
        
        print(optimal_distance,total_time," hours")

p = CrocMonitor()

p.readData()
p.computeDistance("15","18")
p.computeCosting("15","18")
p.countCroc("15")
p.improveDistance("15","18")
p.minTime("15","18")