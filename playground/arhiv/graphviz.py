import snap

G = snap.GenGrid(snap.PUNGraph, 5, 3)
G.DrawGViz(snap.gvlDot, "grid5x3.png", "Grid 5x3")