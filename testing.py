import time
import networkx as nx
import pandas as pd
#from helper_functions import path_to_graph_name


def test_algorithms(graphs, algorithms):
    results = []
    for graph in graphs:
        for algorithm in algorithms:
            start = time.time()
            result = algorithm(graph)
            rez = len(result)
            end = time.time()
            results.append({"graph": graph, "algorithm": algorithm.__name__, "result": rez, "time": end-start})
    return pd.DataFrame(results)


if __name__ == "__main__":
    pass