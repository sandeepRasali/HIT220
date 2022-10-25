import csv

import math
import numpy as np
size= 50
class CrocMonitor:
    nodeList =[]
    import csv
    def __init__(self, size):
        
        self.nodeList = []
        self.matrix = [[0 for x in range(size)]for y in range(size)]
        self.points=[]
        self.readData()

    def readData(self):
        with open('CrocData.csv') as f:
            csv_reader = csv.reader(f)
            index = 0
            next(csv_reader)
            for line in csv_reader:
                
                node=line[0]
                x=line[1]
                y=line[2]              
             
                
                water= 1
                if line[3] == "0":
                    water= 0

                self.nodeList .append( [node, x, y, water] ) # etc
                
                if not node in self.points:
                   
                    self.points.append(node)
                index += 1
        
        f.close()
        
        
        
if __name__ == '__main__':
   
    cm=CrocMonitor(size) 
    print (cm.nodeList)
        
