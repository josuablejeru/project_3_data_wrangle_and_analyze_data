"""
Gather each tweet's retweet count and favorite ("like") count and saves it to tweet.json
"""
__author__ = "Josua Blejeru"

import os
import sys
import pandas
import tweepy
import direnv
from rich import print
import json

direnv.load()
print(direnv.read())

BEARER_TOKEN = os.getenv('BEARER_TOKEN')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_KEY_SECRET = os.getenv('CONSUMER_KEY_SECRET')


def extract_data(input_dict: dict) -> dict:
    data = dict()
    data['retweet_count'] = input_dict.get('retweet_count')
    data['favorite_count'] = input_dict.get('favorite_count')
    data['id'] = input_dict.get('id')

    return data


def append_json(data):
    with open('tweets.json', 'a') as f:
        json.dump(data, f)


def main():
    """ grab and save all informations about twitter data """
    df = pandas.read_csv('./twitter-archive-enhanced.csv')

    auth = tweepy.OAuthHandler(consumer_key=CONSUMER_KEY,
                               consumer_secret=CONSUMER_KEY_SECRET)

    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth=auth)

    total_length = len(df.tweet_id)

    # last query from 1763
    for index, tweet_id in df.tweet_id.items():
        try:
            resp = api.get_status(tweet_id, tweet_mode='extended')
            data = extract_data(resp._json)
            append_json(data)
            print(f"{index} of {total_length} queried")
        except tweepy.HTTPException:
            continue
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    main()
