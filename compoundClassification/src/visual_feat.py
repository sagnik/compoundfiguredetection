#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
import json,sys,os,cv2
import numpy as np
import collections
from collections import defaultdict
import sklearn
from sklearn.cluster import KMeans
base_path='../compoundfiguredetection/figureclasses/'

def resize(img_path):
    img = cv2.resize(cv2.imread(img_path),(256,256))
    return img
    	    

def detectWhiteHorizontalBoader(img, b1, b2):
    boader=0
    for y in xrange(b1,b2):
        for x in xrange(0,255):
            if (img[x][y]!=[255,255,255]).all():
                break
        #print x
        if x==254: boader=1
    return boader

def detectWhiteVerticalBorder(img, b1, b2):
    boader=0
    for x in xrange(b1,b2):
        for y in xrange(0,255):
            if (img[x][y]!=[255,255,255]).all():
                break
        if y==254: boader=1
    return boader

def detectBlackHorizontalBorder(img, b1, b2):
    boader=0
    for y in xrange(b1,b2):
        for x in xrange(0,255):
            if (img[x][y]!=[0,0,0]).all():
                break
        if x==254: boader=1
    return boader



def detectBlackVerticalBorder(img, b1, b2):
    boader=0
    for x in xrange(b1,b2):
        for y in xrange(0,255):
            if (img[x][y]!=[0,0,0]).all():
                break
        if y==254: boader=1
    return boader
           
def boaderFeatExt(path_list, feature_path):#read all files under the list to generate dictionary
    tf=defaultdict(lambda:defaultdict(int))
    frequency = defaultdict(lambda:defaultdict(int))
    label=0
    b1=51;b2=205
    f1=0;f2=0
    b=[0,0,0,0]
    writer=open(feature_path,'w')
    label=0
    for cat in os.listdir(base_path):
    	if not os.path .isdir(base_path+'/'+cat):
    	    continue
    	for f in os.listdir(base_path+'/'+cat+'/pngs'):
            if not os.path.isfile(base_path+'/'+cat+'/pngs/'+f): continue
            img = resize(base_path+'/'+cat+'/pngs/'+f)
            fn=os.path.splitext(f)[0]
            b[0]=detectWhiteHorizontalBoader(img,b1,b2)
            b[1]=detectWhiteVerticalBorder(img,b1,b2)
            b[2]=detectBlackHorizontalBorder(img,b1,b2)
            b[3]=detectBlackVerticalBorder(img,b1,b2)
            if b[0]==1 or b[2]==1: f1=1
            else: f1=0
            if b[1]==1 or b[3]==1: f2=1
            else: f2=0
            
            writer.write(fn+'\t'+str(label)+'\t'+str(f1)+'\t'+str(f2)+'\n')
        label=label+1
    print 'BOARDER PROFILE FEATURE GENERATED'
#http://nbviewer.ipython.org/gist/kislayabhi/abb68be1b0be7148e7b7
def sift(path_list, feature_path,k=200):
    writer=open(feature_path,'w')
    worg=open(feature_path+'_org','w')
    descriptor_mat=[]; N=[]; Y=[]
    label=0; times=[]
    for cat in os.listdir(base_path):
    	if not os.path .isdir(base_path+'/'+cat):
    	    continue
    	for f in os.listdir(base_path+'/'+cat+'/pngs'):
            if not os.path.isfile(base_path+'/'+cat+'/pngs/'+f): continue
            img = resize(base_path+'/'+cat+'/pngs/'+f)
            fn=os.path.splitext(f)[0]
            N.append(fn)
            Y.append(label)
            gray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            sift = cv2.SIFT()
            kp,des = sift.detectAndCompute(gray,None)
            times.append(len(des))
            descriptor_mat.append(des)
        label=label+1

        
    descriptor_mat=np.double(np.vstack(descriptor_mat))
    #descriptor_mat=descriptor_mat.T
    #print descriptor_mat
    #distance=EuclideanDistance(sg_descriptor_mat_features, sg_descriptor_mat_features)
    print 'SIFT DONE'
    kmeans=KMeans(k, max_iter =20)
    kmeans.fit(descriptor_mat)
    labels=list(kmeans.predict(descriptor_mat))
    print 'KMEANS DONE'
    pre=0
    for i,time in enumerate(times):
        vec=defaultdict(int)
        for l in xrange(time):
            worg.write(N[i]+'\t'+str(Y[i])+'\t'+str(labels[l+pre])+'\n')
            vec[labels[l+pre]]=vec[labels[l+pre]]+1
        writer.write(N[i]+'\t'+str(Y[i])+'\t'+'\t'.join(str(vec[j]) for j in xrange(k))+'\n')
        pre=pre+time
        
            
        
    worg.close()
    writer.close()
    print 'SIFT FEATURE GENERATED'

if __name__ == "__main__":
    path_list=[base_path+'compoundimages',base_path+'noncompoundimages']
    #boaderFeatExt(path_list,  base_path+'BoaderFeat')
    sift(path_list,  base_path+'SIFTFeat',k=50)
