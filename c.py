import openpyxl


# define a class to represent a graph object

class Graph:

    def __init__(self):
        # read the data from the excel file
        wb = openpyxl.load_workbook('CrocData.xlsx')
        self.graph = [[] for i in range(0, 33)]
        # get the edges sheet
        sheet = wb['Edges']
        cell = sheet['D2:E44']
        for i in cell:
            # generate the graph
            self.graph[i[0].value].append(i[1].value)

    def get_graph(self):
        return self.graph


# find all paths between two points
def scheduled_points(start, end):
    graph = Graph().get_graph()
    paths = []
    scheduled_points_dfs(start, end, graph, [], paths)
    return paths


def scheduled_points_dfs(start, end, graph, trace, paths):
    # trace saves the nodes that have been visited so that we don't visit them again
   
    trace = trace + [start]
    # if the current node is the end node, then we have found a path
    if start == end:
        paths.append(trace)
    # else we check the neighbours of the current node
    for neighbours in graph[start]:
        if neighbours not in trace:
            scheduled_points_dfs(neighbours, end, graph, trace, paths)


print("test scheduled_points()")
start = input("Enter start point (Enter q to quit): ")
while start != 'q':
    end = input("Enter end point: ")
    print('scheduled_points({},{}) ->'.format(start, end))
    for path in scheduled_points(int(start), int(end)):
        print(path)
    start = input("Enter start point (Enter q to quit): ")
