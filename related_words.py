"""
counters
dictionary
key = word
value = counter that includes all words that have appeared in the same sentence , across all documents
"""
import string
from nltk.tokenize import sent_tokenize
import pickle
from collections import Counter

with open('short.txt','r') as file:
    paragraphs = file.readlines()

with open('stopwords.txt','r') as file:
    stopwords = file.readlines()
    stopwords = [i.strip() for i in stopwords]

table = str.maketrans({key: None for key in string.punctuation})

sentences = [[i.lower().translate(table) for i in sent_tokenize(p)] for p in paragraphs]
text = [[[k for k in j.split() if k not in stopwords] for j in p] for p in sentences]

store = {}

for paragraph in text:
    for sentence in paragraph:
        c = Counter(sentence)
        for word in sentence:
            store[word] = store.setdefault(word, Counter()) + c

# with open('counters.pickle','wb') as file:
#     pickle.dump(store, file)
