import re
import emoji
import string

def give_emoji_free_text(text):
    return emoji.get_emoji_regexp().sub(r'', text.decode('utf8'))

def preprocess_tweet(tweet):
    #delete tags, hashtags, new line, and links
    tweet = re.sub(r"http\S+|@\S+|#\S+|\n|\t", "", tweet)

    #delete emojies
    tweet = give_emoji_free_text(tweet.encode('utf8'))

    #delete unprintable characters
    printable = set(string.printable)
    tweet = ''.join(filter(lambda x: x in printable, tweet))

    #delete leading whitespaces
    tweet = tweet.lstrip() 
    return tweet