from pathlib import Path
import pandas as pd
import pickle

from helper_functions import read_graph_file, path_to_graph_name

db_name = "graphs.csv"


# df = pd.DataFrame(columns=["graph_name","source","pickle_path","opt"])
df = pd.read_csv(db_name)


for path_obj in Path('data').rglob('*.al'):
    path = str(path_obj)
    graph_name = path_to_graph_name(path)
    # if graph_name not in df["graph_name"]:
    if True:
        print(f"INFO: Reading {graph_name}")
        G, graph_name2, source, their_result = read_graph_file(path)
        assert graph_name == graph_name2
        pickle_path = f"pickles/{graph_name}.pickle"
        with open(pickle_path, "wb") as f:
            pickle.dump(G, f)
        df.loc[len(df)] = [graph_name,source,pickle_path,their_result]
    else:
        print(f"INFO: Graph {graph_name} already in DB.")

df.to_csv(db_name)

    