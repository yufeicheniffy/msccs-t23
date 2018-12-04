import sys, os
sys.path.insert(0, './data_files_scripts')

from sklearn.svm import *
from sklearn.naive_bayes import BernoulliNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
import numpy as np
from sklearn.metrics import f1_score, precision_score, recall_score, accuracy_score
from sklearn.externals import joblib
from sklearn.base import clone
from sklearn.dummy import DummyClassifier

class Classify:
    """
    A classifier which pulls tweet data from the mongodb database.
    """
    catadictionary={'GoodsServices':0, 'SearchAndRescue':1,'InformationWanted':2,'Volunteer':3,'Donations':4,
                    'MovePeople':5, 'FirstPartyObservation': 6, 'ThirdPartyObservation': 7, 'Weather': 8, 'EmergingThreats': 9,
                    'SignificantEventChange':10, 'MultimediaShare': 11, 'ServiceAvailable': 12, 'Factoid': 13, 'Official': 14,
                    'CleanUp':15, 'Hashtags': 16, 'PastNews': 17, 'ContinuingNews': 18, 'Advice': 19,
                    'Sentiment':20, 'Discussion': 21, 'Irrelevant': 22, 'Unknown': 23, 'KnownAlready': 24,
                    }

    def __init__(self, cats=None, tweet_texts=None, vocab_size=2000, model=BernoulliNB(), 
        pretrained=None):
        """
        Create and train classifier. Can specify path to pretrained
        classifiers using "pretrained"
        """
        self.cat = cats
        self.text = tweet_texts
        self.cat_arr = np.array(self.cat)
        #print(self.vectorizer.get_feature_names())
        self.model = model

        self.classifiers = list()
        
        if pretrained is None:
            self.vectorizer = CountVectorizer(stop_words=stopwords.words(),
                binary=True, max_features=vocab_size)
            self.vect_train = self.vectorizer.fit_transform(self.text)
            self.train()
        else:
            for f in sorted(os.listdir(pretrained)):
                fn = os.fsdecode(f)
                if fn.endswith('v.pkl'):
                    self.vectorizer = joblib.load(pretrained+fn)
                else:
                    self.classifiers.append(joblib.load(pretrained+fn))


    def train(self):
        """
        Fits classifiers to the training data we already have.
        """
        #len(categories)
        for i in range(0, len(self.cat_arr[0])):
            # unknown should not be predicted unless no other category found
            if i == self.catadictionary['Unknown']:
                m = DummyClassifier('constant', constant=0)
            else:
                m = clone(self.model)
            c = m.fit(self.vect_train, self.cat_arr[:,i])
            self.classifiers.append(c)

        print("Training complete!")


    def save_classifier(self, path='pretrained/'):
        """
        Saves the classifier to the specified path
        """
        joblib.dump(self.vectorizer, path+'v.pkl', compress=1)
        for n in range(0,len(self.classifiers)):
            joblib.dump(self.classifiers[n], path+'c%02d.pkl' % n, compress=1)
        print("Classifiers saved to: " + path)

    #retrieves the index of category eg 0 = 'Advice'
    def map_id(self,category):
        returner = []
        for c in category:
            for i in range(0,len(self.categories)):
                if(c == self.categories[i]):
                    returner.append(i)
        return returner

#   input ytest_array,and X_test
    def evaluation_(self,ytest_array,predict,names):
        ytest_arr = np.array(ytest_array)
        res = list()
        for x in range(0, len(ytest_array[0])):
            d = {"Category": names[x],
                "Accuracy": accuracy_score(ytest_arr[:,x],predict[:,x]),
                "Recall": recall_score(ytest_arr[:,x],predict[:,x]),
                "Precision": precision_score(ytest_arr[:,x],predict[:,x]),
                "F1": f1_score(ytest_arr[:,x],predict[:,x])}
            #print(d)
            res.append(d)
        return res

    def simple_evaluation(self, actual, prediction):
        """
        Simple evaluator, returning overal confusion matrix, accuracy
        recall, precision, f1
        """
        eval = {'Number of Predictions': len(actual)*len(actual[0]),
                'True Positive': 0, 'True Negative': 0,
                'False Positive': 0, 'False Negative': 0,
                'One Label': 0, 'Perfect Match': 0}
        one_lab = False

        for x in range(0, len(actual)):
            if np.array_equal(actual[x], prediction[x]):
                eval['Perfect Match'] += 1
            for y in range(0, len(actual[x])):
                if actual[x][y] == 1:
                    if prediction[x][y] == 1:
                        eval['True Positive'] += 1
                        one_lab = True
                    else: 
                        eval['False Negative'] +=1
                else:
                    if prediction[x][y] == 1:
                        eval['False Positive'] += 1
                    else:
                        eval['True Negative'] += 1
            if one_lab:
                eval['One Label'] += 1
            one_lab = False
        stats = self.stats_calc(eval['True Positive'], 
            eval['True Negative'], eval['False Positive'], 
            eval['False Negative'], eval['One Label'], 
            eval['Perfect Match'])
        eval = {**eval, **stats}
        #print(eval)
        return eval

    def predict(self,tweets):
        """
        Returns an array of predictions for the given features.

        :param tweets: a list or array of string tweets
        :returns: predictions matrix

        :throws RuntimeError: if classifiers have not been trained
        """
        if len(self.classifiers) == 0:
            raise RuntimeError("Classifiers have not been trained!")
        tokenized = self.vectorizer.transform(tweets)
        predictions = np.zeros((len(tweets), len(self.classifiers)))

        for i in range(0, len(self.classifiers)):
            predictions[:,i] = self.classifiers[i].predict(tokenized)
        
        # if nothing predicted, category should be unknown
        for row in predictions:
            if np.sum(row) == 0:
                row[self.catadictionary['Unknown']] = 1
        return(predictions)

    def return_predict_categories(self,tweets):
        """
        Returns an List of prediction catagories for the given features.
        :param tweets: a list or array of string tweets
        :returns: predictions matrix

        :throws RuntimeError: if classifiers have not been trained
    
        """
        if len(self.classifiers) == 0:
            raise RuntimeError("Classifiers have not been trained!")
        tokenized = self.vectorizer.transform(tweets)
        predictions = np.zeros((len(tweets), len(self.classifiers)))

        for i in range(0, len(self.classifiers)):
            predictions[:,i] = self.classifiers[i].predict(tokenized)
        #for i in range((len(tweets)):
            #predictions_cateindex=np.argwhere(predictions[i,:])
            #predictions_categories=self.catadictionary.keys
        return(predictions)

    def stats_calc(self, tp, tn, fp, fn, one_lab, perf_match):
        """
        Calculate summary statistics, return as dict.

        :param tp: # of true postitives
        :param tn: # of true negatives
        :param fp: # of false positives
        :param fn: # of false negatives
        :param one_lab: # with 1 true positive
        :param perf_match: # with all labels correct

        :return: dict of scores
        """
        ret = dict()
        n = tp + tn + fp + fn

        # one label/perfect match is out of number of 
        # tweets, not predictions
        t = n/len(catadictionary)
        ret['One Label Score'] = one_lab/t
        ret['Perfect Match Score'] = perf_match/t
        ret['Accuracy'] = (tp+tn)/n
        ret['Precision'] = tp/(tp+fp)
        ret['Recall'] = tp/(tp+fn)
        ret['F1 Score'] = (2*(ret['Precision']*ret['Recall']))/(ret['Precision']+ret['Recall'])
        return ret
