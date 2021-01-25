#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 20 20:53:26 2020

@author: sandipan
"""
import snap
import random
import sys
Rnd = snap.TRnd(42)
Rnd.Randomize()

g = sys.argv[-1]
def mean(test_list):
    return round(sum(test_list) / len(test_list),4) 
def variance(test_list):
    m=mean(test_list)
    return round(sum((i - m) ** 2 for i in test_list) / len(test_list),4) 

G = snap.LoadEdgeList(snap.PUNGraph, "./Subgraphs/"+g, 0, 1)
#sec 1
node=G.GetNodes()
edge=G.GetEdges()
print ("Number of nodes: "+str(node))
print ("Number of edges: "+str(edge))
print ("Number of nodes with degree=7: "+str(snap.CntDegNodes(G, 7)))

#sec 2
InDegV = snap.TIntPrV()
snap.GetNodeInDegV(G, InDegV)
maxi=0
for item in InDegV:
	if maxi<item.GetVal2():
		maxi=item.GetVal2()
print("Node id(s) with highest degree:",end =" ")
for item in InDegV:
    if(item.GetVal2()==maxi):
        print(str(item.GetVal1()),end =" ")
snap.PlotInDegDistr(G, "deg_dist_"+g, "Undirected graph -degree Distribution")
print("\n",end = "")
#Sec 3
prod=10
diam=[]
while (prod<=1000):
    diag=snap.GetBfsFullDiam(G, prod, False)
    print("Approximate full diameter by sampling "+str(prod)+ " nodes: " + str(diag))
    prod*=10
    diam.append(diag)
print("Approximate full diameter (mean and variance): "+str(mean(diam))+","+str(variance(diam)))
prod=10
diam=[]
while (prod<=1000):
    diag=snap.GetBfsEffDiam(G, prod, False)
    print("Approximate Effective diameter by sampling "+str(prod)+ " nodes: " + str(round(diag,4)))
    prod*=10
    diam.append(diag)
print("Approximate Effective diameter (mean and variance): "+str(mean(diam))+","+str(variance(diam)))
snap.PlotShortPathDistr(G, "shortest_path_"+g, "Undirected graph - shortest path")

#Sec 4
#print("\n")
print('Fraction of nodes in largest connected component: ', round(snap.GetMxSccSz(G),4))
EV = snap.TIntPrV()
snap.GetEdgeBridges(G, EV)
print("Number of edge bridges: "+str(len(EV)))
AV = snap.TIntV()
snap.GetArtPoints(G, AV)
print("Number of articulation points: "+str(len(AV))) 
snap.PlotSccDistr(G, "connected_comp_"+g, "Undirected graph - scc distribution")

#Sec 5
#print("\n")
CC = snap.GetClustCf (G, -1)
print("Average clustering coefficient: %.4f" % CC)
T = snap.GetTriads(G)
print('Number of triads: %d' % T)
nodeid=G.GetRndNId(Rnd)
print("Clustering coefficient of random node %d: %.4f " % (nodeid,snap.GetNodeClustCf(G, nodeid)))
nodeid=G.GetRndNId(Rnd)
print("Number of triads random node %d participates: %d " % (nodeid,snap.GetNodeTriads(G, nodeid)))
z = snap.GetTriadEdges(G)
print("Number of edges that participate in at least one triad: "+str(z) )
snap.PlotClustCf(G, "clustering_coeff_"+g, "UnDirected graph - clustering coefficient")

files=[]
import os
os.remove("ccf.clustering_coeff_"+g+".plt")
os.remove("ccf.clustering_coeff_"+g+".tab")
os.rename("ccf.clustering_coeff_"+g+".png", "clustering_coeff_"+g+".png")
files.append("clustering_coeff_"+g+".png")
os.remove("diam.shortest_path_"+g+".tab")
os.remove("diam.shortest_path_"+g+".plt")
os.rename("diam.shortest_path_"+g+".png","shortest_path_"+g+".png")
files.append("shortest_path_"+g+".png")
os.remove("inDeg.deg_dist_"+g+".tab")
os.remove("inDeg.deg_dist_"+g+".plt")
os.rename("inDeg.deg_dist_"+g+".png","deg_dist_"+g+".png")
files.append("deg_dist_"+g+".png")
os.remove("scc.connected_comp_"+g+".tab")
os.remove("scc.connected_comp_"+g+".plt")
os.rename("scc.connected_comp_"+g+".png","connected_comp_"+g+".png")
files.append("connected_comp_"+g+".png")

import shutil
outpath = './Plots/'

for f in files:
    shutil.move(f,outpath+f)
