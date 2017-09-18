# Required imports or library dependencies
import re, sys, json
from tweet_sentiment import *
from scipy.interpolate import interp1d


MAX_VALUE = 5

# Generate predicted Sentiment Dictionary from tweet score and unknown tweet terms.
# May want to use try except block
# The predSentDict updates automatically that is why we do not return anything.
# Fill the rest, details explained in class.
def genPredSentDict(score, numTerms, uTerms, predSentDict):    
    for uTerm in uTerms:
        try:
            result,number = predSentDict[uTerm]
            result = result+score
            number = number+numTerms
            predSentDict[uTerm] = [result,number]
            #print(type(uTerm))
            #predSentDict[uTerm] = ((1.0*score)/numTerms)*5
            # Fill me. done
        except: predSentDict[uTerm] = [score, numTerms]
        

# Analyse The tweet
# Input: Tweet terms as list, and the sentiment dictionary - hashmap/map
# Output: tweet score, unknown terms as a set data structure.
# Fill the rest. 
# Details explained in class.
def tweetAnalysis(tweet_terms, sentDict):    
    tweet_score = 0
    unknown_terms = set()    
    for term in tweet_terms:
        if term in sentDict:
            tweet_score = tweet_score + sentDict[term]
        else:
            term = re.sub('[^A-Za-z]+', '', term)
            unknown_terms.add(term)     #adding unknown term to set unknown_terms
	# Fill me.
    #done
    return tweet_score, unknown_terms


# Refine the new sentiment dicionary!
# Details explained in class.
# Update the new sentiment dictionary, therefore no explicit return
# Fill the rest.
def refinePredSentDict(newSentDict):
    #print(newSentDict.keys())
    for key in newSentDict.keys():
        score, numTerms = newSentDict[key]
        absuluteScore = abs(score)
        mapping = interp1d([-(MAX_VALUE*numTerms),(MAX_VALUE*numTerms)],[-MAX_VALUE,MAX_VALUE])     #mapping a range to another range
        score = 1.0 * mapping(score)        #making array(something value) to something value
        numTerms = 1        
        newSentDict[key] = [score,numTerms]
        pass
        
	# fill me.


def printSentDict(sentDict):
    for key in sentDict.keys():
        value, numTerms = sentDict[key]
        print("%s %.8f" % (key, value))


def initPredSentDict(sentDict, tweets_file):
    newSentDict = {}    
    tweets_file = open(tweets_file)
    sentDict = genSentDict(sentDict)    #ei line kn korlo ???? sentDict to agei silo
    
    for tweet in tweets_file:
        tweet_json = json.loads(tweet)
        tweet_terms = getENTweet(tweet_json)

        nTerms = len(tweet_terms)
        score, uTerms = tweetAnalysis(tweet_terms, sentDict)
        genPredSentDict(score, nTerms, uTerms, newSentDict)        
        
    return newSentDict


def getPredSentDict(sentDict, tweets_file):
    predDict = initPredSentDict(sentDict, tweets_file)
    refinePredSentDict(predDict)
    return predDict


if __name__ == '__main__':
    predDict = getPredSentDict(sys.argv[1], sys.argv[2])
    printSentDict(predDict)