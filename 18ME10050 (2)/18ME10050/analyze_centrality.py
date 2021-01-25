#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 19:31:42 2020

@author: sandipan
"""
import snap
import json
G = snap.LoadEdgeList(snap.PUNGraph, "facebook_combined.txt", 0, 1)

# Closeness using library
with open("cc.txt", "r") as fp:                                        #loading the cc list produced in the previous code 
    cc = json.load(fp)
cc1=[]
for NI in G.Nodes():
    CloseCentr = snap.GetClosenessCentr(G, NI.GetId())  
    cc1.append([NI.GetId(),CloseCentr])  
cc1.sort(key=lambda x:x[1])
cc1.reverse()
check=[]
cnt=0
for i in range(0,100):
    check.append(cc[i][0])
for i in range(0,100):
    if(cc1[i][0] in check):
        cnt+=1
print("#overlaps for Closeness Centrality: "+str(cnt))        

#Betweenness Centrality using Library
with open("bc.txt", "r") as fp:                                        #loading the bc list produced in the previous code 
    bc = json.load(fp)
bc1=[]
Nodes = snap.TIntFltH()
Edges = snap.TIntPrFltH()
snap.GetBetweennessCentr(G, Nodes, Edges, 0.8)
for node in Nodes:
    bc1.append([node, Nodes[node]])
bc1.sort(key=lambda x:x[1])
bc1.reverse()
check=[]
cnt=0
for i in range(0,100):
    check.append(bc[i][0])
for i in range(0,100):
    if(bc1[i][0] in check):
        cnt+=1
print("#overlaps for Betweenness Centrality: "+str(cnt)) 

#Pagerank calculation using snap
with open("pr.txt", "r") as fp:                                       #loading the pr list produced in the previous code 
    pr = json.load(fp)

pr1=[]
PRankH = snap.TIntFltH()
snap.GetPageRank(G, PRankH)
for item in PRankH:
    pr1.append([item, PRankH[item]])
pr1.sort(key=lambda x:x[1])
pr1.reverse()

check=[]
cnt=0
for i in range(0,100):
    check.append(pr[i][0])
for i in range(0,100):
    if(pr1[i][0] in check):
        cnt+=1
print("#overlaps for PageRank Centrality: "+str(cnt)) 
import os                                                            #removing unwanted files
os.remove("cc.txt")
os.remove("bc.txt")
os.remove("pr.txt")