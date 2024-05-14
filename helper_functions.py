import networkx as nx
import re

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

# read_graph_file("/home/lema/Documents/aproks/FAS/data/FVScompetition/core/complete2.d")
            
    

    
    