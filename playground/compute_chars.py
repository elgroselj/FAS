import pandas as pd
import pickle
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
# import cugraph as nx
from networkx.algorithms import apx

db_name = "components.csv"
df = pd.read_csv(db_name)


def elementary_measures(l,name):
    p25, p50, p75 = np.percentile(l,[25, 50, 75])
    maxi = np.max(l)
    mini = np.min(l)
    d = {f"{name}_min":mini,
         f"{name}_max":maxi,
         f"{name}_p25":p25,
         f"{name}_p50":p50,
         f"{name}_p75":p75,
         }
    return d

cols = list(df.columns)
new_cols = None
for i in range(len(df)):
    if i % 1000 == 0:
        print(f"INFO: Working on {i}th row ...")
    
    row = df.iloc[i]    
    pickle_path = row["pickle_path"]
    with open(pickle_path, "rb") as f:
        G = pickle.load(f)
        assert nx.is_directed(G)
    
    d = {}
    
    if new_cols is None or "n" in new_cols:
        d["n"] = G.number_of_nodes()
    if new_cols is None or "m" in new_cols:
        d["m"] = G.number_of_edges()
    
    '''if new_cols is None or "parallel_edges" in new_cols:
        A= nx.adjacency_matrix(G)
        d["parallel_edges"] = len(np.where(A+A.T == 2))/2
    
    
    if new_cols is None or "density" in new_cols:
        d["density"] = nx.density(G)
    
    if new_cols is None or "planar" in new_cols:
        d["planar"] = nx.is_planar(G)
    
    if new_cols is None or "bipartite" in new_cols:
        d["bipartite"] = nx.is_bipartite(G)
        
    # if new_cols is None or "radius" in new_cols:
    #     ecc = nx.eccentricity(G)
    #     d["radius"] = np.min(ecc) #nx.radius(G)
    #     d["diameter"] = np.max(ecc) #nx.diameter(G)
        
    if new_cols is None or "radius" in new_cols:
        d["radius"] = nx.radius(G)
    if new_cols is None or "diameter" in new_cols:
        d["diameter"] = nx.diameter(G)
    
    # if new_cols is None or "diameter_LB" in new_cols:
    #     d["diameter_LB"] = apx.diameter(G)
        
    if new_cols is None or "node_connectivity" in new_cols:
        d["node_connectivity"] = nx.node_connectivity()
        # minimum number of nodes that must be removed to disconnect G
    
    # if new_cols is None or "node_connectivity_LB" in new_cols:
    #     d["node_connectivity_LB"] = apx.node_connectivity()
    #     # LB for minimum number of nodes that must be removed to disconnect G
    
    if new_cols is None or "degree_min" in new_cols:
        degrees = np.array([deg for n,deg in G.degree])
        d.update(elementary_measures(degrees,"degree"))'''
        
    
    
   
    # cycle_lengths = [len(c) for c in nx.simple_cycles(G)]
    # d.update(elementary_measures(cycle_lengths, "cycle_length"))
    
    # NAJVECJA SCC
    # ccs = list(nx.strongly_connected_components(G))
    # ccs_lengths = list(map(lambda x: len(x), ccs))
    # ind = np.argmax(ccs_lengths)
    # mcc_nodes = ccs[ind] # najvec vozlisc maximum connected component
    # mcc = nx.subgraph(G,mcc_nodes)
    
    
    # degrees = np.array([deg for n,deg in mcc.degree])
    # d.update(elementary_measures(degrees, "mcc_degree"))
    # # cycle_lengths = [len(c) for c in nx.simple_cycles(mcc)]
    # # d.update(elementary_measures(cycle_lengths, "mcc_cycle_length"))
    
    
    # TODO https://www.geeksforgeeks.org/number-of-triangles-in-directed-and-undirected-graphs/
    
    # se pozene le prvic
    if new_cols is None: 
        new_cols = []
        keys = list(d.keys())
        for key in keys:
            if key not in df.columns:
                df[key] = len(df) * [None]
                new_cols.append(key)
            df.iloc[i][key] = d[key]
    else:
        for col in new_cols:
            df.iloc[i][col] = d[col]
    

df.to_csv("chars2_" + db_name, index=False)