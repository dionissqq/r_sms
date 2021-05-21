from pymongo import MongoClient
import sched, time

from preprocessing import preprocess_tweet
from consts import DB_STRING, themes
from  data_extractor import get_tweets_by_hashtag

iterations = 0

s = sched.scheduler(time.time, time.sleep)
client = MongoClient(DB_STRING)
db=client.tweets

def do_something(sc, iterations): 
    print("Doing stuff...")
    print('iteration - ', iterations)
    # do your stuff
    for theme in themes:
        json_res = get_tweets_by_hashtag(theme, 100)
        for el in json_res['data']: 
            tweet = preprocess_tweet(el['text'])
            db[theme].update_one({'text':tweet},{"$set":{'text':tweet}}, upsert=True)

    if(iterations<10):
        s.enter(180, 1, do_something, (sc, iterations+1, ))

s.enter(0, 1, do_something, (s, iterations, ))
s.run()
