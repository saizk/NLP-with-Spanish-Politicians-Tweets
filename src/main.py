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
        twitter = bot.get_twitter_by_name(pol)
        print(f"{idx + 1}: {pol} -> {twitter}")
        with db.begin():
            models.create_politic(db, pol, party, twitter)


def create_parties(db, parties, bot):
    for idx, party in enumerate(parties):
        twitter = bot.get_twitter_by_name(party, min_followers=20)
        print(f"{idx + 1}: {party} -> {twitter}")
        with db.begin():
            models.create_party(db, party, twitter)


def create_tweets(db, twitters, bot):
    for idx, twitter in enumerate(twitters):
        tweets = bot.get_tweets_by_user(user=twitter, since=0, until=30)
        print(f"{idx + 1}: {twitter} -> {len(tweets)} tweets")
        for tweet in tweets:
            models.save_tweet(db, tweet)
        db.commit()


def main():
    session = models.init_db("sqlite:///example.db")
    politics, parties = wiki_parser()
    # pprint(politics)
    # print(len(politics))  # 350
    # pprint(parties)
    # print(len(parties))  # 24

    bot = Twitter(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_KEY)
    create_politics(session, politics, bot)
    create_parties(session, parties, bot)

    twitters = [username[0] for username in session.query(models.Politic.twitter).all() if username[0]]
    # pprint(twitters)
    # print(len(twitters))  # 291
    create_tweets(session, twitters, bot)


if __name__ == "__main__":
    main()
