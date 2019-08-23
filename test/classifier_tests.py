import unittest
import sys
from sklearn.base import is_classifier
import numpy as np
from sklearn.naive_bayes import BernoulliNB
from sklearn.ensemble import RandomForestClassifier

sys.path.insert(0, '../..')
sys.path.insert(0, '../classifier')

from classifier.Classify_with_evaluation import Classify

class TestClassifier(unittest.TestCase):

    # test loading pretrained classifiers
    # note: must actually have pretrained classifiers
    # in classifier/pretrained
    def test_load_pretrained(self):
        c = Classify(pretrained = '../classifier/pretrained/')

        # check there classifiers loaded
        self.assertIsNotNone(c.classifiers)
        self.assertTrue(len(c.classifiers))
        for classifier in c.classifiers:
            self.assertTrue(is_classifier(classifier))

        # check that vectorizer loaded
        self.assertIsNotNone(c.vectorizer)

    # check the simple evaluation method works as intended
    def test_simple_eval(self):
        base = np.array([[0, 1, 0, 0, 0],
                         [0, 1, 0, 0, 1],
                         [1, 0, 0, 1, 0],
                         [1, 0, 0, 1, 0],
                         [1, 1, 1, 1, 1]])
        perf = base
        close = np.array([[0, 1, 0, 1, 0],
                          [0, 1, 0, 0, 1],
                          [1, 0, 0, 1, 0],
                          [1, 0, 0, 1, 0],
                          [0, 0, 0, 0, 0]])
        worst = np.array([[1, 0, 1, 1, 1],
                          [1, 0, 1, 1, 0],
                          [0, 1, 1, 0, 1],
                          [0, 1, 1, 0, 1],
                          [0, 0, 0, 0, 0]])
        one_match_all = np.array([[1, 1, 1, 1, 1],
                                  [1, 1, 1, 1, 0],
                                  [0, 1, 1, 1, 1],
                                  [1, 1, 1, 0, 1],
                                  [0, 0, 0, 0, 1]])

        c = Classify(pretrained='../classifier/pretrained/')

        # check perfect prediction
        t = c.evaluate(base, perf)

        keys = ['Number of Predictions',
                'True Positive', 'True Negative',
                'False Positive', 'False Negative',
                'One Label', 'Perfect Match',
                'One Label Score', 'Perfect Match Score',
                'Accuracy', 'Precision', 'Recall',
                'F1 Score']
        self.assertTrue(all(key in t.keys() for key in keys))
        self.assertTrue(all([
            t['Number of Predictions'] == 25,
            t['True Positive'] == 12,
            t['True Negative'] == 13,
            t['False Positive'] == 0,
            t['False Negative'] == 0,
            t['One Label'] == 5,
            t['Perfect Match'] == 5,
            t['One Label Score'] == 1,
            t['Perfect Match Score'] == 1,
            t['Accuracy'] == 1,
            t['Precision'] == 1,
            t['Recall'] == 1,
            t['F1 Score'] == 1]))

        # test imperfect predictions
        t = c.evaluate(base, close)
        self.assertTrue(all([
            t['Number of Predictions'] == 25,
            t['True Positive'] == 7,
            t['True Negative'] == 12,
            t['False Positive'] == 1,
            t['False Negative'] == 5,
            t['One Label'] == 4,
            t['Perfect Match'] == 3,
            t['One Label Score'] == 4/5,
            t['Perfect Match Score'] == 3/5,
            t['Accuracy'] == 19/25,
            t['Precision'] == 7/8,
            t['Recall'] == 7/12,
            t['F1 Score'] ==
            2*t['Precision']*t['Recall']/(t['Precision'] + t['Recall'])]))

        # check all predictions wrong
        t = c.evaluate(base, worst)
        self.assertTrue(all([
            t['Number of Predictions'] == 25,
            t['True Positive'] == 0,
            t['True Negative'] == 0,
            t['False Positive'] == 13,
            t['False Negative'] == 12,
            t['One Label'] == 0,
            t['Perfect Match'] == 0,
            t['One Label Score'] == 0,
            t['Perfect Match Score'] == 0,
            t['Accuracy'] == 0,
            t['Precision'] == 0,
            t['Recall'] == 0,
            t['F1 Score'] == 0]))

        # check 1 for each row
        t = c.evaluate(base, one_match_all)
        self.assertTrue(all([
            t['Number of Predictions'] == 25,
            t['True Positive'] == 5,
            t['True Negative'] == 0,
            t['False Positive'] == 13,
            t['False Negative'] == 7,
            t['One Label'] == 5,
            t['Perfect Match'] == 0,
            t['One Label Score'] == 1,
            t['Perfect Match Score'] == 0]))

    # test mapid function
    def test_mapid(self):
        c = Classify(pretrained='../classifier/pretrained/')
        self.assertEqual(c.map_id(['GoodsServices']), [0])
        self.assertEqual(c.map_id(['Irrelevant']), [22])
        self.assertEqual(c.map_id(['Unknown']), [23])
        self.assertEqual(c.map_id(['fake']), list())
        self.assertEqual(c.map_id(['MultimediaShare',
                                   'InformationWanted',
                                   'PastNews', 'Hashtags']),
                         [11, 2, 17, 16])

    # test constructor if not pretrained without given model
    def test_creation_no_model(self):
        tweets = ['this is a test', 'tweet tweet test', 'testing tweet']
        cats = [[1, 0, 0, 1], [1, 1, 0, 0], [1, 1, 0, 0]]
        c = Classify(tweets, cats)
        self.assertEqual(tweets, c.text)
        self.assertEqual(cats, c.cat)
        self.assertIsInstance(c.model, BernoulliNB)
        self.assertIsNotNone(c.vectorizer)
        self.assertIsNotNone(c.classifiers)
        self.assertGreater(len(c.classifiers), 0)
        self.assertIsInstance(c.classifiers[0], BernoulliNB)
        for classifier in c.classifiers:
            self.assertTrue(is_classifier(classifier))

    # test constructor if not pretrained without given model
    def test_creation_with_model(self):
        tweets = ['this is a test', 'tweet tweet test', 'testing tweet']
        cats = [[1, 0, 0, 1], [1, 1, 0, 0], [1, 1, 0, 0]]
        c = Classify(tweets, cats, model = RandomForestClassifier())
        self.assertEqual(tweets, c.text)
        self.assertEqual(cats, c.cat)
        self.assertIsInstance(c.model, RandomForestClassifier)
        self.assertIsNotNone(c.vectorizer)
        self.assertIsNotNone(c.classifiers)
        self.assertGreater(len(c.classifiers), 0)
        self.assertIsInstance(c.classifiers[0], RandomForestClassifier)
        for classifier in c.classifiers:
            self.assertTrue(is_classifier(classifier))

    # test special_mat function
    def test_special_mats(self):
        c = Classify(pretrained='../classifier/pretrained/')

        # no predictions
        d0 = dict()
        for key in c.catadictionary.keys():
            d0[key] = {'Number of Predictions': 0,
                'True Positive': 0, 'True Negative': 0,
                'False Positive': 0, 'False Negative': 0}
        res0 = {'Actionable': {'Number of Predictions': 0,
                              'True Positive': 0,
                              'True Negative': 0,
                              'False Positive': 0,
                              'False Negative': 0},
               'Knowledge': {'Number of Predictions': 0,
                             'True Positive': 0,
                             'True Negative': 0,
                             'False Positive': 0,
                             'False Negative': 0}}
        self.assertEqual(c.special_mats(d0), res0)


        # all correct
        d1 = dict()
        for key in c.catadictionary.keys():
            d1[key] = {'Number of Predictions': 10,
                       'True Positive': 5, 'True Negative': 5,
                       'False Positive': 0, 'False Negative': 0}
        res1 = {'Actionable': {'Number of Predictions': 30,
                               'True Positive': 15,
                               'True Negative': 15,
                               'False Positive': 0,
                               'False Negative': 0},
                'Knowledge': {'Number of Predictions': 50,
                              'True Positive': 25,
                              'True Negative': 25,
                              'False Positive': 0,
                              'False Negative': 0}}
        self.assertEqual(c.special_mats(d1), res1)

        # all wrong
        d2 = dict()
        for key in c.catadictionary.keys():
            d2[key] = {'Number of Predictions': 10,
                       'True Positive': 0, 'True Negative': 0,
                       'False Positive': 5, 'False Negative': 5}
        res2 = {'Actionable': {'Number of Predictions': 30,
                               'True Positive': 0,
                               'True Negative': 0,
                               'False Positive': 15,
                               'False Negative': 15},
                'Knowledge': {'Number of Predictions': 50,
                              'True Positive': 0,
                              'True Negative': 0,
                              'False Positive': 25,
                              'False Negative': 25}}
        self.assertEqual(c.special_mats(d2), res2)


        # mixed
        d3 = d1.copy()
        d3['SearchAndRescue'] = {'Number of Predictions': 10,
                                 'True Positive': 7, 'True Negative': 0,
                                 'False Positive': 2, 'False Negative': 1}
        d3['InformationWanted'] = {'Number of Predictions': 10,
                                   'True Positive': 1, 'True Negative': 3,
                                   'False Positive': 3, 'False Negative': 3}
        d3['Official'] = {'Number of Predictions': 10,
                          'True Positive': 7, 'True Negative': 0,
                          'False Positive': 2, 'False Negative': 1}
        d3['MultimediaShare'] = {'Number of Predictions': 10,
                                 'True Positive': 1, 'True Negative': 3,
                                 'False Positive': 3, 'False Negative': 3}
        res3 = {'Actionable': {'Number of Predictions': 30,
                               'True Positive': 13,
                               'True Negative': 8,
                               'False Positive': 5,
                               'False Negative': 4},
                'Knowledge': {'Number of Predictions': 50,
                              'True Positive': 23,
                              'True Negative': 18,
                              'False Positive': 5,
                              'False Negative': 4}}
        self.assertEqual(c.special_mats(d3), res3)

        # test error
        d4 = d1.copy()
        del d4['Official']
        self.assertRaises(ValueError, c.special_mats, d4)
        d5 = d1.copy()
        del d5['SearchAndRescue']
        self.assertRaises(ValueError, c.special_mats, d5)

    # test category_indicis
    def test_category_indices(self):
        c = Classify(pretrained='../classifier/pretrained/')
        r = {0: 'GoodsServices', 1: 'SearchAndRescue', 2: 'InformationWanted', 3: 'Volunteer',
             4: 'Donations', 5: 'MovePeople', 6: 'FirstPartyObservation', 7: 'ThirdPartyObservation',
             8: 'Weather', 9: 'EmergingThreats', 10: 'SignificantEventChange', 11: 'MultimediaShare',
             12: 'ServiceAvailable', 13: 'Factoid', 14: 'Official', 15: 'CleanUp', 16: 'Hashtags',
             17: 'PastNews', 18: 'ContinuingNews', 19: 'Advice', 20: 'Sentiment', 21: 'Discussion',
             22: 'Irrelevant', 23: 'Unknown', 24: 'KnownAlready'}
        self.assertEqual(c.category_indices(), r)




if __name__ == '__main__':
    unittest.main()