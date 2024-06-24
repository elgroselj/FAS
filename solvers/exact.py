import networkx as nx
from functools import cache
from pysat.examples.rc2 import RC2
from pysat.formula import WCNF

@cache
def sub(G):
    # print(len(G.edges()))s
    cycles_nodes = list(nx.simple_cycles(G))
    
    if len(cycles_nodes) == 0:
        return list(G.edges)
    
    
    cycles = []
    for cycle in cycles_nodes:
        new_cycle = [(cycle[-1],cycle[0])]
        for arc in zip(cycle[:-1],cycle[1:]):
            new_cycle.append(arc)
        cycles.append(new_cycle)
    
    best = None
    for cycle in cycles:
        for arc in cycle:
            G.remove_edge(*arc)
            sol = sub(G)
            if best is None or len(best) < len(sol):
                best = sol
            G.add_edge(*arc)
    return best

# g = nx.cycle_graph(3)
# g = nx.DiGraph(g)

# g = nx.DiGraph()
# g.add_edges_from([(1,2),(2,3),(3,1)])
# print(din(g))

def din(G):
    mapping = {node: i for i, node in zip(range(len(G.nodes())), G.nodes())}
    G = nx.relabel_nodes(G, mapping)
    
    remainder = sub(G)
    
    FAS = set(G.edges()).difference(remainder)
    
    
    inv_mapping = {v: k for k,v in mapping.items()}
    G = nx.relabel_nodes(G, inv_mapping)
    
    FAS = [(inv_mapping[v1], inv_mapping[v2]) for (v1,v2) in FAS]
    
    return FAS


def exact_with_wcnf(graph, cycles=None):
    if cycles is None:
        cycles = list(nx.simple_cycles(graph))
    n = graph.number_of_nodes()
    #print(cycles)

    wcnf = WCNF()
    m = 0
    remove = []

    for cycle in cycles:
        arr = list(map(int, cycle))
        add = []
        for i in range(len(arr)):
            x, y = arr[i], arr[(i+1)%len(arr)]
            index = n*x + y
            add.append(index)
            m = max(m, index)
        wcnf.append(add)

    # minimize number of edges needed to remove
    for i in range(1, m+1):
        wcnf.append([-i], weight=1)

    sol_g = RC2(wcnf)
    #print(sol_g.compute())
    opt = next(sol_g.enumerate())

    for edge in opt:
        if edge > 0:
            #y = n if (edge) % n == 0 else (edge) % n   # previous graph generation
            y = edge % n        # new graph generation
            x = (edge - y) // n
            #print('removing edge {0} {1}'.format(x, y))
            remove.append((str(x), str(y)))
    
    return remove
    
# g = nx.DiGraph()
# g.add_edges_from([("1","kjvgakjb"),("kjvgakjb",3),(3,"1")])
# print(din(g))

# g = nx.cycle_graph(3)
# g = nx.DiGraph(g)
# print(din(g))