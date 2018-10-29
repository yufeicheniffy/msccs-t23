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
		remove repeated words, twitter handles.
		"""
		tokenized = self.tokenize(text)
		#print(tokenized)
		print(type(tokenized))

		# remove stopwords
		no_stopwords = [x for x in tokenized if not x in corp.stopwords.words()]

		# remove repeated words
		no_repeats = list(set(no_stopwords))


		print(no_repeats)
		return no_repeats


