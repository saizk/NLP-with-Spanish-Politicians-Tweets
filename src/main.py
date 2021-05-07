import os
import models
from pprint import pprint
from config import *
from twitter import Twitter
from parsers import wiki_parser


# API_KEY = os.environ.get("API_KEY")
# API_SECRET_KEY = os.environ.get("API_SECRET_KEY")
# BEARER_TOKEN = os.environ.get("BEARER_TOKEN")
# ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
# ACCESS_TOKEN_KEY = os.environ.get("ACCESS_TOKEN_KEY")


def create_politics(db, politics, bot):
    for idx, (pol, party) in enumerate(politics):
        users = bot.get_users_by_name(pol)
        twitter = None
        if users and users[0].followers_count > 50:
            twitter = users[0].screen_name
        print(f"{idx + 1}: {pol} -> {twitter}")
        with db.begin():
            models.create_politic(db, pol, party, twitter)


def create_tweets(db, twitters, bot):
    for idx, twitter in enumerate(twitters):
        tweets = bot.get_tweets_by_user(user=twitter, since=0, until=20)
        print(f"{idx + 1}: {twitter} -> {len(tweets)} tweets")
        for tweet in tweets:
            models.save_tweet(db, tweet)
        db.commit()


def main():
    session = models.init_db("sqlite:///example.db")
    politics = wiki_parser()
    # pprint(politics)
    # print(len(politics))

    bot = Twitter(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_KEY)
    create_politics(session, politics, bot)

    twitters = [username[0] for username in session.query(models.Politic.twitter).all() if username[0]]
    # pprint(twitters)
    # print(len(twitters))
    create_tweets(session, twitters, bot)


if __name__ == "__main__":
    main()
