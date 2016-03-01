import feedparser

import urllib

import time

import pickle

feedparser._FeedParserMixin.namespaces['http://a9.com/-/spec/opensearch/1.1/'] = 'opensearch'
feedparser._FeedParserMixin.namespaces['http://arxiv.org/schemas/atom'] = 'arxiv'

wait_time = 3

#Array to store the different feeds we will get
feed_array = []

#Form query
base_url = 'http://export.arxiv.org/api/query?'

search_query = 'co:phd+thesis'

slice_size = 1000

#Note: Could be cleverer here, and on first pass of loop
#get opensearch metadata from first xml feed and look at
#opensearch_totalresults, which tells us how many results
#there are *altogether* and then only loop as high as we
#need in order to get them all.

for ii in range(0,10):
    start = ii*slice_size
    #Note: max_results is how many results - not end num
    max_results = slice_size
    query = 'search_query=%s&start=%i&max_results=%i' %(search_query,start,max_results)

    print "Initiating GET for results %i to %i" %(start,(ii+1)*max_results)

    #GET request with constructed URL query
    response = urllib.urlopen(base_url+query).read()

    feed_array.append(feedparser.parse(response))

    print "Added results to feed_array"

    # Remember to play nice and sleep a bit
    print 'Sleeping for %i seconds' % wait_time
    time.sleep(wait_time)


print "Saving results with pickle..."

with open('training_feeds.pickle','w') as f:
    pickle.dump(feed_array,f)

print "Results saved!"
