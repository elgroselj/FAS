import pandas as pd
import pickle
import networkx as nx
from time import time
import sys
sys.path.append(".")

from solvers.DiVerSeS import diverses
from helper_functions import path_to_graph_name

db_name = "chars_components_small.csv"
df = pd.read_csv(db_name)


def solve(pickle_path,solver_name):
    solver = {
        "diverses": diverses
        # tukaj dodaj svoj solver "ime":funkcija
        }[solver_name]
    
    print(f"INFO: Solving FAS for graph {path_to_graph_name(pickle_path)}")
    
    with open(pickle_path,"rb") as f:
        G = pickle.load(f)
        
    if G.number_of_edges() in [0, 1]:
        return 0, 0
    
    start  = time()
    sol = solver(G)
    stop = time()
    return sol, stop - start


# tu pozenemo solverje
for solver_name in ["diverses"]:
    df[solver_name+"_sol"], df[solver_name+"_time"] = zip(*df["pickle_path"].map(lambda path: solve(path, solver_name)))



df.to_csv("solvers_"+db_name,index=False)
