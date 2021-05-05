import tweepy
import datetime
from parsers import parse_tweet_text


class Twitter(object):
    BASE_URL = "https://twitter.com"

    def __init__(self, client, secret, access_token_key, access_token_secret):
        if access_token_key is None or access_token_secret is None:
            auth = tweepy.AppAuthHandler(client, secret)
        else:
            auth = tweepy.OAuthHandler(client, secret)
            auth.set_access_token(access_token_key, access_token_secret)

        self.api = tweepy.API(auth)

    def get_tweets_by_user(self, user: str, since: int, until: int):
        page = 1
        parsed_tweets = []
        while True:
            tweets = self.api.user_timeline(user, page=page, tweet_mode="extended")

            for tweet in tweets:
                tweet_day = (datetime.datetime.now() - tweet.created_at).days
                if since <= tweet_day < until:
                    # Do processing here:
                    if (not tweet.retweeted) and ('RT @' not in tweet.full_text):
                        parse_tweet = parse_tweet_text(tweet.full_text)
                        parsed_tweets.append(parse_tweet)

                elif tweet_day > until:
                    return parsed_tweets
                # elif tweet_day < since:
                #     pass
            page += 1
