import os
from dotenv import load_dotenv
import tweepy
load_dotenv()

bearer_token = os.getenv('TWITTER_BEARER_TOKEN')


auth = tweepy.OAuth2BearerHandler("Bearer Token here")
api = tweepy.API(auth)


tweets = api.home_timeline(count=1)
for tweet in tweets:
    print(tweet.text)
