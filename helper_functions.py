import networkx as nx

def get_some_FAS(G, sort_mode="ain",dir_mode="f",plot=False,verbose=False):
    
    if verbose:
        print(f"INFO: Settings are: sort_mode = '{sort_mode}' and dir_mode = '{dir_mode}'.")
    
    assert sort_mode in ["ain", "din", "aout", "dout"]
    assert dir_mode in ["f","b"]
    

    def FAS_of_scc(H, sort_mode="ain",dir_mode="f",plot = False, verbose=False):

        degs = list(H.in_degree() if "in" in sort_mode else H.out_degree())
        degs.sort(key=lambda x: (x[1], x[0]),reverse="d" in sort_mode)
        node_order = [x[0] for x in degs]
        
        if dir_mode == "f":
            edges_b = [(v1,v2) for (v1, v2) in H.edges() if node_order.index(v1) > node_order.index(v2)]
            outE = edges_b
        elif dir_mode == "b":
            edges_f = [(v1,v2) for (v1, v2) in H.edges() if node_order.index(v1) < node_order.index(v2)]
            outE = edges_f
        
        # outE je F oz. "začasno" odstranjene povezave
        outE = edges_b if dir_mode == "f" else edges_f 
        
        K = nx.DiGraph(H)
        K.remove_edges_from(outE)
        FAS = set()
        
        def cycle(graph):
            try:
                c = nx.find_cycle(graph)
                return c
            except Exception:
                return None
        
        while len(outE) > 0:
            count = 0
            while count < len(outE):
                # en increment pointerja pride iz zamika pri pop,
                # drugi pa pri povečanja counterja uspešno dodanih povezav
                (v1, v2) = outE.pop(count)
                K.add_edge(v1,v2)
                c = cycle(K)
                if c is not None:
                    if verbose:
                        print(f"INFO: Cycle {c} emerged when edge {(v1,v2)} was added. Removed this edge.")
                    K.remove_edge(v1,v2)
                    FAS.add((v1,v2))
                else:
                    count += 1
                    
        if plot:
            nx.draw(H,with_labels=True,pos = nx.circular_layout(H),edge_color="tab:red")
            nx.draw(K,with_labels=True,pos = nx.circular_layout(K))
        return list(FAS)

    
    FAS = []

    for scc in nx.strongly_connected_components(G):
        FAS_ = FAS_of_scc(G.subgraph(scc), sort_mode=sort_mode,dir_mode=dir_mode,plot=plot,verbose=verbose)
        FAS = FAS + FAS_
    
    if verbose:
        print(f"INFO: {len(FAS)} out of {len(G.edges())} edges removed from the graph.")
    return FAS
        

    

    
    