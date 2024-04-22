import networkx as nx

graph = nx.DiGraph()

st = 10
with open("twitter_combined_sample.txt", "r") as f:
    v1, v2 = map(int, f.readline().split(" "))
    graph.add_edge(v1,v2)

nx.draw(graph)
    