import unittest
import sys
from sklearn.base import is_classifier
import numpy as np

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
        t = c.simple_evaluation(base, perf)

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
        t = c.simple_evaluation(base, close)
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
        t = c.simple_evaluation(base, worst)
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
        t = c.simple_evaluation(base, one_match_all)
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

    # test constructor if not pretrained
    def test_creation(self):



if __name__ == '__main__':
    unittest.main()