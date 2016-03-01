import feedparser

import operator, pickle, itertools

from textblob import TextBlob

from collections import defaultdict


def tag_abs():

    """
    Collect together all words from abstracts according to their tag
    """

    #Open the array of feeds retrieved from arxiv

    with open('training_feeds.pickle') as f:
        feed_array = pickle.load(f)

    #Extract all summary data and compile
    #(Note: only first 5 feeds were non-empty)
    #This generates a list of lists for each feed
    feed_list = [list(entry.summary for entry in feed.entries) for feed in feed_array[0:6]]

    #Concatenate summaries form each feed into one large list
    #of all summaries
    summary_corpus = list(itertools.chain(*feed_list))

    #Pos_tag each summary
    #Use textblob for this as faster
    #Create textb   lobs for each summary

    summary_textblobs = [TextBlob(summary) for summary in summary_corpus]

    summary_postags = [tb.tags for tb in summary_textblobs]

    #Break down array of postags for each summary into words
    all_word_postags = list(itertools.chain(*summary_postags))


    import time

    t0 = time.time()

    #Arrange into dictionary with tags as keys
    #Note: think that TextBlob uses PennTreeBank tagset
    tags_dict = defaultdict(tuple)
    for tup in all_word_postags:
        tags_dict[tup[1]] += (tup[0],)

    t1 = time.time()

    print 'Time taken forming dictionary = %i' %(t1-t0)

    #Pickle tags dictionary (takes ~8mins to form):
    with open('tags_dict.pickle','w') as f:
        pickle.dump(tags_dict,f)

with open('tags_dict.pickle')as f:
    tagged_abs = pickle.load(f)


#Take a look at most common (and least common) words of each tag type

# Loop over tags used and inspect most and least common words to see which
# tags carry significant information contet

for tag_name in tagged_abs.keys():

    print ""
    print "%s: common/uncommon words" % (tag_name)
    #Form textblob from all VBD tagged words (formed into one long string first)
    tb = TextBlob(" ".join(tagged_abs[tag_name]))
    #Count occurence of each word
    num_w = sorted(tb.word_counts.items(), key=operator.itemgetter(1))
    print "10 most common: %s" % num_w[-10:]
    print "10 least common: %s" % num_w[:10]
