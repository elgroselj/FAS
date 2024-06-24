import networkx as nx
import re
import matplotlib.pyplot as plt
import numpy as np
import random

def path_to_graph_name(graph_file):
    graph_name = re.split('\ |/', graph_file)[-1]
    return graph_name
        
def read_graph_file(graph_file,verbose=True):
    
    graph_name = path_to_graph_name(graph_file)
            
    if graph_file[-3:] == ".al":
        # FASP-benchmarks format (adjency list)
        source = "FASP-benchmarks"
        G = nx.read_adjlist(graph_file,create_using=nx.DiGraph)
        
        their_result = None
        try:
            with open(graph_file[:-3] + ".mfas","r") as file:
                their_result = len(file.readlines())
        except FileNotFoundError:
            pass
                    
    elif "snap" in graph_file:
        # SNAP format
        # nodeId.edges : [...] The 'ego' node does not appear, but it is assumed that they follow every node id that appears in this file.
        # adding ego node edges in not needed, as ego node is not part of any strongly connected component anyway
        source = "snap"
        
        G = nx.DiGraph()
        with open(graph_file, "r") as file:
            if verbose:
                print("INFO: Reading and adding edges from file ...")
            while True:            
                line = file.readline()
                if len(line) == 0:
                    break
                v1, v2 = map(int, line.split(" "))
                G.add_edge(v1,v2)
            if verbose:
                print("INFO: Done reading and adding edges from file.")
                
        # no known results:
        their_result = None
        
    elif graph_file[-2:] == ".d":
        # DIMACS formar of FVS data
        source = "FVS_competition"
        
        G = nx.DiGraph()
        with open(graph_file,"r") as f:
            edge_num = int(f.readline().split(" ")[3])
            for e in range(edge_num):
                v1,v2 = map(int,f.readline().split(" ")[1:3])
                G.add_edge(v1,v2)
                
        # no known results:
        their_result = None
        
    else:
        raise Exception(f"Format '.{graph_file.split('.')[-1]}' not supported.")
    

    return G, graph_name, source, their_result

def draw_graph_with_FAS(G, edges_remove):
    edge_colors = []
    for u, v in G.edges():
        #print(u,v)
        if (u,v) in edges_remove:
            #print(u,v)
            edge_colors.append('r')
        else:
            edge_colors.append('b')
    nx.draw(G, edge_color=edge_colors, with_labels=True)
    plt.show()

def generate_random_DAG(n, m):
    G = nx.DiGraph()
    g = nx.DiGraph()

    G.add_nodes_from(range(n))
    G.name = "random_DAG(%s,%s)"%(n,m)

    if n==1:
        return G

    max_edges = n * (n-1)
	
    if m >= max_edges:
       return nx.complete_graph(n, create_using=G)
    
    nlist = list(G.nodes()) 
    edge_count = 0
    while edge_count < m:
		# generate random edge,u,v
        u = random.choice(nlist)
        v = random.choice(nlist)
        u, v = min(u,v), max(u,v)
        if u != v and not G.has_edge(u,v):
            #print(edge_count)
            G.add_edge(u,v)
            edge_count += 1
    
    #print(len(G.edges()))

    permutation = np.random.permutation(n)
    new_edges = []
    for e in G.edges():
        u,v = e 
        new_edges.append((permutation[u],permutation[v]))

    g.add_edges_from(new_edges)
    #assert nx.is_directed_acyclic_graph(g)
	#print("is_directed_acyclic_graph: %s" % nx.is_directed_acyclic_graph(g))
    return g

def add_cycle_edges_by_path(G, number_of_edges, path_length=5):
    number = 0
    num_nodes = G.number_of_nodes()
    nodes = list(G.nodes())
    extra_edges = []
    while number < number_of_edges:
        u, v = np.random.randint(0, num_nodes, 2)
        u = nodes[u]
        v = nodes[v]
        if nx.has_path(G,u,v):
            length = nx.shortest_path_length(G, source=u, target=v)
            if length <= path_length:
                extra_edges.append((v,u))
                number += 1
        if nx.has_path(G,v,u):
            length = nx.shortest_path_length(G, source=v, target=u)
            if length <= path_length:
                extra_edges.append((u,v))
                number += 1
	#print("# extra edges added with path length <= %d: %d" % (path_length,len(extra_edges)))
    return extra_edges

