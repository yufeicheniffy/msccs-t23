# Classifier

Full design details for the classifier may be found in the associated report for this project. This file contains details on how to run the classification evaluation script.

The evaluation script uses a modified form of cross validation, where one event is left out in each fold. The calculations include accuracy, recall, precision, and F1, both overall averages and by category. It also includes one label and perfect match scores. For full details, see the associated report.

The file to run to evaluate the classifier is test_classifier_by_event.py.
Options for this file include
* --out OUTPUT_NAME - the file to output the results to
* --classifier CLASSIFIER - the model to use for the classifier. Options include: 
    * rf - random forest
    * lsvc - linear svm
    * log - logistic regression
    * anything else - naive bayes
* --pretrained - uses a pretrained model instead of training one
* --save - saves the model used in the classifier for future use
