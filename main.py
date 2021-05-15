from nlp.config import *
from nlp.scraper import models
from nlp.scraper.twitter import Twitter
from nlp.scraper.parties import PARTIES_TWITTERS
from nlp.scraper.parsers import *
from pprint import pprint
from nlp.topicmodeling import NLPPipeline


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


def get_raw_tweets_df(engine):
    politics, _ = wiki_parser()
    tweets_df = pd.read_sql_table("tweet", con=engine)
    tweets_df["author"] = [politics[i-1][0] for i in tweets_df["author_id"]]
    return tweets_df


def nlp_pipeline_result(disable_parser: bool = True, disable_ner: bool = True, parameters: dict = None):
    session, engine = models.init_db("sqlite:///example.db")
    tweets_df = get_raw_tweets_df(engine)
    parsed_tweets_df = tweets_parser(
        tweets_df,
        parameters=parameters,
        session=session,
    )

    nlp_tok = NLPPipeline(
        tweets=parsed_tweets_df["Parsed Tweets"],
        disable_parser=disable_parser,
        disable_ner=disable_ner,
        gpu=False
    )
    parsed_tweets_df["Lemmas"] = nlp_tok.get_lemmas()
    return parsed_tweets_df


def main():
    session, engine = models.init_db("sqlite:///example.db")
    politics, parties = wiki_parser()
    # pprint(politics)
    # create_politics(session, politics, bot)
    print(f"Number of politics in the Congress: {len(politics)}")  # 350

    # pprint(parties)
    # create_PARTIES_TWITTERS(session, PARTIES_TWITTERS)
    print(f"Number of political parties: {len(parties)}")  # 24

    bot = Twitter(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_KEY)
    twitters = models.get_politics_twitter_dict(session)
    print(f"Number of politics with Twitter: {len(twitters)}")  # 292

    # create_tweets(session, twitters, bot)
    raw_tweets_df = get_raw_tweets_df(engine)
    # print(raw_tweets_df)
    print(f"Number of tweets of the politics during the last month: {len(raw_tweets_df.text)}")  # 18206

    print("Parsing incorrect and non-Spanish tweets ...")
    parsed_tweets_df = tweets_parser(
        raw_tweets_df,
        parameters={
            "remove_hashtag_word": True,
            "replace_politics": True,
            "replace_parties": True,
        },
        session=session,
    )
    print(f'Number of tweets in Spanish: {len(parsed_tweets_df["Parsed Tweets"])}')

    print("Pre-processing text with SpaCy ...")
    nlp_tok = NLPPipeline(raw_tweets_df["Parsed Tweets"])
    parsed_tweets_df["Lemmas"] = nlp_tok.get_lemmas()
    print(parsed_tweets_df)


if __name__ == "__main__":
    main()
