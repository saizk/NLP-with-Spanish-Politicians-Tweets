import tweepy


class Twitter(object):
    BASE_URL = "https://twitter.com"

    def __init__(self, client, secret, access_token_key, access_token_secret):
        if access_token_key is None or access_token_secret is None:
            auth = tweepy.AppAuthHandler(client, secret)
        else:
            auth = tweepy.OAuthHandler(client, secret)
            auth.set_access_token(access_token_key, access_token_secret)

        self.api = tweepy.API(auth)




