# import the necessary libraries 
import nltk 
import re
from nltk.tokenize import word_tokenize 
from nltk.corpus import stopwords 
from collections import Counter
import pickle as pckl

# Case folding
def text_lowercase(text): 
	return text.lower() 

# Remove special characters 
def remove_nonalphanum(text): 
	result = re.sub(r'[^\d\w\s\n\t]+', '', text) 
	return result 

# Remove stopwords
def remove_stopwords(text): 
	stop_words = set(stopwords.words("english")) 
	word_tokens = word_tokenize(text) 
	filtered_text = [word for word in word_tokens if word not in stop_words] 
	return ' '.join(filtered_text)
  
with open('corpus/Multi-core_processor.txt', 'r') as f:
	text = '\n'.join(f.readlines())

text = text_lowercase(text)
text = remove_nonalphanum(text)
text = remove_stopwords(text)

col = Counter(text.split())

print (len(col))

with open('count.pckl', 'wb') as f:
	pckl.dump(col, f)

print(text)



