from collections import deque

class EdgeInfo:
    def __init__(self, v, u, edge_id, forward, number_of_nodes):
        self.v = v
        self.u = u
        self.edge_id = edge_id
        self.forward = forward
        self.number_of_nodes = number_of_nodes

class FlowGraph:
    def __init__(self, number_of_nodes):
        self.adjacency_list = [[] for _ in range(number_of_nodes)]
        self.flow = []
        self.capacity = [] #for each edge

    def add_edge(self, v, u, c):
        self.adjacency_list[v].append(EdgeInfo(v, u, len(self.flow), True))
        self.adjacency_list[u].append(EdgeInfo(u, v, len(self.flow), False))
        self.flow.append(0)
        self.capacity.append(c)

    def add_flow(self, edge, flow):
        if edge.forward:
            self.flow[edge.edge_id] += flow
        else:
            self.flow[edge.edge_id] -= flow

    def left_over_capacity(self, edge): #how much is there on edge
        if edge.forward:
            return self.capacity[edge.edge_id] - self.flow[edge.edge_id]
        else:
            return self.flow[edge.edge_id]

    def traversable(self, edge):
        return self.left_over_capacity(edge) > 0

def BFS(graph, s, t): #it doesnt need to go through whole graph - just needs to reach t
    marked = [False for _ in range(graph.number_of_nodes)]
    edge_taken = [None for _ in range(graph.number_of_nodes)]
    marked[s] = True
    q = deque()
    q.append(s)
    while q:
        v = q.popleft()
        if v == t:
            break
        for edge in graph.adjacency_list[v]:
            if graph.traverable(edge) and not marked[edge.u]:
                marked[edge.u] = True
                edge_taken[edge.u] = edge
                q.append(edge.u)
    if edge_taken[t]:
        v = t
        path = []
        while edge_taken[v]:
            path.append(edge_taken[v])
            v = edge_taken[v].v
        return path
    return None

def edmonds(graph, s, t):
    while True:
        path = BFS(graph, s, t)
        if not path:
            break
        flow = graph.left_over_capacity(path[0])
        for edge in path:
            flow = min(flow, graph.left_over_capacity(edge))

        for edge in path:
            graph.add_flow(edge, flow)
    total_flow = 0
    for edge in graph.adjacency_list[s]:
        if edge.forward:
            total_flow += graph.flow[edge.edge_id]
    return total_flow


n = int(input())
m = int(input())


flow_graph = FlowGraph(n)


for _ in range(m):
    v, u, c = tuple(map(int, input().split()))
    flow_graph.add_edge(v, u, c)

print(edmonds(flow_graph, 0, 1))

