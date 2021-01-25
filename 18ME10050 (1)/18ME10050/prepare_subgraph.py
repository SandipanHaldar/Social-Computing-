# -*- coding: utf-8 -*-
"""
Spyder Editor
"""
import snap
G = snap.LoadEdgeList(snap.PUNGraph, "facebook_combined.txt", 0, 1)

NIdV = snap.TIntV()
for ni in G.Nodes():
    if ni.GetId()%5==0 :
    	NIdV.Add(ni.GetId())
snap.DelNodes(G, NIdV) 
snap.SaveEdgeList(G, './Subgraphs/facebook.elist')

G = snap.LoadEdgeList(snap.PUNGraph, "com-amazon.ungraph.txt", 0, 1)
NIdV = snap.TIntV()
for ni in G.Nodes():
    if ni.GetId()%4!=0 :
        NIdV.Add(ni.GetId())
snap.DelNodes(G, NIdV) 
snap.SaveEdgeList(G, './Subgraphs/amazon.elist')