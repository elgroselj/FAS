import pandas as pd
import pickle
import networkx as nx
from time import time
import sys

sys.path.append(".")
sys.path.append("../solvers")

from solvers.DiVerSeS import diverses
from solvers.exact import exact_with_wcnf
from solvers.italjani import get_some_FAS
from solvers.remove_cycle_edges_by_dfs import remove_edges_dfs
from solvers.remove_cycle_edges_by_minimum_feedback_arc_set_greedy import remove_edges_FAS_greedy
from solvers.remove_cycle_edges_by_minimum_feedback_arc_set_greedy_parallel import remove_edges_FAS_greedy_parallel
from solvers.remove_cycle_edges_by_hierarchy import remove_edges_hierarchy

from helper_functions import path_to_graph_name

db_name = "chars_components_small.csv"
df = pd.read_csv(db_name)

# example: run = wrap(get_some_FAS, 5), run(G): runs get_some_FAS(G) 5 times and returns the best result
def wrap(solver, n=5):
    """
    Wraps the solver function into a function that runs it n times and returns the best result.
    """
    def run_n_times(G):
        results = []
        for i in range(n):
            start  = time()
            sol = solver(G)
            stop = time()
            results.append((sol, stop - start))
        #return min(results, key = lambda t: t[0])
        r = min(results, key = lambda t: t[0])
        return (len(r[0]), r[1])
    return run_n_times

solvers_dict = {
    #"diverses": diverses,
    "italjani": wrap(get_some_FAS),
    "remove_edges_dfs": wrap(remove_edges_dfs),
    "remove_edges_FAS_greedy": wrap(remove_edges_FAS_greedy),
    "remove_edges_pagerank_scc_iteratively": wrap(lambda G: remove_edges_hierarchy(G, "pagerank", "scc_iteratively")),
    "remove_edges_trueskill_scc_iterativela": wrap(lambda G: remove_edges_hierarchy(G, "trueskill", "scc_iteratively")),
    "remove_edges_pagerank_BF_iterately_forward": wrap(lambda G: remove_edges_hierarchy(G, "pagerank", "BF_iterately_forward")),
    "remove_edges_trueskill_BF_iterately_forward": wrap(lambda G: remove_edges_hierarchy(G, "trueskill", "BF_iterately_forward")),
    "remove_edges_pagerank_BF_iterately_noforward": wrap(lambda G: remove_edges_hierarchy(G, "pagerank", "BF_iterately_noforward")),
    "remove_edges_trueskill_BF_iterately_noforward": wrap(lambda G: remove_edges_hierarchy(G, "trueskill", "BF_iterately_noforward")),
    "remove_edges_pagerank_voting": wrap(lambda G: remove_edges_hierarchy(G, "pagerank", "voting")),
    "remove_edges_trueskill_voting": wrap(lambda G: remove_edges_hierarchy(G, "trueskill", "voting")),
}


def solve(pickle_path,solver_name):
    solver = solvers_dict[solver_name]
    
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
#for solver_name in solvers_dict.keys():
for solver_name in solvers_dict.keys():
    print(solver_name)
    df[solver_name+"_sol"], df[solver_name+"_time"] = zip(*df["pickle_path"].map(lambda path: solve(path, solver_name)))



df.to_csv("solutions2_solvers_"+db_name,index=False)
