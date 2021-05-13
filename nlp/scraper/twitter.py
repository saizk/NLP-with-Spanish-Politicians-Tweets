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

    def get_users_by_name(self, user: str, count: int = 5):
        return self.api.search_users(user, count=count)

    def get_twitter_by_name(self, user: str, min_followers: int = 50, is_verified: bool = False):
        users = self.get_users_by_name(user)
        twitter = None
        if users:
            for user in users:
                verify_cond = (user.verified == is_verified) if is_verified else True
                if user.followers_count > min_followers and verify_cond:
                    twitter = user.screen_name
                    break
        return twitter

    def get_followers(self, user: str, count: int = 100, **kwargs):
        return self.api.followers(screen_name=user, count=count, **kwargs)

    def get_user_timeline(self, user: str, page: int = 1, tweet_mode="extended", **kwargs):
        return self.api.user_timeline(user, page=page, tweet_mode=tweet_mode, **kwargs)

    def get_tweets_by_user(self, user: str, since: int = 0, until: int = 30, last_n_months: int = 1):
        page = 1
        parsed_tweets = []
        while True:
            tweets = self.get_user_timeline(user, page=page)
            for tweet in tweets:
                tweet_day = (datetime.datetime.now() - tweet.created_at).days

                if since <= tweet_day < last_n_months * until:
                    if (not tweet.retweeted) and ('RT @' not in tweet.full_text):
                        parsed_tweets.append(tweet)

                elif tweet_day > last_n_months * until:
                    return parsed_tweets
                # elif tweet_day < since:
                #     pass
            page += 1
