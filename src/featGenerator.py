#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
from sklearn.decomposition import PCA
from visual_feat import *
from textual_feat import *
from nlpUtil import *
base_path='../compoundfiguredetection/figureclasses/'
def featureGenerator(json_file, img_file,text_pca,visual_pca ,dicPath, kmeans_model, k=200):
    feat=[]
    
    
    if not os.path.isfile(json_file): print 'no json file';exit(-1)
    if not os.path.isfile(img_file): print 'no png file';exit(-1)

    dic=loadDict(dicPath)
    jtexts = loadJson(json_file)
    jtexts_lower=dict((k.lower(), v) for k, v in jtexts.iteritems())

    if not 'caption' in jtexts_lower: feat.extend([0 for i in range(0,20)])
    else:
        tf=wordFreq(jtexts_lower['caption'].lower(), stopword=stop,l=1)
        X=[tf[w] for w in dic]
        X=np.array(X)
        f_text_pca = open(text_pca, 'rb')
        tpca = pickle.load(f_text_pca)
        X_new_BOW=tpca.transform(X)
        
        f_text_pca.close()
        for x in  X_new_BOW.tolist():
            for xx in x: feat.append(xx)
            
    #char delimiter
    pattern=[[u'A',u'B'],[u'Lower',u'Upper'],[u'lower',u'upper'],[u'i',u'ii'],[u'(1).',u'(2).'],[u'1).',u'2).'],[u'Left',u'Right'],[u'left',u'right'],[u'I).',u'II).']]
    if not 'caption' in jtexts_lower: feat.extend([0 for i in range(0,2)])
    else:
        l=[0,0]
        text=jtexts['Caption'].lower()
        for p in pattern:
            if p[0] in text and p[1] in text:
                l=[1,1]
                break
        feat.extend(l)
    
    
    #boarder profile
    f1=0;f2=0;b1=51;b2=205;b=[0,0,0,0]
    img = resize(img_file)
    b[0]=detectWhiteHorizontalBoader(img,b1,b2)
    b[1]=detectWhiteVerticalBorder(img,b1,b2)
    b[2]=detectBlackHorizontalBorder(img,b1,b2)
    b[3]=detectBlackVerticalBorder(img,b1,b2)
    if b[0]==1 or b[2]==1: f1=1
    else: f1=0
    if b[1]==1 or b[3]==1: f2=1
    else: f2=0
    feat.append(f1);feat.append(f2)
    
    #sift
    gray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    sift = cv2.SIFT()
    
    kp,des = sift.detectAndCompute(gray,None)
    
    f = open(kmeans_model, 'rb')
    kmeans = pickle.load(f)
    
    labels=list(kmeans.predict(des))
    
    vec=defaultdict(int)
    for l in xrange(len(des)):
        vec[labels[l]]=vec[labels[l]]+1
    
    X=[vec[j] for j in xrange(k)]
    X=np.array(X)
    f_visual_pca = open(visual_pca, 'rb')
    vpca = pickle.load(f_visual_pca)
    X_new_SIFT=vpca.transform(X)
    for x in  X_new_SIFT.tolist():
            for xx in x: feat.append(xx)
    f.close();f_visual_pca.close()
    return feat
def compoundClassfication(feat,model_path):
    f = open(model_path, 'rb')
    clf = pickle.load(f)
    
    Y=clf.predict(feat)
    print Y[0]
    f.close()
    return Y[0]
if __name__ == "__main__":
    json_file=base_path+'noncompoundimages/jsons/10.1.1.1.1924-Figure-1.json'
    img_file=base_path+'noncompoundimages/pngs/10.1.1.1.1924-Figure-1.png'
    dic_path=base_path+'dic'
    
    feat=featureGenerator(json_file,img_file,base_path+'text_pca',base_path+'visual_pca',dic_path,base_path+'kmeans.pkl',k=200)
    compoundClassfication(feat,base_path+'randomForest.pkl')

    
