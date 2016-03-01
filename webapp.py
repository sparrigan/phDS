import feedparser

import urllib

#Form query
base_url = 'http://export.arxiv.org/api/query?'

search_query = 'co:phd+thesis'
start = 0
max_results = 100

query = 'search_query=%s&start=%i&max_results=%i' %(search_query,start,max_results)

#Hack to expose namespaces used by arxiv in feedparser
feedparser._FeedParserMixin.namespaces['http://a9.com/-/spec/opensearch/1.1/'] = 'opensearch'
feedparser._FeedParserMixin.namespaces['http://arxiv.org/schemas/atom'] = 'arxiv'

#GET request with constructed URL query
response = urllib.urlopen(base_url+query).read()

#Parse response to request with feedparser
feed = feedparser.parse(response)

#Note: code to save feed var to file using pickle
#to debug etc... without repeating requests to arxiv:
#import pickle
#with open('phdabs.pickle','w') as f:
#...     pickle.dump(feed,f)
#Retrieve pickled variables:
#with open('phdabs.pickle') as f:
#...     feed  = pickle.load(f)


#Loop through entries and print titles, author names
#and comments

import nltk

#Tokenize abstracts to give list of lists
token_words = [nltk.word_tokenize(entry.summary) for entry in feed.entries]

#REMOVE BY POS TAG FIRST
#Selecting words with given postag(s)
#[word_postag[0] for word_postag in aa if word_postag[1] == 'NN' or word_postag[1] == 'NNS']


#THEN GENERATE STOPWORD LIST BY ASSESSING MOST COMMON WORDS IN ALL ABSTRACTS COMBINED AND HUMAN-READING THESES TO SEE WHICH ARE MORE THESIS RELATED THAN TOPIC RELATED

#THEN USE PORTER STEMMING


#Eliminate any none-alpha and repeated words
#And also ignore stopwords based on nltk list
#NOTE: NEED TO COME BACK AND MAKE EXCPETIONS - EG
#HYPHENATED WORDS ETC...
from nltk.corpus  import stopwords
stopwords = stopwords.words('english')
not_stopwords = [set(word.lower() for word in entry if word.isalpha() and word not in stopwords) for entry in token_words]

#Run stemming algorithm to stem words - making them
#more easily comparable
from nltk.stem.porter import PorterStemmer

porter_stemmer = PorterStemmer()

stemmed_words = [porter_stemmer.stem(word) for word in entry for entry in not_stopwords]


for entry in feed.entries:
    print 'Title: %s' %entry.title
    #Note: should only have one author on thesis,
    #so don't unpack multiple authors
    print 'Author: %s' %entry.author
    #Allow for no comment (although should only have)
    #search results with non-null entries
    try:
        comment = entry.arxiv_comment
    except AttributeError:
        comment = 'No comment found'
    print 'Comments: %s' % comment
    print ''
