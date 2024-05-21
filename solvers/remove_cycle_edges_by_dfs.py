import networkx as nx 
import argparse
import numpy as np
#from measures import F1	# from original code

import sys
sys.setrecursionlimit(5500000)

def dfs_visit_recursively(g,node,nodes_color,edges_to_be_removed):

	nodes_color[node] = 1
	nodes_order = list(g.successors(node))
	nodes_order = np.random.permutation(nodes_order)
	for child in nodes_order:
		if nodes_color[child] == 0:
				dfs_visit_recursively(g,child,nodes_color,edges_to_be_removed)
		elif nodes_color[child] == 1:
			edges_to_be_removed.append((node,child))

	nodes_color[node] = 2

def dfs_remove_back_edges(g):
	'''
	0: white, not visited 
	1: grey, being visited
	2: black, already visited
	'''

	nodes_color = {}
	edges_to_be_removed = []
	for node in list(g.nodes()):
		nodes_color[node] = 0

	nodes_order = list(g.nodes())
	nodes_order = np.random.permutation(nodes_order)
	num_dfs = 0
	for node in nodes_order:

		if nodes_color[node] == 0:
			num_dfs += 1
			dfs_visit_recursively(g,node,nodes_color,edges_to_be_removed)

	#print("number of nodes to start dfs: %d" % num_dfs)
	#print("number of back edges: %d" % len(edges_to_be_removed))

	return edges_to_be_removed



def remove_edges_dfs(G):
	'''
	DFS Remove Back Edges
	'''

	edges_to_be_removed = dfs_remove_back_edges(G)
	return edges_to_be_removed
	
