# Required imports or library dependencies
import re, sys, json
from tweet_sentiment import *
import matplotlib.pyplot as plt
import operator


# Fill me.
# Details explained in class.
def gettopTenHashTags(tweets_file, n = 10):
    hashTagFreq = {}
    tweets_file = open(tweets_file)
        
    for tweet in tweets_file:
        tweet_json = json.loads(tweet)
        try:        
            hashtag = ((tweet_json['entities']['hashtags'])[0])['text'].lower() #.encode('utf-8')   # at first extracting a list which contains a dictionary
              # then by using [0] I am selecting first item of the list which is the dictionary 
              # now after having the dictionary I have used the dictionary key name text to extract
              # its value to hashtag
            #hashTagFreq[hashtag] = [hashTagFreq.get(hashtag, 0)+1]
            if hashtag not in hashTagFreq:
                hashTagFreq[hashtag] = 1
            else:
                hashTagFreq[hashtag] += 1
        except:
            pass


    sortedTags = sorted(hashTagFreq,
                        key=hashTagFreq.get,
                        reverse=True)
    #for item in sortedTags:
    #    print item, hashTagFreq[item] 
    return sortedTags[0:n], hashTagFreq
    
    
def plotFrequencyBar(freqDict):
    lists = sorted(freqDict.items(), key=operator.itemgetter(1), reverse=True)[0:10]
    terms, counts = zip(*lists)
    r = range(len(terms))
    plt.xticks(r, terms)
    plt.bar(r, counts, align='center')
    plt.show()

        
if __name__ == '__main__':    
    #gettopTenHashTags(sys.argv[1])
    toptenTags, hash_tag_dic = gettopTenHashTags(sys.argv[1])
    for item in toptenTags:
        print item, hash_tag_dic[item]    
    plotFrequencyBar(hash_tag_dic)
    
    
