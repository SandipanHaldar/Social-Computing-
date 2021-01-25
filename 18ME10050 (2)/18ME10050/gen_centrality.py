#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 10:25:32 2020

@author: sandipan
"""

import snap
import json
G = snap.LoadEdgeList(snap.PUNGraph, "facebook_combined.txt", 0, 1)
#Closeness 
def Closness():
    cc=[]                                                                 #cc stores the Closeness Centrality for each node in the form of a pair
    for i in G.Nodes():
        NIdToDistH = snap.TIntH()
        tot=0
        shortestPath = snap.GetShortPath(G, i.GetId(), NIdToDistH)
        for j in NIdToDistH:
            tot+=NIdToDistH[j]                                            #tot is the sum of distance of every other node from node i
        cc.append([i.GetId(),(G.GetNodes()-1)/tot])  
    cc.sort(key=lambda x:x[1])
    cc.reverse()
    f=open("./centralities/closeness.txt","w")
    for item in cc:
        f.write(str(item[0])+" "+str(round(item[1],6))+"\n")               #Saving the list cc in the file in readable manner
    f.close()
    with open("cc.txt", "w") as fp:                                        #Saving the list cc
        json.dump(cc, fp)


def init(A,val):
    A.clear()
    for i in G.Nodes():
        if val==-99:
            A[i.GetId()]=[]                                                #This function initializes a dictionary to the given value
        else :
            A[i.GetId()]=val                                               #-99 indicates initialising an empty list for each key of the dict
    return A

#Betweeness Centrality using Brandes Algorithm
def Betweenness():
    d=dict()
    sig=dict()                                                            #d stores the distance of every node from the given node  
    P=dict()                                                              #sig is the sigma , Cb stores the betweenness Centrality
    Cb=dict()
    delta=dict()
    Cb=init(Cb,0)
    for Nid in G.Nodes():
        s=Nid.GetId()
        P=init(P,-99)
        sig=init(sig,0)
        sig[s]=1
        d=init(d,-1)
        d[s]=0
        S=[]
        Q=[]
        Q.append(s)
        while (len(Q)!=0):
            v=Q.pop(0)
            S.append(v)
            for w in G.GetNI(v).GetOutEdges():
                if(d[w]<0):
                    Q.append(w)
                    d[w]=d[v]+1
                if(d[w]==d[v]+1):
                    sig[w]=sig[w]+sig[v]
                    P[w].append(v)
        delta=init(delta,0)
        while (len(S)!=0):
            w=S.pop()
            for v in P[w]:
                delta[v]=delta[v]+(sig[v]/sig[w])*(1+delta[w])
            if(w!=s):
                Cb[w]=Cb[w]+delta[w] 
    bc=[]                                                               #bc stores the betweenness centrality for each node
    n=G.GetNodes()
    x=2/((n-1)*(n-2))               
    for Nid in G.Nodes():
        s=Nid.GetId()
        Cb[s]=Cb[s]*x 
        bc.append([s,Cb[s]])
    bc.sort(key=lambda x:x[1])
    bc.reverse()
    f=open("./centralities/betweenness.txt","w")
    for item in bc:
        f.write(str(item[0])+" "+str(round(item[1],6))+"\n")           #Saving the bc list in a text file
    f.close()
    with open("bc.txt", "w") as fp:
        json.dump(bc, fp)
    
    
#pagerank
def finddeg(u):
    c=0
    for v in G.GetNI(u).GetOutEdges():                                 #This functions finds the outdegree of a node u
        c+=1
    return c
def returnSum(myDict):      
    s = 0
    for i in myDict: 
        s = s + myDict[i]                                             #Finds the sum of values in a dictionary
    return s
def Pagerank():
    d=dict()
    cnt=0
    for i in G.Nodes():
        no=i.GetId()
        if( no%4==0):                                                #cnt is the total number of nodes with id%4==0
            cnt+=1
    for i in G.Nodes():
        no=i.GetId()
        if( no%4==0):
            d[no]=1/cnt                                              # biasing the preference vector   
        else:
            d[no]=0
    PR=dict()
    temp=dict()
    alpha=0.8
    e=1e-6
    itr=0
    for i in G.Nodes():
        u=i.GetId()
        PR[u]=d[u]
    while(itr<=3):
        temp.clear()
        temp=PR.copy()
        for i in G.Nodes():
            u=i.GetId()
            t=0
            for v in G.GetNI(u).GetOutEdges():
               t+=temp[v]/finddeg(v)
            temp[u]=alpha*t+(1-alpha)*d[u]
        f=1.0/returnSum(temp)
        for k in temp:
            temp[k] = temp[k]*f
        PR.clear()
        PR=temp.copy()
        itr+=1
    pr=[]                                                           # pr stores the pagerank of each nodes
    for Nid in G.Nodes():
        s=Nid.GetId()
        pr.append([s,PR[s]]) 
    pr.sort(key=lambda x:x[1])
    pr.reverse()  
    f=open("./centralities/pagerank.txt","w")
    for item in pr:
        f.write(str(item[0])+" "+str(round(item[1],6))+"\n")        #saving the pr list in a text file 
    f.close() 
    with open("pr.txt", "w") as fp:
        json.dump(pr, fp)
         
Closness()
Betweenness()
Pagerank()
   
        
        
        

               

    

       
        
    
    
    



