# Idea
# A normal human can read 200 - 250 words per minute. Depending upon the difficulty level of the text.
# I'm defining difficulty to read as: rare_words/common_words. It's a ratio therefor larger value will mean more difficulty.
# I will take gutenberg corpora's words frequency distribution.
# Words with frequency more than 25 will be considered as common. While the rest will be considered as rare words.
# Read time will be a function of difficulty*level of number of words per minute output as hours and mins.

# Question and Objective
# write a program to analyse nltk gutenberg data
# aim is to write an 1-3 step algorithm which can estimate reading time of a book depending on the difficulty level

from nltk.corpus import gutenberg

# list all the files (books) available in the Gutenberg corpus
books = gutenberg.fileids()
print("Number of books {}".format(len(books)))
# Number of books 18

# read books from the data
gutenbergdict = { i:gutenberg.raw(i) for i in books}

# create corpora
gutenbergcorpora = ""
for i,j in gutenbergdict.items():
    gutenbergcorpora+=" "+j

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# tokenize the corpora
gutenbergwords = word_tokenize(gutenbergcorpora)

# Get the set of English stopwords
stopwords = set(stopwords.words('english'))
print("Number of stop words {}".format(len(stopwords)))
# Number of stop words 179

from nltk.probability import FreqDist

# Remove stopwords, small words and numbers from the tokenized words
def nostopwords(listofwords):
    return [word.lower() for word in listofwords if word.lower() not in stopwords and len(word)>2 and not word.isnumeric()]

gutenbergwords = nostopwords(gutenbergwords)
# create frequency distribution of the word
wordfreq = FreqDist(gutenbergwords)

print("Number of unique words {}".format(len(wordfreq)))
# Number of unique words 52410

# sort the word frequency
def sortedfreqdist(freqdistdict):
    return {k: v for k, v in sorted(freqdistdict.items(), key=lambda item: item[1], reverse=True)}

# create common and rare words list
common, rare = [], []
for i,j in sortedfreqdist(wordfreq).items():
    if j >= 25:
        common.append(i)
    else:
        rare.append(i)

print("Number of rare words {}".format(len(rare)))
# Number of rare words 46911
print("Number of common words {}".format(len(common)))
# Number of common words 5499

# get the ratio of rare words upon common words by dividing total rare words found with total common words found
def rareandcommonratio(gutenbergbook,common=common,rare=rare):
    tokenizedbook=word_tokenize(gutenbergbook)
    countrare, countcommon = 0, 0
    l=len(tokenizedbook)
    for i in tokenizedbook:
        if i in common:
            countcommon+=1
    countrare = l - countcommon
    return (countrare/countcommon,l)

ratios=[]
# loop over books to get their ratios
for i,j in gutenbergdict.items():
    ratio = rareandcommonratio(j)
    print("Name of the book: {} and its ratio {}".format(i,round(ratio[0],3)))    
    ratios.append((i,ratio[0], ratio[1] ))
# Name of the book - austen-emma.txt and its ratio 2.524
# Name of the book - austen-persuasion.txt and its ratio 2.455
# Name of the book - austen-sense.txt and its ratio 2.431
# Name of the book - bible-kjv.txt and its ratio 2.117
# Name of the book - blake-poems.txt and its ratio 2.133
# Name of the book - bryant-stories.txt and its ratio 2.345
# Name of the book - burgess-busterbrown.txt and its ratio 2.571
# Name of the book - carroll-alice.txt and its ratio 2.58
# Name of the book - chesterton-ball.txt and its ratio 2.447
# Name of the book - chesterton-brown.txt and its ratio 2.457
# Name of the book - chesterton-thursday.txt and its ratio 2.414
# Name of the book - edgeworth-parents.txt and its ratio 2.617
# Name of the book - melville-moby_dick.txt and its ratio 2.631
# Name of the book - milton-paradise.txt and its ratio 2.331
# Name of the book - shakespeare-caesar.txt and its ratio 4.376
# Name of the book - shakespeare-hamlet.txt and its ratio 4.479
# Name of the book - shakespeare-macbeth.txt and its ratio 4.581
# Name of the book - whitman-leaves.txt and its ratio 2.757

# mapping ratio to hypothetical read speeds
#  250 words = 2.10-2.29
#  240 words = 2.30-2.39
#  220 words = 2.40-2.49
#  210 words = 2.50-2.79
#  200 words = 2.80-2.89
#  190 or less = above 2.90

import datetime

readtime=[]
for i in ratios:
    if i[1] <= 2.29:
        mins = i[2]/250        
    elif 2.30<=i[1]<=2.39:
        mins = i[2]/240
    elif 2.40<=i[1]<=2.49:
        mins = i[2]/220
    elif 2.50<=i[1]<=2.79:
        mins = i[2]/210
    elif 2.80<=i[1]<=2.89:
        mins = i[2]/200
    else:
        mins = i[2]/190
    # convert minutes to read time
    readtime = str(datetime.timedelta(minutes = mins))
    print("Read time of {} is {}.".format(i[0],readtime))
# Read time of austen-emma.txt is 15:13:15.714286.
# Read time of austen-persuasion.txt is 7:25:04.909091.
# Read time of austen-sense.txt is 10:42:37.090909.
# Read time of bible-kjv.txt is 2 days, 15:07:14.880000.
# Read time of blake-poems.txt is 0:32:57.360000.
# Read time of bryant-stories.txt is 3:51:46.
# Read time of burgess-busterbrown.txt is 1:28:17.714286.
# Read time of carroll-alice.txt is 2:39:29.714286.
# Read time of chesterton-ball.txt is 7:22:01.090909.
# Read time of chesterton-brown.txt is 6:28:27.818182.
# Read time of chesterton-thursday.txt is 5:15:31.090909.
# Read time of edgeworth-parents.txt is 16:35:50.571429.
# Read time of melville-moby_dick.txt is 20:14:25.142857.
# Read time of milton-paradise.txt is 6:38:49.
# Read time of shakespeare-caesar.txt is 2:12:54.
# Read time of shakespeare-hamlet.txt is 3:11:25.894737.
# Read time of shakespeare-macbeth.txt is 1:57:00.947368.
# Read time of whitman-leaves.txt is 11:50:28.857143.