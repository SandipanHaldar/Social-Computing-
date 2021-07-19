
!pip install sent2vec
!pip install pandas
!pip install snap-stanford
!pip install scipy


import pandas as pd
from scipy import spatial
from sent2vec.vectorizer import Vectorizer
import snap
from sklearn.preprocessing import OrdinalEncoder


e=OrdinalEncoder()
df_label = pd.read_csv('label.txt', names=['labels'])
df_label["labels"] = df_label["labels"].astype('category')
df_label["label_cat"] = df_label["labels"].cat.codes
df = pd.read_csv('sentence.txt', names=['Sentence'])

def l2(l):
  return l[2]

def f(l):
  return l[1]

def makelist(d):
  l=[]
  for i in d:
    l.append([i,d[i]])
  return l  

def sort(l):
  return sorted(l,key=f,reverse=True) 


def findDistribution(N=0.3,length=1000,sampled=400):
  sentences = []
  for s in df['Sentence']:
    sentences.append(s)
    if(len(sentences)==length):
      break

  print("[INFO] No of sentences= "+str(len(sentences)))
  vectorizer = Vectorizer()
  vectorizer.bert(sentences)
  vectors_bert = vectorizer.vectors
  data=[]

  for i in range(length):
    for j in range(i+1,length):
      dist = spatial.distance.cosine(vectors_bert[i], vectors_bert[j])
      data.append([i+1,j+1,dist])
    if(((i+1)/length * 100)%10==0):
      print(str((i+1)/length * 100)+" % done")  
  data_sorted=sorted(data,key=l2,reverse=True) 

  G = snap.TUNGraph.New()
  for i in range(length):
    G.AddNode(i)

  val=int(length*N)
  for i in range (val):
    G.AddEdge(data_sorted[i][0],data_sorted[i][1]) 


  PRankH = G.GetPageRank()

  adj=dict()
  for i in G.Nodes():
    adj[i.GetId()]=[]

  for id in G.Nodes():
    i=id.GetId()
    for w in id.GetOutEdges():
      adj[i].append(w)

  pagerank=dict()
  for item in PRankH:
      pagerank[item]= PRankH[item]

  final=[]
  while(len(final)<sampled):
    pr_list=makelist(pagerank)
    pr_list=sort(pr_list)
    val=pr_list[0][0]
    for u in adj[val]:
      if u in pagerank:
        pagerank[u]*=0.8
    pagerank.pop(val)
    final.append(val) 

  counts=dict()
  for i in range(7):
    counts[i]=0
  for i in final:
    counts[df_label.iloc[i,1]]+=1

  return counts

print(findDistribution(length=2000,sampled=400))  
