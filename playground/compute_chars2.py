import pandas as pd
import pickle
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
# import cugraph as nx
#from networkx.algorithms import apx

db_name = "chars2_components.csv"
df = pd.read_csv(db_name)

print("n ...")
for i, line in enumerate(df.iterrows()):
    if i % 100 == 0:
        print(f"INFO: Working on {i}th row ...")
    row = line[1]
    pickle_path = row["pickle_path"]
    with open(pickle_path, "rb") as f:
        G = pickle.load(f)
        #assert nx.is_directed(G)
        df.at[line[0], "m"] = G.number_of_edges()

#df["n"] = df.apply(lambda row: nx.number_of_nodes(pickle.load(row["pickle_path"])), axis=1)
'''print("m ...")
df["m"] = df.apply(lambda row: nx.number_of_edges(pickle.load(row["pickle_path"])), axis=1)
print("closeness centrality ...")
df["closeness_centrality"] = df.apply(lambda row: nx.closeness_centrality(nx.read_pickle(row["pickle_path"])), axis=1)
print("betweenness centrality ...")
df["betweenness_centrality"] = df.apply(lambda row: nx.betweenness_centrality(nx.read_pickle(row["pickle_path"])), axis=1)
print("degree centrality ...")
df["degree_centrality"] = df.apply(lambda row: nx.degree_centrality(nx.read_pickle(row["pickle_path"])), axis=1)
print("eigenvector centrality ...")
df["eigenvector_centrality"] = df.apply(lambda row: nx.eigenvector_centrality(nx.read_pickle(row["pickle_path"])), axis=1)
print("clustering ...")
df["clustering"] = df.apply(lambda row: nx.clustering(nx.read_pickle(row["pickle_path"])), axis=1)
print("average clustering ...")
df["average_clustering"] = df.apply(lambda row: nx.average_clustering(nx.read_pickle(row["pickle_path"])), axis=1)
print("transitivity ...")
df["transitivity"] = df.apply(lambda row: nx.transitivity(nx.read_pickle(row["pickle_path"])), axis=1)
print("katz centrality ...")
df["katz_centrality"] = df.apply(lambda row: nx.katz_centrality(nx.read_pickle(row["pickle_path"])), axis=1)
print("pagerank ...")
df["pagerank"] = df.apply(lambda row: nx.pagerank(nx.read_pickle(row["pickle_path"])), axis=1)'''

df.to_csv("chars3_components.csv", index=False)