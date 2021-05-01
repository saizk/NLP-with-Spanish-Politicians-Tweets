import sqlalchemy as sq
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base
from util import classproperty
from datetime import datetime

Model = declarative_base()
Model.__tablename__ = classproperty(lambda o: o.__name__.lower())


def init_db(db_uri):
    engine = sq.create_engine(db_uri)
    Model.metadata.bind = engine
    session = orm.scoped_session(orm.sessionmaker())(bind=engine)
    return session


def get_or_create_user(db, twitter_user):
    user_hash = hash(twitter_user.id)
    user = db.query(User).filter_by(twitter_id=user_hash).first()
    if user is None:
        user = User(
            user_id=user_hash,
            name=twitter_user.name,
            username=twitter_user.username,
            description=twitter_user.description,
            created_at=datetime.fromtimestamp(float(twitter_user.created_utc))
        )
        db.add(user)
    return user


def save_tweet(db, tweet):
    tweet_hash = hash(tweet.id)
    db_tweet = db.query(Tweet).filter_by(twitter_id=tweet_hash).first()
    if db_tweet is None:
        db_tweet = Tweet(
            tweet_id=tweet_hash,
            author=get_or_create_user(db, tweet.author),
            text=tweet.text,
            retweets=tweet.retweets,
            favs=tweet.favs,
            created_at=datetime.fromtimestamp(float(tweet.created_utc)),
        )
        db.add(db_tweet)


class User(Model):
    id = sq.Column(sq.Integer, primary_key=True)
    user_id = sq.Column(sq.Integer, nullable=False)

    name = sq.Column(sq.String(255), nullable=False)
    username = sq.Column(sq.String(255), nullable=False)
    description = sq.Column(sq.String(512), nullable=False)
    pparty = sq.Column(sq.String(128), nullable=False)  # political party

    tweets = orm.relationship("Tweet",
                              backref="user",
                              cascade="all, delete-orphan")


class Tweet(Model):
    id = sq.Column(sq.Integer, primary_key=True)
    tweet_id = sq.Column(sq.Integer, nullable=False)

    text = sq.Column(sq.String, nullable=False)
    retweets = sq.Column(sq.Integer, nullable=False)  # organic metrics in tweepy object
    favs = sq.Column(sq.Integer, nullable=False)

    created_at = sq.Column(sq.DateTime, nullable=False)
    author_id = sq.Column(sq.Integer, sq.ForeignKey('user.id'), nullable=False)

