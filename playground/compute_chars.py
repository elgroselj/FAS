import pandas as pd
import pickle
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
# import cugraph as nx
from networkx.algorithms import approximation as apx

import sys
sys.path.append(".")
from timeout import timeout
from time import sleep



import sys
sys.path.append(".")
from solvers.lower_bound import LB
from helper_functions import repeat_max 

db_name = "3_2_1_components.csv"
# db_name = "components_small.csv"
df = pd.read_csv(db_name)

@timeout(1*60)
def to(lam):
    return lam()

def call(lam):
    try:
        res = to(lam)
        return res
    except Exception:
        print(f"WARNING: Timedout: {lam}")
        return None
        
    

def elementary_measures(l,name):
    if l is None:
        return {f"{name}_min":None,
         f"{name}_max":None,
         f"{name}_p25":None,
         f"{name}_p50":None,
         f"{name}_p75":None,
         }
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



MODE = 4
for i in range(len(df)):
    # if i % 1000 == 0:
    #     print(f"INFO: Working on {i}th row ...")
    print(f"INFO: Working on {i}th row ...")
    
    row = df.iloc[i]    
    pickle_path = row["pickle_path"]
    with open(pickle_path, "rb") as f:
        G = pickle.load(f)
        assert nx.is_directed(G)
        
    if G.number_of_nodes() <= 1:
        continue
    
    d = {}
    
    # 1
    if MODE == 1:
        if new_cols is None or "n" in new_cols:
            d["n"] = call(G.number_of_nodes)
            
        if new_cols is None or "m" in new_cols:
            d["m"] = call(G.number_of_edges)
        

        if new_cols is None or "density" in new_cols:
            d["density"] = call(lambda : nx.density(G))
        
        if new_cols is None or "planar" in new_cols:
            d["planar"] = call(lambda : nx.is_planar(G))
        
        if new_cols is None or "bipartite" in new_cols:
            d["bipartite"] = call(lambda : nx.is_bipartite(G))
            
            
        if new_cols is None or "radius" in new_cols:
            d["radius"] = call(lambda : nx.radius(G))
        if new_cols is None or "diameter" in new_cols:
            d["diameter"] = call(lambda : nx.diameter(G))
    


    # 2
    if MODE == 2:
        if new_cols is None or "node_connectivity" in new_cols:
            d["node_connectivity"] = call(lambda : nx.node_connectivity(G))
            # minimum number of nodes that must be removed to disconnect G
        
        if new_cols is None or "transitivity" in new_cols:
            d["transitivity"] = call(lambda : nx.transitivity(G))
            
        # cast v NEUSMERJEN graf
        if new_cols is None or "treewidth_min_fill_in" in new_cols:
            res = call(lambda : apx.treewidth_min_fill_in(nx.Graph(G)))
            d["treewidth_min_fill_in"] = None if res is None else res[0]
            
        if new_cols is None or "treewidth_min_degree" in new_cols:
            res = call(lambda : apx.treewidth_min_degree(nx.Graph(G)))
            d["treewidth_min_degree"] = None if res is None else res[0]
            
        
        
        
        
    # 3
    if MODE == 3:

        if new_cols is None or "degree_min" in new_cols:
            degrees = call(lambda : np.array([deg for n,deg in G.degree]))
            d.update(elementary_measures(degrees,"degree"))
            
        if new_cols is None or "closeness_centrality_min" in new_cols:
            vals = call(lambda : np.array([val for n,val in nx.closeness_centrality(G).items()]))
            d.update(elementary_measures(vals,"closeness_centrality"))
            
            
        if new_cols is None or "betweenness_centrality_min" in new_cols:
            vals = call(lambda : np.array([val for n,val in nx.betweenness_centrality(G).items()]))
            d.update(elementary_measures(vals,"betweenness_centrality"))
            
    
        
        if new_cols is None or "degree_centrality_min" in new_cols:
            vals = call(lambda : np.array([val for n,val in nx.degree_centrality(G).items()]))
            d.update(elementary_measures(vals,"degree_centrality"))
            

        
        if new_cols is None or "clustering_min" in new_cols:
            vals = call(lambda : np.array([val for n,val in nx.clustering(G).items()]))
            d.update(elementary_measures(vals,"clustering"))
            

            
        if new_cols is None or "katz_centrality_min" in new_cols:
            vals = call(lambda : np.array([val for n,val in nx.katz_centrality(G).items()]))
            d.update(elementary_measures(vals,"katz_centrality"))
        
        
        if new_cols is None or "pagerank_min" in new_cols:
            vals = call(lambda : np.array([val for n,val in nx.pagerank(G).items()]))
            d.update(elementary_measures(vals,"pagerank"))

        

        
    # 4
    if MODE == 4:
        if new_cols is None or "LB" in new_cols:
            d["LB"] = repeat_max(lambda: LB(G), 10)
    
    
    
    # se pozene le prvic
    if new_cols is None: 
        new_cols = []
        keys = list(d.keys())
        for key in keys:
            if key not in df.columns:
                df[key] = len(df) * [None]
                new_cols.append(key)
            # df.iloc[i][key] = d[key]
            df.at[i,key] = d[key]
    else:
        for col in new_cols:
            # df.iloc[i][col] = d[col]
            df.at[i,col] = d[col]
    

# df.to_csv("chars_" + db_name, index=False)
df.to_csv(f"{MODE}_" + db_name, index=False)