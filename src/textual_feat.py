#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
import json,sys,os
import numpy as np
import collections
from collections import defaultdict
from nlpUtil import wordFreq
from nltk.corpus import stopwords
stop = stopwords.words('english')
base_path='../compoundfiguredetection/figureclasses/'

#use json files with corresponding pngs
def mergePNG2JSON():
    file_set=set()
    for cat in os.listdir(base_path):
    	if not os.path .isdir(base_path+'/'+cat):
    	    continue
    	for f in os.listdir(base_path+'/'+cat+'/pngs'):
            if not os.path.isfile(base_path+'/'+cat+'/pngs/'+f): continue
            fn=os.path.splitext(f)[0]
            file_set.add(fn)
    for cat in os.listdir(base_path):
    	if not os.path .isdir(base_path+'/'+cat):
    	    continue
    	for f in os.listdir(base_path+'/'+cat+'/jsons'):
            if not os.path.isfile(base_path+'/'+cat+'/jsons/'+f): continue
            fn=os.path.splitext(f)[0]
            if not fn in file_set:
                os.remove(base_path+'/'+cat+'/jsons/'+f)
def loadJson(fp):
    r=open(fp,'r')
    return json.load(r)
def dicExt(path_list):#read all files under the list to generate dictionary
    tf=defaultdict(lambda:defaultdict(int))
    frequency = defaultdict(lambda:defaultdict(int))
    label=0
    count=0
    clsize=[]
    for cat in os.listdir(base_path):
    	if not os.path .isdir(base_path+'/'+cat):
    	    continue
    	count=0
    	for f in os.listdir(base_path+'/'+cat+'/jsons'):
            if not os.path.isfile(base_path+'/'+cat+'/jsons/'+f): continue
            jtexts = loadJson(base_path+'/'+cat+'/jsons/'+f)
            jtexts_lower=dict((k.lower(), v) for k, v in jtexts.iteritems())
            if not 'caption' in jtexts_lower: continue
            tf_file=wordFreq(jtexts_lower['caption'].lower(),stopword=stop,l=1)
            for w in tf_file:
                frequency[label][w]=frequency[label][w]+1
            count=count+1
        clsize.append(count)
        label=label+1
    
        
    return frequency, clsize
def dicFilter(tf, clsize,thres=0.85):#normalized by article length
    article_len = [];candidates=set(); keywords=set()
    word_diff = defaultdict(float)
    #print clsize
    #for c in tf:
    #    count=sum(tf[c][w] for w in tf[c])
    #    article_len.append(count)
    for c in tf:
        for w in tf[c]:
            candidates.add(w)
    
    for w in candidates:
        #print w.encode('utf-8')
        #print tf[0][w]
        #print tf[1][w]
        #print tf[0][w]/clsize[0]
        #print tf[1][w]/clsize[1]
        word_diff[w]=abs(tf[0][w]/clsize[0]-tf[1][w]/clsize[1])
        

    sorted_diff = sorted(word_diff.items(), key=lambda x: x[1], reverse=True)
    #print sorted_diff
    for i,p in enumerate(sorted_diff):
        if i>(1-thres)*len(sorted_diff): break
        if len(p[0])<=2: continue
        keywords.add(p[0])
    return keywords
def saveDict(words, dicPath):
    with open(dicPath,'w') as w:
        for k in words:
            w.write(k.encode('utf-8')+'\n')
def loadDict(dicPath):
    dic=set()
    with open(dicPath,'r') as r:
        for w in r: dic.add(w.strip().decode('utf-8'))
    return dic
def fileFreq(text,dic): #get the word frequency for given texts using extracted dictionary
    tf_file=defaultdict(int)
    tf=wordFreq(text,stopword=stop,l=1)
    for w in tf:
        if w in dic:
            tf_file[w]=tf_file[w]+1
    return tf_file
def BOWFeature(json_files, dicPath, feature_path=''):
    dic=loadDict(dicPath);label=0
    dic_list=list(dic)
    writer=open(feature_path,'w')
    worg=open(feature_path+'_org','w')
    for cat in os.listdir(base_path):
    	if not os.path .isdir(base_path+'/'+cat):
    	    continue
    	for f in os.listdir(base_path+'/'+cat+'/jsons'):
            if not os.path.isfile(base_path+'/'+cat+'/jsons/'+f): continue
            jtexts = loadJson(base_path+'/'+cat+'/jsons/'+f)
            jtexts_lower=dict((k.lower(), v) for k, v in jtexts.iteritems())
            if not 'caption' in jtexts_lower: continue
            tf=wordFreq(jtexts_lower['caption'].lower(), stopword=stop,l=1)
            fn=os.path.splitext(f)[0]
            
            worg.write(fn+str(label)+'\t'+'\t'+'\t'.join(w.encode('utf-8')+'\t'+str(tf[w]) for w in tf if w in dic_list)+'\n')
            writer.write(fn+'\t'+str(label)+'\t'+'\t'.join(str(tf[w]) for w in dic)+'\n')
        label=label+1
    writer.close()
    worg.close()
    print 'BAG OF TEXTUAL FEATURE GENERATED'
def CharDelimiterFeature(json_files, feature_path):
    #pattern 1 2 is removed here
    pattern=[[u'A',u'B'],[u'Lower',u'Upper'],[u'lower',u'upper'],[u'i',u'ii'],[u'(1).',u'(2).'],[u'1).',u'2).'],[u'Left',u'Right'],[u'left',u'right'],[u'I).',u'II).']]
    writer=open(feature_path,'w');label=0
    worg=open(feature_path+'_org','w')
    for cat in os.listdir(base_path):
    	if not os.path .isdir(base_path+'/'+cat):
    	    continue
    	for f in os.listdir(base_path+'/'+cat+'/jsons'):
            if not os.path.isfile(base_path+'/'+cat+'/jsons/'+f): continue
            jtexts = loadJson(base_path+'/'+cat+'/jsons/'+f)
            jtexts_lower=dict((k.lower(), v) for k, v in jtexts.iteritems())
            if not 'caption' in jtexts_lower: continue
            l=[0,0]
            text=jtexts['Caption'].lower()
            for p in pattern:
                if p[0] in text and p[1] in text:
                    l=[1,1]
                    #print p
                    break
            fn=os.path.splitext(f)[0]
            worg.write(fn+'\t'+str(label)+'\t'+'\t'.join(str(ll) for ll in l)+'\n')
            writer.write(fn+'\t'+str(label)+'\t'+'\t'.join(str(ll) for ll in l)+'\n')
        label=label+1
    writer.close()
    print 'CHARACTER DELIMITER FEATURE GENERATED'
if __name__ == "__main__":
    merge=-1
    if merge==1: mergePNG2JSON()
    path_list=[base_path+'compoundimages',base_path+'noncompoundimages']
    
    dicExists=-1; dic_path=base_path+'dic'
    
    if dicExists == -1:
        tf,clsize= dicExt(path_list)
        words=dicFilter(tf,clsize)
        saveDict(words,dic_path)
    #print dic_path
    BOWFeature(path_list, dic_path, base_path+'/BOWFeat')
    
    CharDelimiterFeature(path_list, base_path+'/CharFeat')
