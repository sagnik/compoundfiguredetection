===== dir structure=====
See the attached zip please

===== parameter settings =====
base_path: relative path of compoundfiguredetection directory to source code, needed to specify in visual_feat.py, textual_feat.py, compoundClassification.py
visual_feat.py 

	boaderFeatExt :
		path_list: set as  [base_path+'compoundimages',base_path+'noncompoundimages']
		feature_path : base_path+feature_name
	sift: 
		k: # of clusters


textual_feat.py
	merge: since there are more json files than png files, specify merge as 1 to only save those json files with png files. Only need to be set as 1 for first running the experiments
	dicExists: -1 if there is  a dictionary
	

compoundClassification.py
	merge: no feature file for classification, specify as -1; otherwise specfiy as other value
	ifPCA: whether perform PCA on sift features and textual BOW


To get the experiment results, python compoundClassification.py, this scripts output 5 fold cross validation score 

To change the features used in classification, see ile_list parameter in mergeFeautre, add/remove any file

Experimental results on 815 figures

Textual BOW+ Character delmiter 0.68 0.67 0.67 0.7 0.72
Textual BOW+ Character delmiter +Boarder 0.77 0.73 0.76 0.74 0.74
All 0.8 0.74 0.89 0.86 0.81


===================FeatGenerator.py: To classify an image, you need to specify its image path and json path in this file. You also need to specify randomForest.pkl, test_pca, visual_pca and text dictionary path in the file. 
Then first use function featureGenerator() to generate all its features and then compoundClassfication() to classify the figure. See main function for the processing flow. . Y[0] ]is the predicted label and is returned by function compoundClassfication(), 0 stands for compound image and 1 stands for noncompound image.

### just text based detection
Just text based detection has 62.1%  accuracy for compound images and 87% accuracy for non compound images

##both text and column span based detection

75% accuracy for both compound and non compound images. 
