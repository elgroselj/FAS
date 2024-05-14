from pathlib import Path
import pandas as pd
import pickle

from helper_functions import read_graph_file, path_to_graph_name

db_name = "graphs.csv"

try:
    df = pd.read_csv(db_name)
    print(f"INFO: Openning an existing DB '{db_name}'.")
except FileNotFoundError:
    df = pd.DataFrame(columns=["graph_name","source","pickle_path","opt"])
    print(f"INFO: A new DB {db_name} was created.")

paths = list(Path('data').rglob('*.al'))
paths += list(Path('data').rglob('*.d'))
for path_obj in paths:
    path = str(path_obj)
    graph_name = path_to_graph_name(path)
    
    if graph_name not in list(df["graph_name"]):
        print(f"INFO: Reading {graph_name}")
        G, _, source, their_result = read_graph_file(path)
        pickle_path = f"pickles/{graph_name}.pickle"
        
        with open(pickle_path, "wb") as f:
            pickle.dump(G, f)
            
        df.loc[len(df)] = [graph_name,source,pickle_path,their_result]
    else:
        print(f"INFO: Graph {graph_name} already in DB.")

df.to_csv(db_name, index=False)
print(f"INFO: A DB {db_name} was saved.")

    