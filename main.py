from nlp.scraper import models
from nlp.config import *
from nlp.scraper.twitter import Twitter
from nlp.scraper.parsers import *
from pprint import pprint
from nlp.topicmodeling import nlp_pipeline


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


def create_parties(db, parties):
    for idx, (twitter, party) in enumerate(parties.items()):
        print(f"{idx + 1}: {party[0]} -> {twitter}")
        with db.begin():
            models.create_party(db, party[0], twitter)


def create_tweets(db, twitters, bot, last_n_months=1):
    for idx, twitter in enumerate(twitters):
        tweets = bot.get_tweets_by_user(user=twitter, last_n_months=last_n_months)
        print(f"{idx + 1}: {twitter} -> {len(tweets)} tweets")
        for tweet in tweets:
            models.save_tweet(db, tweet)
        db.commit()


def nlp_pipeline_result():
    session, engine = models.init_db("sqlite:///example.db")
    tweets_df = pd.read_sql_table("tweet", con=engine)
    parsed_tweets = tweets_parser(session, tweets_df)

    return nlp_pipeline(parsed_tweets)


def main():
    session, engine = models.init_db("sqlite:///example.db")
    politics, parties = wiki_parser()
    # pprint(politics)
    # create_politics(session, politics, bot)
    print(f"Number of politics in the Congress: {len(politics)}")  # 350

    # pprint(parties)
    # create_parties(session, PARTIES)
    print(f"Number of political parties: {len(parties)}")  # 24

    bot = Twitter(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_KEY)
    twitters = models.get_politics_twitter_dict(session)
    pprint(twitters)
    print(f"Number of politics with Twitter: {len(twitters)}")  # 292

    # create_tweets(session, twitters, bot)
    tweets_df = pd.read_sql_table("tweet", con=engine)
    print(f"Number of tweets of the politics during the last month: {len(tweets_df.text)}")  # 18206

    parsed_tweets = tweets_parser(session, tweets_df)
    # pprint(parsed_tweets)
    print(f"Number of tweets in Spanish: {len(parsed_tweets)}")
    exit()
    nlp_pipeline(parsed_tweets)


if __name__ == "__main__":
    main()
