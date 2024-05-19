from pathlib import Path
import pandas as pd
import pickle
import networkx as nx

from helper_functions import read_graph_file, path_to_graph_name

# db_name = "graphs.csv"
db_name = "components.csv"

try:
    df = pd.read_csv(db_name)
    print(f"INFO: Openning an existing DB '{db_name}'.")
except FileNotFoundError:
    df = pd.DataFrame(columns=["graph_name","parent_name","source","pickle_path","opt_sum"])
    print(f"INFO: A new DB {db_name} was created.")

# parent je cel graf, graph je pa komponenta od parenta

paths = list(Path('data').rglob('*.al'))
paths += list(Path('data').rglob('*.d'))
for path_obj in paths:
    path = str(path_obj)
    parent_name = path_to_graph_name(path)
    
    if parent_name not in list(df["parent_name"]):
        # print(f"INFO: Reading {parent_name}")
        G, _, source, their_result = read_graph_file(path)
        sccs = nx.strongly_connected_components(G)
        for i, scc_nodes in enumerate(sccs):
            scc = nx.DiGraph(nx.subgraph(G,scc_nodes))
            graph_name = f"{parent_name}_{i}"
            pickle_path = f"pickles/{graph_name}.pickle"
        
            with open(pickle_path, "wb") as f:
                pickle.dump(scc, f) 
            
            df.loc[len(df)] = [graph_name,parent_name,source,pickle_path,their_result]
    else:
        print(f"INFO: Graph {parent_name} already in DB.")

df.to_csv(db_name, index=False)
print(f"INFO: A DB {db_name} was saved.")

    