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
from scipy import sparse

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

    def __init__(self, tweet_texts=None, cats=None, vocab_size=2000, model=BernoulliNB(), 
        pretrained=None):
        """
        Create and train classifier. Can specify path to pretrained
        classifiers using "pretrained"

        :param tweet_texts: list of tweets to train classifier on
        :param cats: matrix of categories that belong to the tweets
        :param vocab_size: maximum number of words in classifier
        :param model: model to use for classification
        :param pretrained: path to pretained classifiers, if using
                            pretrained classifiers
        """
        self.cat = cats
        self.text = tweet_texts
        self.model = model

        self.classifiers = list()
        
        if pretrained is None:
            self.train()
        else: # load pretrained classifiers
            for f in sorted(os.listdir(pretrained)):
                fn = os.fsdecode(f)
                if fn.endswith('v.pkl'):
                    self.vectorizer = joblib.load(pretrained+fn)
                else:
                    self.classifiers.append(joblib.load(pretrained+fn))


    def train(self, text = None, cats = None, vocab_size = 2000):
        """
        Fits classifiers to the training data provided. If
        already trained, clears classifiers and retrains.

        :param text: tweets to train on. defaults to tweets provided
            on creation
        :param cats: actual labels
        :param vocab_size: number of words as max features
        """
        if text is None:
            text = self.text
        if cats is None:
            cats = self.cat

        # fit vectorizer
        self.vectorizer = CountVectorizer(stop_words=stopwords.words(),
            binary=True, max_features=vocab_size)
        self.vect_train = self.vectorizer.fit_transform(text)
        hashtags = np.array([[1] if '#' in t else [0] for t in text])
        addtl_feat = sparse.hstack([self.vect_train, hashtags])

        print(addtl_feat.shape)

        # clear classifiers (in case retraining)
        self.classifiers = list()

        cat_arr = np.array(cats)

        # train
        for i in range(0, len(cat_arr[0])):
            # unknown should not be predicted unless no other category found
            if i == self.catadictionary['Unknown']:
                m = DummyClassifier('constant', constant=0)
            else:
                m = clone(self.model)
            c = m.fit(addtl_feat, cat_arr[:,i])
            self.classifiers.append(c)

        #print("Training complete!")

    def save_classifier(self, path='pretrained/'):
        """
        Saves the classifier to the specified path

        :param path: directory to save classifier and vectorizer into
        """
        joblib.dump(self.vectorizer, path+'v.pkl', compress=1)
        for n in range(0,len(self.classifiers)):
            joblib.dump(self.classifiers[n], path+'c%02d.pkl' % n, compress=1)
        print("Classifiers saved to: " + path)

    def map_id(self, category):
        """
        Return the indices of the given categories e.g. 0 = 'Advice'

        :param category: categories to lookup

        :return: list of int index
        """
        returner = []
        for c in category:
            if c in self.catadictionary:
                returner.append(self.catadictionary.get(c))
        return returner

    def evaluation_(self, ytest_array, predict, names):
        """
        Evaluate the gicen input 
        """
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
            eval['Perfect Match'], rows=len(actual[0]))
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
        hashtags = [[1] if '#' in t else [0] for t in tweets]
        addtl_feat = sparse.hstack([tokenized, hashtags])

        predictions = np.zeros((len(tweets), len(self.classifiers)))

        for i in range(0, len(self.classifiers)):
            predictions[:,i] = self.classifiers[i].predict(addtl_feat)
        
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

    def stats_calc(self, tp, tn, fp, fn, one_lab, perf_match, rows=25):
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
        t = n/rows
        ret['One Label Score'] = one_lab/t
        ret['Perfect Match Score'] = perf_match/t
        ret['Accuracy'] = (tp+tn)/n
        ret['Precision'] = tp/(tp+fp)
        ret['Recall'] = tp/(tp+fn)
        try:
            ret['F1 Score'] = (2*(ret['Precision']*ret['Recall']))/(ret['Precision']+ret['Recall'])
        except ZeroDivisionError:
            ret['F1 Score'] = 0
        return ret
