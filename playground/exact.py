from random import sample 
import cvxpy as cp
import numpy as np
import networkx as nx
import pandas as pd
import datetime
from functools import cache

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
    
# g = nx.DiGraph()
# g.add_edges_from([("1","kjvgakjb"),("kjvgakjb",3),(3,"1")])
# print(din(g))

# g = nx.cycle_graph(3)
# g = nx.DiGraph(g)
# print(din(g))