def add_extra_edges(G, number_of_edges):
    number = 0
    num_nodes = G.number_of_nodes()
    nodes = list(G.nodes())
    extra_edges = set()
    
    #paths = []
    edges_cycles = {}
    for e in G.edges():
        edges_cycles[e] = set()
    
    while len(extra_edges) < number_of_edges:
        u, v = np.random.randint(0, num_nodes, 2)
        u = nodes[u]
        v = nodes[v]
        if nx.has_path(G,u,v):
            if (v,u) not in extra_edges:
                path = nx.shortest_path(G, u, v)
                for i in range(len(path)):
                    pass#edges_cycles
                extra_edges.add((v,u))	
        if nx.has_path(G,v,u):
            if (u,v) not in extra_edges:
                extra_edges.add((u,v))
    extra_edges = list(extra_edges)
	#sprint("# extra edges added (path lenght unconstrainted): %d" % (len(extra_edges)))
    return extra_edges	

def add_cycle_edges(G, num_extra_edges, path_length = 1):
    if path_length == 1:
        edges = list(G.edges_iter())
        extra_edges_index = np.random.choice(len(edges),num_extra_edges)
        extra_edges = [(edges[index][1],edges[index][0]) for index in extra_edges_index]
        extra_edges = list(set(extra_edges))
        #print("# extra edges added by length = %d: %d" % (path_length,len(extra_edges)))
        return extra_edges
    else:
        return add_cycle_edges_by_path(G, num_extra_edges, path_length=path_length)

def introduce_cycles(G, num_extra_edges, path_length=0):
    if path_length <= 0:
		# no constraints on path length 
        edges = add_extra_edges(G, num_extra_edges)
    else:
		# path length >= 1
        edges = add_cycle_edges(G, num_extra_edges, path_length)
    G.add_edges_from(edges)

# read_graph_file("/home/lema/Documents/aproks/FAS/data/FVScompetition/core/complete2.d")
            
    
def repeat_max(fun_call,n):
    # example: repeat_max(lambda: LB(G), 5)
    maksi = None
    for i in range(n):
        val = fun_call()
        maksi = val if maksi is None or maksi < val else maksi
    return maksi


def run(edges, cycles_edges):
    edge = max(edges, key=edges.get)
    i = 0
    while i < len(cycles_edges):
        if edge in cycles_edges[i]:
            for e in cycles_edges[i]:
                if e != edge and e in edges:
                    edges.pop(e)
            del cycles_edges[i]
            i -= 1
        i += 1
    edges.pop(edge)
    return edges, cycles_edges, edge
                    


def gen_graph_DAG(n, m=None, c=None):
    # define random cycles
    cycles = []
    vertices_in_cycles = set()
    
    if c is None:
        c = random.randint(1, n)

    for i in range(c):
        # min length: 3
        cycle_length = random.randint(3, n//3)
        cycle = random.sample(range(n), cycle_length)
        cycle = sorted(cycle)
        if cycle not in cycles:
            cycles.append(cycle)
            vertices_in_cycles = vertices_in_cycles.union(set(cycle))
        else:
            i -= 1

    vertices_in_cycles = sorted(list(vertices_in_cycles))
    for i, v in enumerate(vertices_in_cycles):
        vertices_in_cycles[i] = i
        for cycle in cycles:
            if v in cycle:
                cycle[cycle.index(v)] = i
    
    # add random edges
    edges = []
    for u in range(n-1, len(vertices_in_cycles)-1, -1):
        added = []
        #a = random.randint(1, u)
        a = random.randint(1, 2)
        for i in range(a):
            v = random.randint(0, u-1)
            if v not in added:
                edges.append([u, v])
            else:
                i -= 1
    
    graph = nx.DiGraph()
    graph.name = f"random_DAG"
    graph.add_nodes_from(range(n))
    graph.add_edges_from(edges)
    for cycle in cycles:
        for i in range(len(cycle)):
            graph.add_edge(cycle[i], cycle[(i+1)%len(cycle)])
    
    return graph, cycles

#gen_graph(10, c=7)