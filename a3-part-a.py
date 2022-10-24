import csv

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

# Merge Sort Algorithm adapted from https://www.geeksforgeeks.org/merge-sort/
def merge_sort_desc(array, sort_by_index: int):
    if len(array) > 1:
        mid = len(array) // 2 # midpoint
        left = array[:mid] # left half
        right = array[mid:] # right half

        merge_sort_desc(left, sort_by_index) # sort left half
        merge_sort_desc(right, sort_by_index) # sort right half

        i = j = k = 0 # iterators

        while i < len(left) and j < len(right):
            if left[i][sort_by_index] > right[j][sort_by_index]:
                array[k] = left[i]
                i += 1
            else:
                array[k] = right[j]
                j += 1
            k += 1

        while i < len(left):
            array[k] = left[i]
            i += 1
            k += 1
        
        while j < len(right):
            array[k] = right[j]
            j += 1
            k += 1

# Driver Code
if __name__ == '__main__':
    cm = CrocMonitor()
    cm.import_data('CrocDataNodes.csv')
    print("Original Data:")
    cm.read_data()

    test_sort = CrocMonitor()
    test_sort.import_data('CrocDataNodes.csv')
    merge_sort_desc(test_sort.node_list, 4)
    print("Sorted Data by Highest Sightings:")
    test_sort.read_data()