import pandas as pd
import pickle
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
# import cugraph as nx

db_name = "graphs.csv"
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
for i in range(len(df)):
    print(f"INFO: Working on {i}th row ...")
    # for row in df.iterrows():
    row = df.iloc[i]    
    pickle_path = row["pickle_path"]
    with open(pickle_path, "rb") as f:
        G = pickle.load(f)
    # print(list(graph.nodes()))
    # nx.draw(graph)
    # plt.show()
    print("*1")
    d = {}
    
    d["n"] = G.number_of_nodes()
    d["m"] = G.number_of_edges()
    assert nx.is_directed(G)
    
    print("*2")
    degrees = np.array([deg for n,deg in G.degree])
    # degree_min, degree_max, degree_p25, degree_p50, degree_p75 = elementary_measures(degrees)
    d.update(elementary_measures(degrees,"degree"))
    
    # print("*")
    # cycle_lengths = [len(c) for c in nx.simple_cycles(G)]
    # # cycle_length_min, cycle_length_max, cycle_length_p25, cycle_length_p50, cycle_length_p75 = elementary_measures(cycle_lengths)
    # d.update(elementary_measures(cycle_lengths, "cycle_length"))
    
    print("*3")
    ccs = list(nx.strongly_connected_components(G))
    ccs_lengths = list(map(lambda x: len(x), ccs))
    ind = np.argmax(ccs_lengths)
    mcc_nodes = ccs[ind] # najvec vozlisc maximum connected component
    mcc = nx.subgraph(G,mcc_nodes)
    print("*4")
    degrees = np.array([deg for n,deg in mcc.degree])
    d.update(elementary_measures(degrees, "mcc_degree"))
    # mcc_degree_min, mcc_degree_max, mcc_degree_p25, mcc_degree_p50, mcc_degree_p75 = elementary_measures(degrees)
    # print("*5")
    # cycle_lengths = [len(c) for c in nx.simple_cycles(mcc)]
    # print(cycle_lengths)
    # # mcc_cycle_length_min, mcc_cycle_length_max, mcc_cycle_length_p25, mcc_cycle_length_p50, mcc_cycle_length_p75 = elementary_measures(cycle_lengths)
    # d.update(elementary_measures(cycle_lengths, "mcc_cycle_length"))
    # TODO https://www.geeksforgeeks.org/number-of-triangles-in-directed-and-undirected-graphs/
    print("*6")
    
    new_cols = list(d.keys())
    for col in new_cols:
        if col not in df.columns:
            df[col] = len(df) * [None]
        df.iloc[i][col] = d[col]
    print("*7")
    

df.to_csv("chars_"+db_name, index=False)