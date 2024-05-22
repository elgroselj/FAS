import random
import networkx as nx

def LB(G,verbose=False):
    edges = list(G.edges())
    random.shuffle(edges)
    
    H = nx.DiGraph()
    H.add_edges_from(edges)
    nodes = list(H.nodes())
    count = 0
    while True:
        try:
            node = random.sample(nodes,1)[0]
            cycle = nx.find_cycle(H,source=node)
            if verbose:
                print(cycle)
            H.remove_edges_from(cycle)
            count += 1
        except nx.exception.NetworkXNoCycle:
            # print(count)
            return count
        
# # G = nx.DiGraph(nx.cycle_graph(5))


# G = nx.DiGraph()
# G.add_edges_from([(1,2),(2,3),(3,1),(1,3)])

# G = nx.DiGraph()
# G.add_edges_from([(1,2),(2,1),(2,3),(1,3)])

# G = nx.DiGraph()
# G.add_edges_from([(1,2),(2,3),(3,2),(3,1),(1,3)])

# print(LB(G))

# import sys
# sys.path.append(".")
# from helper_functions import repeat_max
# print(repeat_max(lambda: LB(G), 5))

