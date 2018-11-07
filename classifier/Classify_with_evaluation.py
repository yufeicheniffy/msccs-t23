import sys
sys.path.insert(0, './data_files_scripts')

from sklearn.naive_bayes import BernoulliNB
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
import numpy as np
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import accuracy_score
import pandas as pd


class Classify:
    """
    A classifier which pulls tweet data from the mongodb database.
    """

    def __init__(self, cats, tweet_texts, vocab_size):
        """
        Create and train classifier.
        """
        self.cat = cats
        self.text = tweet_texts
        self.cat_arr = np.array(self.cat)

        self.vectorizer = CountVectorizer(stop_words=stopwords.words(),
            binary=True, max_features=vocab_size)
        self.vect_train = self.vectorizer.fit_transform(self.text)

        print(self.vectorizer.get_feature_names())


        self.classifiers = list()
        self.train()


    def train(self):
        """
        Fits classifiers to the training data we already have.
        """
        #len(categories)
        for i in range(0, len(self.cat_arr[0])):
            c = BernoulliNB().fit(self.vect_train, self.cat_arr[:,i])
            self.classifiers.append(c)

        print("Training complete!")

    #retrieves the index of category eg 0 = 'Advice'
    def map_id(self,category):
        returner = []
        for c in category:
            for i in range(0,len(self.categories)):
                if(c == self.categories[i]):
                    returner.append(i)
        return returner

#   input ytest_array,and X_test
    def evaluation_(self,ytest_array,predict):
        listdic = []
        data_v = []
        #y_test_arr = self.create_binary_category(ytest_array)
        y_test_arr = np.array(ytest_array)
        print(y_test_arr)
        print(sum(y_test_arr))
        print(type(y_test_arr))
        for i in range(0,len(self.categories)):
            listdic.append({"Category": self.categories[i], "Accuracy": accuracy_score(y_test_arr[:,i],predict[:,i]), "Recall": recall_score(y_test_arr[:,i],predict[:,i],pos_label=1), "Preccision": precision_score(y_test_arr[:,i],predict[:,i],pos_label=1), "F1score":f1_score(y_test_arr[:,i],predict[:,i],pos_label=1)})
            data_v.append(accuracy_score(y_test_arr[:,i],predict[:,i]))
            data_v.append(recall_score(y_test_arr[:,i],predict[:,i],pos_label=1))
            data_v.append(precision_score(y_test_arr[:,i],predict[:,i],pos_label=1))
            data_v.append(f1_score(y_test_arr[:,i], predict[:,i], pos_label=1))

        data_v = np.array(data_v)
        data_v = data_v.reshape(25,4)
        data_frame = pd.DataFrame(data=data_v, index=np.array(self.categories),columns=np.array(['Accuracy', 'Precision', 'Recall', 'F1 Score']))
        #print(data_frame)
        data_frame.to_csv('evaluation.csv', sep='\t')
        return data_frame


    def simple_evaluation(self, actual, prediction):
        true_pos = 0
        true_neg = 0
        false_pos = 0
        false_neg = 0
        for x in range(0, len(actual)):
            for y in range(0, len(actual[x])):
                if actual[x][y] == 1:
                    if prediction[x][y] == 1:
                        true_pos += 1
                    else: 
                        false_neg +=1
                else:
                    if prediction[x][y] == 1:
                        false_pos += 1
                    else:
                        true_neg += 1
        print("true positive ", true_pos)
        print("false positive ", false_pos)
        print("true negative ", true_neg)
        print("false negative ", false_neg)
        print("overall accuracy ", (true_pos+true_neg)/(true_pos+true_neg+false_pos+false_neg))
        print("overall recall ", true_pos/(true_pos+false_neg))
        print("overall precision ", true_pos/(true_pos+false_pos))

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
        return(predictions)
