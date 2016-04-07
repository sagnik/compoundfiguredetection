#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
import numpy as np
from sklearn.decomposition import PCA
from collections import *
from sklearn import cross_validation
from sklearn.ensemble import RandomForestClassifier
base_path='../compoundfiguredetection/figureclasses/'
def featPCA(fn, thres=20):
    print fn
    r=open(fn,'r')
    X=[]; Y=[];N=[]
    for line in r:
        if len(line.split('\t')) < 2: continue
        feat=[]
        N.append(line.split('\t')[0])
        Y.append(line.split('\t')[1])
        for i,field in enumerate(line.split('\t')):
            
            if i==0 or i==1:continue
            feat.append(line.split('\t')[i])
        X.append(feat)
    
    X=np.array(X)
    pca = PCA(n_components=20)
    X_new=pca.fit_transform(X)
    writer=open(fn+'_pca','w')
    for i,y in enumerate(Y):
        writer.write(N[i]+'\t'+str(y)+'\t'+'\t'.join(str(x) for x in X_new[i])+'\n')
    writer.close()
    print 'PCA FINISHED'
    
def mergeFeature(feature_path):
    file_list=['BOWFeat_pca', 'CharFeat','BoaderFeat','SIFTFeat_pca']
    X=defaultdict(list);Y=defaultdict(int)
    writer=open(feature_path,'w')
    for f in file_list:
        r=open(base_path+f,'r')
        for line in r:
            if len(line.split('\t')) < 2: continue
            fn=line.split('\t')[0]
            Y[fn]=line.split('\t')[1]
            for i,field in enumerate(line.split('\t')):
                if i==0 or i==1:continue
                X[fn].append(line.split('\t')[i].strip())
        r.close()
    for fn in Y:
        writer.write(Y[fn]+'\t'+'\t'.join(str(v) for v in X[fn])+'\n')
    writer.close()
    print 'FEATURE FILE GENERATED'

    
def crossValidation(feature_path):
    X=[]; Y=[]
    r=open(feature_path,'r')
    for line in r:
        if len(line.split('\t')) < 2: continue
        feat=[]
        Y.append(line.split('\t')[0])
        for i,field in enumerate(line.split('\t')):
            if i==0 :continue
            feat.append(line.split('\t')[i])
        X.append(feat)
        
    clf = RandomForestClassifier(n_estimators=10, max_depth=None, min_samples_split=1, random_state=0)   
    cores = cross_validation.cross_val_score(clf, X,Y, cv=5)
    print cores
if __name__ == "__main__":
    feature_path=base_path+'compoundFeat'
    merge=1; ifPCA=1
    if ifPCA==1:  featPCA(base_path+'BOWFeat');featPCA(base_path+'SIFTFeat')
    if merge==1: mergeFeature(feature_path)
    crossValidation(feature_path)
