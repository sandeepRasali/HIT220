import csv

class CrocMonitor:
    def __init__(self):
        self.node_list = []

    def read_data(self):
        with open('CrocDataNodes.csv') as f:
            csv_reader = csv.reader(f)
            next(csv_reader)

            for line in csv_reader:
                node = int(line[0])
                x = float(line[1])
                y = float(line[2])
                water = bool(int(line[3]))
                sightings = int(line[4])

                self.node_list.append([node, x, y, water, sightings])
        
        f.close()

        return self.node_list
        
if __name__ == '__main__':
    cm = CrocMonitor() 
    print(cm.read_data())
