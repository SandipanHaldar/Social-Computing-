#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 18:15:14 2020

@author: sandipan
"""
import pandas as pd
import csv
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import AdaBoostClassifier


#vectorizing the tweets  before applying on adaboost classifier

vectorizer = TfidfVectorizer(max_df=0.8,min_df=0.05,)
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


clf = AdaBoostClassifier(n_estimators=100, random_state=0)
clf.fit(X_train, y_train)
y_pred=clf.predict(X_test)

row=[]
for i in range(len(df)):
    rr=[]
    rr.append(df['id'][i])
    rr.append(y_pred[i])
    row.append(rr)
with open("../predictions/T2.csv",'w') as f:
    csvwriter=csv.writer(f)
    csvwriter.writerow(['id','hateful'])
    csvwriter.writerows(row)
    
