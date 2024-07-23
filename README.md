# Influence of Graph Characteristics on Solutions of Feedback Arc Set Problem

This code is a companion of an article Influence of Graph Characteristics on Solutions of Feedback Arc Set Problem by Tomaž Poljanšek and Ema Leila Grošelj. In this article we present Feedback Arc Set problem and how certain graph characteristics impact results of heuristic algorithms. We then inspect how the most promising characteristic (treewidth) helps in choosing the most appropriate heuristics for our graph.

Project structure:
- data = supposed to contain test data (graphs)
    - v FASP-benchmarks/data there is a readme about the files
    - graph-benchmarks
    - snap (real networks == large)

    - we unify all these formats by collecting them in one database graphs.csv and their pickle files in the pickles folder (1. create the pickles folder, 2. run construct_db_components.py)

- playground = space for trying things out
- solvers = implementations
- helper_functions.py = helper functions
- NOTES.md = notes on sources, etc.
