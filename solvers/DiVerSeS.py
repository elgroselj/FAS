import os
import networkx as nx

def diverses(G):
    # naredimo line graph (prevedemo na problem FVS)
    G = nx.line_graph(G)
    
    # vozlisca so naravna stevila
    G = nx.relabel_nodes(G,dict(zip(G,list(range(1, G.number_of_nodes()+1)))))

    
    with open("solvers/temp/input.txt", "w") as f:
        f.write(f"{G.number_of_nodes()} {G.number_of_edges()} 0")
        for line in nx.generate_adjlist(G):
            f.write("\n" + line[2:])

    # pozenemo FVS solver
    here = "/home/lema/Documents/aproks/FAS/solvers/"
    os.system(f"/home/lema/Documents/aproks/pace-2022/build/DiVerSeS < {here}temp/input.txt > {here}temp/output.txt 2>{here}temp/logs.err")
    
    with open("solvers/temp/output.txt", "r") as f:
        FVS_size = len(f.readlines())
    
    return FVS_size
        
    
G = nx.DiGraph()
G.add_edges_from([(1,2),(2,3),(3,1),(1,3),(3,2)])
print(diverses(G))
