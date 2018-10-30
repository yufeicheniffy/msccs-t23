from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import accuracy_score
from sklean.metrics import classification_report
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score
import pandas as pd
import codecs
import unicode
import numpy as np


#text proccess
#split data to 25 categories
#make document-term-vector of all categories
#train the algorithm
#test and evaluate

#input 25 fited classifiers, and a test data
#assuming we have classifiers eg naive bayes or randomforest
def test_and_evaluate(classifiers, Xtest, Ytest):

    #for each category create the term document for X test
    # X must be term+1 columns the +1 column is the id
    # classifier has an id also
    for c in classifiers:
        term_doc_list = term_document_category(Xtest, c[-1])
        randomf=RandomForestClassifier(n_estimators=115, criterion='entropy', class_weight='balanced')
        #randomf.fit(x_processed_for_each_category,category_for_each_x)
        y_pred =randomf.predict(Xtest)
        with codecs.open('y_pred.txt', 'w', encoding='utf-8') as f:
            for i in range(y_pred.shape[0]):
                f.write(unicode(y_pred[i])+' '+Xtest[-1]+'\n')
        # since it is one label classifier we want accuracy_score
        #prints precission-recall-f1-score-support of the classifier
        print("for classifier c")
        rf_accuracy = accuracy_score(Ytest, y_pred)
        rf_classification_report = classification_report(Ytest, y_pred)
        rf_precision = precision_score(Ytest, y_pred, pos_label=1)
        rf_recall = recall_score(Ytest, y_pred, pos_label=1)
        rf_f1 = f1_score(Ytest, y_pred, pos_label=1)
        f = open("metrics_rf.txt", 'w')
        f.write('rf_accuracy: %s \n')%rf_accuracy
        f.write('rf_classification_report: %s \n')%rf_classification_report
        f.write('rf_prec at true labels: %s \n')%rf_precision
        f.write('rf_recall at true labels: %s \n')%rf_recall
        f.write('rf_f1 at true labels: %s \n')%rf_f1




    # SVM
    svm_model = SVC(probability=True)
    # Fit
    # for each category
    #svm_model = svm_model.fit(x_train, y_train)
    # Accuracy on training data
    #svm_model.score(x_train, y_train)

    # Predictions/probs on the test dataset
    predicted = (svm_model.predict(Xtest))
    probs = (svm_model.predict_proba(Xtest))

    # Store metrics
    svm_accuracy = accuracy_score(Ytest, predicted)
    svm_classification_report = classification_report(Ytest, predicted)
    svm_precision = precision_score(Ytest, predicted, pos_label=1)
    svm_recall = recall_score(Ytest, predicted, pos_label=1)
    svm_f1 = f1_score(Ytest, predicted, pos_label=1)

    # Evaluate the model using 10-fold cross-validation
    svm_cv_scores = cross_val_score(SVC(probability=True), Xtest, Ytest, scoring='precision', cv=10)
    svm_cv_mean = np.mean(svm_cv_scores)
    # write to txt
    f = open("metrics_svm.txt", 'w')
    f.write('svm_accuracy: %s \n')%svm_accuracy
    f.write('svm_classification_report: %s \n')%svm_classification_report
    f.write('svm_precision at true labels: %s \n')%svm_precision
    f.write('svm_recall at true labels: %s \n')%svm_recall
    f.write('svm_f1 at true labels: %s \n')%svm_f1
    f.write('svm_crossvalidation 10-fold mean : %s \n')%svm_cv_mean

    #Bayes

    bayes_model = GaussianNB()
# Fit the model
    #bayes_model.fit(x_train, y_train)
    # Accuracy
    #bayes_model.score(x_train, y_train)

    # Predictions/probs on the test dataset
    predicted = (bayes_model.predict(Xtest))
    probs = (bayes_model.predict_proba(Xtest))

    # Store metrics
    bayes_accuracy = accuracy_score(Ytest, predicted)
    bayes_classification_report = classification_report(Ytest, predicted)
    bayes_precision = precision_score(Ytest, predicted, pos_label=1)
    bayes_recall = recall_score(Ytest, predicted, pos_label=1)
    bayes_f1 = f1_score(Ytest, predicted, pos_label=1)

    f = open("metrics_svm.txt", 'w')
    f.write('GausianNB_accuracy: %s \n')%bayes_accuracy
    f.write('GaussianNB_classification_report: %s \n')%bayes_classification_report
    f.write('GaussianNB_prec at true labels: %s \n')%bayes_precision
    f.write('GaussianNB_recall at true labels: %s \n')%bayes_recall
    f.write('GaussianNB_f1 at true labels: %s \n')%bayes_f1

    models = pd.DataFrame({'Model': ['r.f.', 'SVM', 'Bayes'], 'Accuracy': [rf_accuracy, svm_accuracy, bayes_accuracy], 'Precision': [rf_precision, svm_precision, bayes_precision], 'recall': [rf_recall, svm_recall, bayes_recall], 'F1': [rf_f1, svm_f1, bayes_f1]})
    models.to_csv('summary_results.txt', sep='\t', encoding='utf-8')
