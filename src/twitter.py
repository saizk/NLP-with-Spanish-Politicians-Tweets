import time
import tweepy
import datetime


class Twitter(object):
    BASE_URL = "https://twitter.com"

    def __init__(self, client, secret, access_token_key, access_token_secret):
        if access_token_key is None or access_token_secret is None:
            auth = tweepy.AppAuthHandler(client, secret)
        else:
            auth = tweepy.OAuthHandler(client, secret)
            auth.set_access_token(access_token_key, access_token_secret)

        self.api = tweepy.API(auth,  retry_count=5, wait_on_rate_limit=True)

    def get_users_by_name(self, user: str):
        return self.api.search_users(user)

    def get_tweets_by_user(self, user: str, since: int, until: int):
        page = 1
        parsed_tweets = []
        while True:
            tweets = self.api.user_timeline(user, page=page, tweet_mode="extended")
            for tweet in tweets:
                tweet_day = (datetime.datetime.now() - tweet.created_at).days

                if since <= tweet_day < until:
                    if (not tweet.retweeted) and ('RT @' not in tweet.full_text):
                        parsed_tweets.append(tweet)

                elif tweet_day > until:
                    return parsed_tweets
                # elif tweet_day < since:
                #     pass
            page += 1
