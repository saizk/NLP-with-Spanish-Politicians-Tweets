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
        users = bot.api.search_users(pol)
        if users:
            twitter = users[0].screen_name
        else:
            twitter = None
        print(f"{idx}:  {pol} -> {twitter}")
        with db.begin():
            models.create_politic(db, pol, party, twitter)


def main():
    session = models.init_db("sqlite:///example.db")
    politics = wiki_parser()
    # pprint(politics)
    # print(len(politics))

    bot = Twitter(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_KEY)
    # create_politics(session, politics, bot)

    twitters = [username[0] for username in session.query(models.Politic.twitter).all() if username[0]]
    # pprint(twitters)
    # print(len(twitters))

    result = bot.get_tweets_by_user(user=twitters[0], since=0, until=10)
    pprint(result)
    print(len(result))
    # print(result.__dir__())


if __name__ == "__main__":
    main()
