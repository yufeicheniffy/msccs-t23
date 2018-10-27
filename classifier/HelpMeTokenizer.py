import nltk
import nltk.corpus as corp
from nltk.tokenize import TweetTokenizer


class HelpMeTokenizer(TweetTokenizer):

	def __init__(self):
		# can try adjusting constructor if we're not getting decent results.
		super(HelpMeTokenizer, self).__init__(preserve_case=False, reduce_len=True, strip_handles=True)

	def process(self, text):
		"""
		Tokenize tweet, remove stopwords, 
		twitter handles.
		"""
		tokenized = self.tokenize(text)
		#print(tokenized)
		

