import re, sys, json
from tweet_sentiment import *
import matplotlib.pyplot as plt
import operator

# Fill the rest
# Details explained in class.
# Input: The downloaded tweets file
# Output: The freq dictionary {key: tweet terms, value: frequency as probability}
def frequency(tweets_file):
    freq = {}
    tweets_file = open(tweets_file)
    all_term = 0.0    
    
    for tweet in tweets_file:
        tweet_json = json.loads(tweet)
        tweet_terms = getENTweet(tweet_json)
        if tweet_terms:  
            for term in tweet_terms:
                all_term = all_term+1
                term = re.sub('[^A-Za-z]+', '', term) 
                term = term.lower()
                #freq[term] = freq.get(term,0)+1.0       #The dict's get() method takes an optional second parameter that can be used to provide a default value if the requested key is not found
                if term not in freq:
                    freq[term] = 1
                else:
                    freq[term] += 1                
                freq[term] = 1.0*freq[term]/all_term
        
    
    return freq

def printFrequency(freqDict):
    sortedTags = sorted(freqDict, key=freqDict.get,  reverse=True)
    for term in sortedTags[0:20]:
        print term, freqDict[term]
#    for key in freqDict.keys():
#        if freqDict[key]:
#            print("%s %.8f" % ( key, freqDict[key] ) )   

def plotFrequencyBar(freqDict):
    lists = sorted(freqDict.items(), key=operator.itemgetter(1), reverse=True)[0:10]
    terms, counts = zip(*lists)
    r = range(len(terms))
    plt.xticks(r, terms)
    plt.bar(r, counts, align='center')
    plt.show()

if __name__ == '__main__':
    printFrequency(frequency(sys.argv[1]))
    plotFrequencyBar(frequency(sys.argv[1]))


#https://pythonprogramming.net/python-matplotlib-live-updating-graphs/