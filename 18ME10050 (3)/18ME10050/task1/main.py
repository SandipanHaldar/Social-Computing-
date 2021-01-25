#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 18:47:31 2020

@author: sandipan
"""
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import csv
import string
from sklearn.ensemble import RandomForestClassifier
from gensim.models import Word2Vec 
import numpy as np
from sklearn.svm import SVC
import fasttext
 
def preprocess(words):
    words = [''.join(c for c in s if c not in string.punctuation) for s in words]
    words = [s for s in words if s]
    words = [w.lower() for w in words]
    
    final=""
    for w in words:
        final+=w+" "
    return final


    
#randomforest classifier

vectorizer = TfidfVectorizer(max_df=0.8,min_df=0.05)
df=pd.read_csv('../data/processed_data_train.csv',sep='\t')
df=df.dropna()
L=df['text'].tolist()

vectors = vectorizer.fit_transform(L)
feature_names = vectorizer.get_feature_names()
n_features=len(feature_names)
dense = vectors.todense()
X_train = dense.tolist()
y_train= df['hateful'].tolist()

vectorizer = TfidfVectorizer(max_df=0.8,min_df=0.05,max_features=n_features)
df=pd.read_csv('../data/processed_data_test.csv',sep='\t')
df=df.dropna()
L=df['text'].tolist()
vectors = vectorizer.fit_transform(L)
feature_names = vectorizer.get_feature_names()
dense = vectors.todense()
X_test = dense.tolist()

clf = RandomForestClassifier()
clf.fit(X_train, y_train)
y_pred=clf.predict(X_test)

row=[]
for i in range(len(df)):
    rr=[]
    rr.append(df['id'][i])
    rr.append(y_pred[i])
    row.append(rr)
with open("../predictions/RF.csv",'w') as f:
    csvwriter=csv.writer(f)
    csvwriter.writerow(['id','hateful'])
    csvwriter.writerows(row)
    
 
    
    
#SVM classifier   
  
df=pd.read_csv('../data/processed_data_train.csv',sep='\t')
df=df.dropna()
L_train=df['text'].tolist()
y_train= df['hateful'].tolist()

df=pd.read_csv('../data/processed_data_test.csv',sep='\t')
df=df.dropna()
L_test=df['text'].tolist()

words=[]
for s in L_train:
    w=s.split()
    words.append(w)
for s in L_test:
    w=s.split()
    words.append(w)
    
model1 = Word2Vec(words, min_count = 1,  size = 100, window = 5)     
X_train=[]
X_test=[]

for s in L_train:
    w=s.split()
    features=np.zeros(100)
    for i in w:
        features=np.add(features,np.array(model1.wv[i]))
    features/=(len(w)+1e-6)
    X_train.append(features)
    
    
for s in L_test:
    w=s.split()
    features=np.zeros(100)
    for i in w:
        features=np.add(features,np.array(model1.wv[i]))
    features/=(len(w)+1e-6)
    X_test.append(features)

clf=SVC(kernel='rbf')
clf.fit(X_train,y_train)
y_pred=clf.predict(X_test)

row=[]
for i in range(len(df)):
    rr=[]
    rr.append(df['id'][i])
    rr.append(y_pred[i])
    row.append(rr)
with open("../predictions/SVM.csv",'w') as f:
    csvwriter=csv.writer(f)
    csvwriter.writerow(['id','hateful'])
    csvwriter.writerows(row)
    

#fasttrack model 

df=pd.read_csv('../data/processed_data_train.csv',sep='\t')
df=df.dropna()
L=df['text'].tolist()
with open('fasttext_input.txt', 'w') as f:
    for each_text, each_label in zip(df['text'], df['hateful']):
        f.writelines(f'__label__{each_label} {each_text}\n')

model = fasttext.train_supervised('fasttext_input.txt', wordNgrams=2)
df=pd.read_csv('../data/processed_data_test.csv',sep='\t')
df=df.dropna()
L_test=df['text'].tolist()

y_pred=model.predict(L_test)
y_pred1=[]
for i in range(len(y_pred[0])):
    y_pred1.append(int(y_pred[0][i][0][len(y_pred[0][i][0])-1]))

row=[]
for i in range(len(df)):
    rr=[]
    rr.append(df['id'][i])
    rr.append(y_pred1[i])
    row.append(rr)
with open("../predictions/FT.csv",'w') as f:
    csvwriter=csv.writer(f)
    csvwriter.writerow(['id','hateful'])
    csvwriter.writerows(row)    
