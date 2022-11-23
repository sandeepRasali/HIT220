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


# find all cycles in the graph
# a cycle is a path that starts and ends at the same node
# we can use a dfs to find all the cycles
def cycles():
    graph = Graph().get_graph()
    cycles = []
    visited = []
    # we need to find out all the cycles in the graph
    # we do this by starting from each node and doing a dfs
    for node in range(1, len(graph)):
        if (node in visited):
            continue
        cycles_dfs(node, graph, cycles, visited, [])
    return cycles


def cycles_dfs(node, graph, cycles, visited, trace):

    if (node in visited):
        # if the node is already in the trace, then we have found a cycle
        # we add the cycle to the list of cycles
        if (node in trace):
            # get the start of the cycle
            trace_index = trace.index(node)
            cycle = []
            # add all the nodes in the cycle to the cycle list
            for i in range(trace_index, len(trace)):
                cycle.append(trace[i])
            # add the start node to the cycle list to make the path list like [1,2,3...,5,1] (a cycle)
            cycle.append(cycle[0])
            # add the cycle to the list of all cycles
            cycles.append(cycle)
            return
        return

    # add the current node to the visited list
   
    visited.append(node)
    # add the current node to the trace
  
    trace.append(node)

    # for each neighbour of the current node, we do a dfs
    for neighbour in graph[node]:
        cycles_dfs(neighbour, graph, cycles, visited, trace)
    trace.pop()


print("test cycles()")
print("cycles() -> ")
for cycle in cycles():
    print(cycle)
