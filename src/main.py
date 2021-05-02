import os
import models
from pprint import pprint
from config import *
from twitter import Twitter
from parsers import wiki_parser, search_twitter


# API_KEY = os.environ.get("API_KEY")
# API_SECRET_KEY = os.environ.get("API_SECRET_KEY")
# BEARER_TOKEN = os.environ.get("BEARER_TOKEN")
# ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
# ACCESS_TOKEN_KEY = os.environ.get("ACCESS_TOKEN_KEY")


def create_politics(db, politics):
    with db.begin():
        for idx, (pol, party) in enumerate(politics):
            models.create_politic(db, pol, party, search_twitter(pol))


def main():
    session = models.init_db("sqlite:///example.db")
    politics = wiki_parser()
    pprint(politics)
    print(len(politics))
    create_politics(session, politics)

    # bot = Twitter(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_KEY)


if __name__ == "__main__":
    main()
