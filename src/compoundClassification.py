#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
import pickle
import numpy as np
from sklearn.decomposition import PCA
from collections import *
from sklearn import cross_validation
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn.linear_model import LogisticRegression
from sklearn.grid_search import GridSearchCV
from scipy.stats import randint as sp_randint
from sklearn.preprocessing import StandardScaler
base_path='../compoundfiguredetection/figureclasses/'
def featPCA(fn, pca_file='',thres=20):
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
    pca=pca.fit(X)
    model_writer=  open(pca_file,'wb')
    pickle.dump(pca, model_writer)
    model_writer.close()
    X_new=pca.fit_transform(X)
    writer=open(fn+'_pca','w')
    for i,y in enumerate(Y):
        writer.write(N[i]+'\t'+str(y)+'\t'+'\t'.join(str(x) for x in X_new[i])+'\n')
    writer.close()
    print 'PCA FINISHED'
    
def mergeFeature(feature_path):
    #file_list=['BOWFeat_pca','CharFeat','BoaderFeat','SIFTFeat_pca']
    file_list=['SIFTFeat_pca']
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

    
def crossValidation():
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
    return X,Y
def compoundSVM(X,Y):
    print 'SVM'
    tuned_parameters = [{'kernel': ['rbf'], 'gamma': [1e-3, 1e-4],
                     'C': [1, 10]},{'kernel': ['linear'], 'C': [1,10]}]
    clf = GridSearchCV(svm.SVC(), tuned_parameters, cv=5)
    
    clf.fit(X, Y)
    print clf.best_params_
    scores = cross_validation.cross_val_score(clf, X,Y, cv=5)
    print clf.grid_scores_
    print scores
    
def compoundRF(X,Y):

    param_grid = {"max_depth": [3, None],
              "max_features": [30, 44],
              "min_samples_split": [1, 3, 10],
              "min_samples_leaf": [1, 3, 10],
              "bootstrap": [True, False],
              "criterion": ["gini", "entropy"]}
    clf = GridSearchCV(RandomForestClassifier(n_estimators=10), param_grid=param_grid, cv=5)
    
    clf.fit(X, Y)
    print clf.best_params_
    scores = cross_validation.cross_val_score(clf, X,Y, cv=5)
    print scores

def compoundLogistic(X,Y):
    param_grid = {'C': [0.01, 0.1, 1, 10] }
    X = StandardScaler().fit_transform(X)
    clf = GridSearchCV(LogisticRegression(), param_grid=param_grid, cv=5)
    #clf=LogisticRegression()
    clf.fit(X, Y)
    print clf.best_params_
    scores = cross_validation.cross_val_score(clf, X,Y, cv=5)
    print scores
    
if __name__ == "__main__":
    feature_path=base_path+'compoundFeat'
    model_path=base_path+'randomForest.pkl'
    merge=-1; ifPCA=1
    #if ifPCA==-1:  featPCA(base_path+'BOWFeat',base_path+'text_pca');featPCA(base_path+'SIFTFeat',base_path+'_pca')
    if merge==-1: mergeFeature(feature_path)
    #crossValidation(feature_path,model_path)
    X,Y = crossValidation()
    compoundLogistic(X,Y)
