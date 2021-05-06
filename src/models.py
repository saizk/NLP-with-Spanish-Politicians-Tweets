import sqlalchemy as sq
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base
from util import classproperty
from datetime import datetime
from parsers import parse_tweet_text


Model = declarative_base()
Model.__tablename__ = classproperty(lambda o: o.__name__.lower())


def init_db(db_uri):
    engine = sq.create_engine(db_uri)
    Model.metadata.bind = engine
    session = orm.scoped_session(orm.sessionmaker(bind=engine))
    Tweet.__table__.create(bind=engine, checkfirst=True)
    Politic.__table__.create(bind=engine, checkfirst=True)
    return session


def save_tweet(db, tweet):
    tweet_hash = hash(tweet.id)
    db_tweet = db.query(Tweet).filter_by(tweet_id=tweet_hash).first()
    if db_tweet is None:
        db_tweet = Tweet(
            tweet_id=tweet_hash,
            author_id=get_politic(db, tweet.user.screen_name).id,
            text=parse_tweet_text(tweet.full_text),
            retweets=tweet.retweet_count,
            favs=tweet.favorite_count,
            created_at=tweet.created_at,
        )
        db.add(db_tweet)


def create_politic(db, name, party, twitter):
    pol = db.query(Politic).filter_by(politic_id=hash(name)).first()
    if pol is None:
        pol = Politic(politic_id=hash(name), name=name, party=party, twitter=twitter)
        db.add(pol)


def get_politic(db, twitter):
    politic = db.query(Politic).filter_by(twitter=twitter).first()
    return politic


def get_party(db, twitter):
    politic = get_politic(db, twitter)
    return politic.party


class Tweet(Model):
    id = sq.Column(sq.Integer, primary_key=True)
    tweet_id = sq.Column(sq.Integer, nullable=False)

    text = sq.Column(sq.String, nullable=False)
    retweets = sq.Column(sq.Integer, nullable=False)
    favs = sq.Column(sq.Integer, nullable=False)

    created_at = sq.Column(sq.DateTime, nullable=False)
    author_id = sq.Column(sq.Integer, sq.ForeignKey('politic.id'), nullable=False)


class Politic(Model):
    id = sq.Column(sq.Integer, primary_key=True)
    politic_id = sq.Column(sq.Integer, nullable=False)
    name = sq.Column(sq.String, nullable=False)
    party = sq.Column(sq.String(128), nullable=False)
    twitter = sq.Column(sq.String(128))
    tweets = orm.relationship("Tweet",
                              backref="politic",
                              cascade="all, delete-orphan")
