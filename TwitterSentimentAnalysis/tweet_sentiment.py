# Required imports or library dependencies
import re, sys, json


# Is the tweet in English?
# Use try and except clause
# If try works for english language tweet return true, else false
# Read Twitter Developer Documentation carefully
def isLang(tweet_json, lang='en'):
    try:  # Fill me  ....
        if tweet_json['lang'] == lang :
            return  True
    except:
        return False


# Create a sentiment dictionary
def genSentDict(sent_file):
    sent_file = open(sent_file)
    scores = {}

    for line in sent_file:
        term, score = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        scores[term] = int(score)  # Convert the score to an integer.

    return scores


# Get a English tweet
# Check for English Tweets
# input: tweet as json
# output: tweet terms as list

# Make sure to use unicode encode
# Use re.findall to get the tweet terms/words as list.
# Fill the rest.
# Details explained in class.
def getENTweet(tweet_json):
    
    if (isLang(tweet_json)):
        stringSentence = tweet_json['text'].encode('utf-8')
        tweet_terms_unsplited = stringSentence.lower()
        
        tweet_terms = tweet_terms_unsplited.split()  #converting to a list from string 
        #print(twee)
        return tweet_terms
    
    else:
        return []


# Get score from the tweet
# input: tweet as json, sentiment dictionary (hashmap and/or map, python dictionary)
# output: tweet score
# Fill the rest, details explained in class.
def getSentScoreOfTweet(tweet_json, sentDict):
    tweet_score = 0
    tweet_terms = getENTweet(tweet_json)
    
    if tweet_terms:    
        for term in tweet_terms :
            term = re.sub('[^A-Za-z]+', '', term)       #removing anything but a-z
            if term in sentDict:
                tweet_score=tweet_score+sentDict[term]
            else:
                tweet_score=tweet_score+0
        return tweet_score
    return None 

# Score the tweets in the tweets file
def getTweetScores(sentDict, tweets_file):
    tweets_file = open(tweets_file)
    sentDict = genSentDict(sentDict)

    for tweet in tweets_file:
        tweet_json = json.loads(tweet)

        try:
            score = getSentScoreOfTweet(tweet_json, sentDict)
            if score is not None:            
                print score

        except:
            pass


if __name__ == '__main__':
    getTweetScores(sys.argv[1], sys.argv[2])