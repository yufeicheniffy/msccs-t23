import sys
import os
from sklearn.naive_bayes import BernoulliNB
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
import numpy as np
from sklearn.externals import joblib
from sklearn.base import clone
from sklearn.dummy import DummyClassifier
from scipy import sparse

sys.path.insert(0, './data_files_scripts')


class Classify:
    """
    A classifier which can categorize tweets into one or more of the
    25 categories, as required by TREC.
    """
    catadictionary={'GoodsServices':0, 'SearchAndRescue':1,'InformationWanted':2,'Volunteer':3,'Donations':4,
                    'MovePeople':5, 'FirstPartyObservation': 6, 'ThirdPartyObservation': 7, 'Weather': 8,
                    'EmergingThreats': 9, 'SignificantEventChange':10, 'MultimediaShare': 11, 'ServiceAvailable': 12,
                    'Factoid': 13, 'Official': 14, 'CleanUp':15, 'Hashtags': 16, 'PastNews': 17, 'ContinuingNews': 18,
                    'Advice': 19, 'Sentiment':20, 'Discussion': 21, 'Irrelevant': 22, 'Unknown': 23, 'KnownAlready': 24}
    actionable = ['SearchAndRescue', 'MovePeople', 'InformationWanted']
    knowledge = ['FirstPartyObservation', 'EmergingThreats',
                 'SignificantEventChange', 'MultimediaShare','Official']

    def __init__(self, tweet_texts=None, cats=None, vocab_size=2000, model=BernoulliNB(alpha = 0.1),
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
        self.vectorizer = None
        self.vect_train = None

        if pretrained is None:
            self.train(vocab_size=vocab_size)
        else: # load pretrained classifiers
            for f in sorted(os.listdir(pretrained)):
                fn = os.fsdecode(f)
                if fn.endswith('v.pkl'):
                    self.vectorizer = joblib.load(pretrained+fn)
                else:
                    self.classifiers.append(joblib.load(pretrained+fn))

    def train(self, text=None, cats=None, vocab_size=2000):
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
                                          binary=True,
                                          max_features=vocab_size)
        self.vect_train = self.vectorizer.fit_transform(text)

        # add feature determining if hashtag in tweet
        hashtags = np.array([[1] if '#' in t else [0] for t in text])
        addtl_feat = sparse.hstack([self.vect_train, hashtags])

        # clear classifiers (in case of retraining)
        self.classifiers = list()

        cat_arr = np.array(cats) # convert to array

        # train
        for i in range(0, len(cat_arr[0])):
            # unknown should not be predicted unless no other category found
            # so use dummy classifier only predicting 0 for unknown
            if i == self.catadictionary['Unknown']:
                m = DummyClassifier('constant', constant=0)
            else:
                # clone original model. "clone" is needed or it will
                # just keep training the original model on all categories
                m = clone(self.model)
            # fit model and append to list of models
            c = m.fit(addtl_feat, cat_arr[:,i])
            self.classifiers.append(c)

    def save_classifier(self, path='pretrained/'):
        """
        Saves the classifier to the specified path

        :param path: directory to save classifier and vectorizer into
        """
        # save vectorizer
        joblib.dump(self.vectorizer, path+'v.pkl', compress=1)
        # save classifiers
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

    def mat_all_categories(self, actual, prediction):
        """
        Evaluator returning confusion matrices for all categories
        as a dictionary, with the keys being the categories and
        values being confusion matrix dictionaries

        :param actual: actual category matrix
        :param prediction: prediction matrix

        :return: dictionary of confusion matrix by category
        """
        ind_to_cat = self.category_indices()
        ret = dict()
        actual_arr = np.array(actual)
        prediction_arr = np.array(prediction)
        for n in range(0, len(actual[0])):
            vals = self.mat_one_category(actual_arr[:,n], prediction_arr[:,n])
            ret[ind_to_cat[n]] = vals
        return ret

    def mat_one_category(self, actual, prediction):
        """
        Evaluator returning confusion matrix for a single category as a dict

        :param actual: numpy array of binary category vals
        :param prediction: binary numpy array of predictions

        :return: dict of number of predictions,
                true pos, true neg, false pos,
                and false neg for predictions
        """
        eval = {'Number of Predictions': len(actual),
                'True Positive': 0, 'True Negative': 0,
                'False Positive': 0, 'False Negative': 0}

        for x in range(0, len(actual)):
            if actual[x] == 1:
                if prediction[x] == 1:
                    eval['True Positive'] += 1
                else:
                    eval['False Negative'] +=1
            else:
                if prediction[x] == 1:
                    eval['False Positive'] += 1
                else:
                    eval['True Negative'] += 1
        return eval

    def evaluate(self, actual, prediction):
        """
        Evaluator, returning overall confusion matrix, accuracy
        recall, precision, f1, one label, category, and perfect match
        scores as a dictionary

        :param actual: a matrix of actual binary values
        :param prediction: a matrix of the predicted binary values

        :return: dictionary of number of predictions, true/false
                positive/negative, number of rows with at least 1
                true positive, number of perfect match rows,
                accuracy, precision, recall, f1, one label,
                and perfect match scores
        """
        # result matrix
        evaluation_mat = {'Number of Predictions': len(actual)*len(actual[0]),
                          'True Positive': 0, 'True Negative': 0,
                          'False Positive': 0, 'False Negative': 0,
                          'One Label': 0, 'Perfect Match': 0}
        one_label = False # used to check if at least one label in current row is true pos

        # evaluate by row
        for x in range(0, len(actual)):
            # check for perfect match
            if np.array_equal(actual[x], prediction[x]):
                evaluation_mat['Perfect Match'] += 1

            # iterate through predictions
            for y in range(0, len(actual[x])):
                if actual[x][y] == 1:
                    if prediction[x][y] == 1:
                        # both positive
                        evaluation_mat['True Positive'] += 1
                        one_label = True
                    else:
                        # prediction negative, actually positive
                        evaluation_mat['False Negative'] += 1
                else:
                    if prediction[x][y] == 1:
                        # prediction positive, actually negative
                        evaluation_mat['False Positive'] += 1
                    else:
                        # both negative
                        evaluation_mat['True Negative'] += 1

            # check if at least one true pos
            if one_label:
                evaluation_mat['One Label'] += 1
            one_label = False

        # once all rows checked, use confusion matrix and one label /
        # perfect match counts to calculate other statistics
        stats = self.stats_calc(evaluation_mat['True Positive'],
                                evaluation_mat['True Negative'],
                                evaluation_mat['False Positive'],
                                evaluation_mat['False Negative'],
                                evaluation_mat['One Label'],
                                evaluation_mat['Perfect Match'],
                                cats=len(actual[0]))
        ret = {**evaluation_mat, **stats}
        return ret

    def predict(self, tweets):
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
            predictions[:, i] = self.classifiers[i].predict(addtl_feat)

        # if nothing predicted, category should be unknown
        for row in predictions:
            if np.sum(row) == 0:
                row[self.catadictionary['Unknown']] = 1
        return predictions

    def stats_calc(self, tp, tn, fp, fn, one_lab, perf_match, cats=25):
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
        t = n/cats
        ret['One Label Score'] = one_lab/t
        ret['Perfect Match Score'] = perf_match/t
        ret['Accuracy'] = (tp+tn)/n
        try:
            ret['Precision'] = tp/(tp+fp)
        except ZeroDivisionError:
            ret['Precision'] = 0
        try:
            ret['Recall'] = tp/(tp+fn)
        except ZeroDivisionError:
            ret['Recall'] = 0
        try:
            ret['F1 Score'] = (2*(ret['Precision']*ret['Recall']))/(ret['Precision']+ret['Recall'])
        except ZeroDivisionError:
            ret['F1 Score'] = 0
        return ret

    def category_indices(self):
        """
        Return dict of index to category, based on the catadict
        """
        ret = dict()
        for key in self.catadictionary:
            ret[self.catadictionary[key]] = key
        return ret

    def special_mats(self, mat):
        """
        Calculate knowledge and actionable confusion matrices from a category confusion matrix dict

        :param mat: a dictionary of conf matrices for categories as formed by self.mat_all_categories

        :return: dictionary of name to dict confusion matrix

        :raise ValueError: if any of the stats in self.actionable or self.knowledge don't appear in mat
        """
        act = {'Number of Predictions': 0,
               'True Positive': 0, 'True Negative': 0,
               'False Positive': 0, 'False Negative': 0}
        know = {'Number of Predictions': 0,
                'True Positive': 0, 'True Negative': 0,
                'False Positive': 0, 'False Negative': 0}
        for m in self.actionable:
            if m in mat:
                for stat in mat[m]:
                    act[stat] += mat[m][stat]
            else:
                raise ValueError("Incorrectly formed dictionary passed to calculate actionable stats.")
        for m in self.knowledge:
            if m in mat:
                for stat in mat[m]:
                    know[stat] += mat[m][stat]
            else:
                raise ValueError("Incorrectly formed dictionary passed to calculate knowledge stats.")
        return {'Actionable': act, 'Knowledge': know}