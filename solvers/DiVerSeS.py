import os
import networkx as nx

def diverses(G,timeout=10):
    # naredimo line graph (prevedemo na problem FVS)
    with open("solvers/temp/line_graph_size.txt", "a") as f:
        f.write(f"{G.number_of_nodes()} {G.number_of_edges()} ")
        # print(f"INFO: Original graph size: n = {G.number_of_nodes()}, m = {G.number_of_edges()}")
        G = nx.line_graph(G)
        f.write(f"{G.number_of_nodes()} {G.number_of_edges()}\n")
        # print(f"INFO: Line graph size: n = {G.number_of_nodes()}, m = {G.number_of_edges()}")
    
    # vozlisca so naravna stevila
    G = nx.relabel_nodes(G,dict(zip(G,list(range(1, G.number_of_nodes()+1)))))

    
    with open("solvers/temp/input.txt", "w") as f:
        f.write(f"{G.number_of_nodes()} {G.number_of_edges()} 0")
        for line in nx.generate_adjlist(G):
            line = " ".join(line.split(" ")[1:])
            f.write("\n" + line)
    # pobirisemo output.txt
    open('solvers/temp/output.txt', 'w').close()

    # pozenemo FVS solver
    here = "/home/lema/Documents/aproks/FAS/solvers/"
    command = f"/home/lema/Documents/aproks/pace-2022/build/DiVerSeS --time-limit={timeout}000 < {here}temp/input.txt > {here}temp/output.txt 2>{here}temp/logs.err"

    os.system(command)

  
    
    with open("solvers/temp/output.txt", "r") as f:
        FVS_size = len(f.readlines())
        if FVS_size == 0:
            # sklepamo, da solver ni izpisal vmesne resitve po timeoutu
            print(f"WARNING: No intermediate solution given.")
            return None
    
    return FVS_size
        
    
# G = nx.DiGraph()
# G.add_edges_from([(1,2),(2,3),(3,1),(1,3),(3,2)])
# print(diverses(G))





