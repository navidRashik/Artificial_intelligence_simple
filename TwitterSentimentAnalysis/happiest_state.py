# Required imports or library dependencies
import re, sys, json
from tweet_sentiment import *
from stateDict import getStatesDict
import matplotlib.pyplot as plt
import operator


# Is the tweet from a certain country?
def isCountry(tweet_json, country = 'United States'):
    try: return tweet_json['place']['country'] == country
    except: return False
    


# Gets the state (cond. USA) info of the tweet.
def getUSAStateABV(tweet_json):
    try:
        placeInfo = tweet_json['place']['full_name']        
        stateABV = getStateFromPlace(placeInfo)
        return stateABV
    except: ''


# Is the state in the United States?
# Returns true flase.
# Fill me
def isStateInUSA(tweet_json, stateList):            #statelist is a dictionary
    try:
        if isGeoEnabled(tweet_json) and isCountry(tweet_json):
            search_state_full_name = tweet_json['place']['name']
            for state_short_name , state_full_name in stateList.iteritems():
                if state_full_name == search_state_full_name:
                    return True                    
                    #print state_short_name
       
    except: return False
    return False

# Is the tweet geo coded?
def isGeoEnabled(tweet_json):
    return tweet_json['user']['geo_enabled']

def plotFrequencyBar(freqDict):
    lists = sorted(freqDict.items(), key=operator.itemgetter(1), reverse=True)[0:10]
    terms, counts = zip(*lists)
    r = range(len(terms))
    plt.xticks(r, terms)
    plt.bar(r, counts, align='center')
    plt.show()
# Fill the rest.
# Details explained in class
def mostHappyUSState(sentDict, tweets_file):
    stateSenti = {}
    statesList = getStatesDict()    #this is a dictionary
    tweets_file = open(tweets_file)
    sentDict = genSentDict(sentDict)    
        
    for tweet in tweets_file:
        tweet_json = json.loads(tweet)  
        
        try:
            score = getSentScoreOfTweet(tweet_json, sentDict)
            if score is not None and isStateInUSA(tweet_json, statesList): 
                stateName = tweet_json['place']['name'].encode('utf-8')
                #stateSenti[stateName] = [stateSenti.get(stateName, 0)+score]
                if stateName not in stateSenti:
                    stateSenti[stateName] = score
                else:
                    stateSenti[stateName] += score
                #stateSenti[stateName] = [stateSenti.get(stateName, 0)+score,stateSenti.get(stateName, 0)+1] #1st parameter total score 2nd parameter amount of tweet
                #print stateSenti
        except:
            pass
    plotFrequencyBar(stateSenti)
    sortedList = sorted(stateSenti,key= stateSenti.get, reverse=True)  
    for item in sortedList:    
        print item,  stateSenti[item]
    
    


       
if __name__ == '__main__':
    mostHappyUSState(sys.argv[1], sys.argv[2])
