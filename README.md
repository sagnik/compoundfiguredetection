##Compound Figure Detection

Input: 1. An image file for a scholarly figure, as output by pdffigures by AllenAI. 2. A Json file containing the caption of the image.
 
Output: Compound (contains sub figure)/ Non Compound (stand alone)

### Contact: Shuting Wang (sxw327@psu.edu)

###parameter settings
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

Random Forest

criterion: entropy bootstrap true max-depth false max_feature 44 min_samples_split 3 min_samples_leaf 10

bow: 0.7 0.7 0.68 0.69 0.71
char 0.58 0.52 0.55 0.53 057
board 0.8 0.79 0.7 0.8 0.74
sift 0.7 0.75 0.68 0.71 0.63
Overall 0.85 0.8 0.89 0.88 0.82


SVM 
kernal: rbf C:10 gamma: 0.001

bow 0.76 0.66 0.67 0.72 0.76
char delimiter 0.58  0.52 0.55 0.53 0.57
board 0.72 0.73 0.8 0.79 0.75
sift 0.71 0.8 0.77 0.75 0.7
overall 0.87 0.85 0.87 0.88 0.84


logistic
bow 0.76 0.68 0.68 0.72 0.76
char 0.58 0.52 0.55 0.53 0.57
board 0.78 0.73 0.8 0.8 0.75
sift 0.72 0.76 0.74 0.75 0.66
overall 0.87 0.81 0.83 0.85 0.82


###FeatGenerator.py 
To classify an image, you need to specify its image path and json path in this file. You also need to specify randomForest.pkl, test_pca, visual_pca and text dictionary path in the file. 

Then first use function featureGenerator() to generate all its features and then compoundClassfication() to classify the figure. See main function for the processing flow. . Y[0] ]is the predicted label and is returned by function compoundClassfication(), 0 stands for compound image and 1 stands for noncompound image.
