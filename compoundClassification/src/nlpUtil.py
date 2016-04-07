#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
from nltk.stem.porter import PorterStemmer
from nltk import pos_tag
import collections
from collections import *
from nltk.util import ngrams
from nltk.tokenize import word_tokenize

ps = PorterStemmer()

#return the frequency of all n-grams in given content c
def wordFreq(c,stopword=(),l=4):
	words_temp=word_tokenize(c)
	words=[]
	sents=['.',',',':',';','!','?','(',')','\'','-',']','[','—','=']
	for w in words_temp:
	    if (not w in sents) and (not w in stopword):   
                words.append(ps.stem(w.strip()))
	grams=[]
	n=1
	while n<=l:
	    g=ngrams(words, n)
	    for gram in g:
	    	temp=' '.join(gg for gg in gram)
		if not temp in stopword:
			grams.append(temp)
	    n=n+1
	tf=defaultdict(int)
	for w in grams:
		tf[w]=tf[w]+1
	
	return tf
