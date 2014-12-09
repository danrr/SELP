from datetime import datetime, timedelta
import math
from mock import patch, Mock
from imgurpython import ImgurClient
from sqlalchemy import UniqueConstraint, exists, and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
import flask.ext.whooshalchemy as whooshalchemy
from werkzeug.security import check_password_hash, generate_password_hash
from app import db, app
from app.config import imgur_client_id, imgur_client_secret

upvotes = db.Table("upvotes",
                   db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                   db.Column('submission_id', db.Integer, db.ForeignKey('submission.id'))
                   )

tags = db.Table('tags',
                db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
                db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
                )


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(120))
    score = db.Column(db.Integer)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    submissions = db.relationship('Submission', backref='submitter', lazy='dynamic')

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.score = 0

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def increase_score(self, score):
        self.score += score

    def get_rank(self):
        return self.__class__.query.filter(self.__class__.score > self.score).count() + 1

    @classmethod
    def get_olympic_rankings(cls):
        """ Return list of tuples of the form (rank, user) in order score.
        Users with the same score will have the same rank - olympic ranking
        """
        users = cls.query.order_by(cls.score.desc()).all()
        users_list = []
        i = 0
        while i < len(users):

            users_list.append((i + 1, users[i]))
            i += 1
            while i < len(users) and users[i-1].score == users[i].score:
                # place users with the same score on the same rank
                users_list.append((users_list[i-1][0], users[i]))
                i += 1
        return users_list

    def __repr__(self):
        return '<User {username}>'.format(username=self.username)


class Post(db.Model):
    __searchable__ = ['title', 'body']
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.Text)
    difficulty = db.Column(db.Integer)
    publish_time = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    submissions = db.relationship('Submission', backref='post', lazy='dynamic')
    tags = db.relationship('Tag', secondary=tags, backref='posts', lazy='dynamic')
    ingredients = db.relationship('Ingredient', backref='post', lazy='dynamic')

    def __init__(self, title, body, user_id, difficulty, publish_time=None):
        self.title = title
        self.body = body
        self.user_id = user_id
        self.difficulty = difficulty
        if not publish_time:
            publish_time = datetime.now()
        self.publish_time = publish_time

    def get_closing_datetime(self):
        return self.publish_time + timedelta(days=7)

    def is_visible(self):
        return self.publish_time <= datetime.now()

    @classmethod
    def get_visible_posts(cls, start=0, end=5):
        return cls.query.filter(cls.publish_time <= datetime.now()).order_by(Post.id.desc())[start:end]

    def is_archived(self):
        return self.is_closed() and any(submission.won for submission in self.submissions.all())

    @classmethod
    def get_archived_posts(cls, start=0, end=5):
        return cls.query.join(Submission).filter(cls.publish_time <= datetime.now(),
                                                 Submission.won,
                                                 Submission.post_id == cls.id).order_by(Post.id.desc())[start:end]

    def are_submissions_open(self):
        return self.is_visible() and self.get_closing_datetime() > datetime.now()

    @classmethod
    def get_open_posts(cls, start=0, end=5):
        return cls.query.filter(cls.publish_time <= datetime.now(),
                                cls.publish_time > (datetime.now() - timedelta(days=7))
                                ).order_by(Post.id.desc())[start:end]

    def is_closed(self):
        return self.is_visible() and not self.are_submissions_open()

    @classmethod
    def get_closed_posts(cls, start=0, end=5):
        return db.session.query(cls).filter(cls.publish_time <= datetime.now() - timedelta(days=7),
                                            ~exists().where(and_(cls.id == Submission.post_id,
                                                               Submission.won)))[start:end]

    def get_difficulty_string(self):
        return {
            1: "Beginner",
            2: "Novice",
            3: "Intermediate",
            4: "Hard",
            5: "Expert"
        }.get(self.difficulty, "Intermediate")

    def add_tag(self, name):
        try:
            tag = Tag.query.filter(Tag.name == name).one()
        except NoResultFound:
            tag = Tag(name)
            db.session.add(tag)
        if tag not in self.tags:
            self.tags.append(tag)
            return tag
        return

    def remove_tag(self, name):
        tag = Tag.query.filter_by(name=name).first()
        self.tags.remove(tag)
        if not tag.posts:
            db.session.delete(tag)

    def add_ingredients(self, ingredients):
        for text in ingredients:
            ingredient = Ingredient(text, self.id)
            db.session.add(ingredient)
            self.ingredients.append(ingredient)

    def remove_ingredients(self):
        for ingredient in self.ingredients.all():
            self.ingredients.remove(ingredient)

    def get_ingredients(self):
        return [ingredient.text for ingredient in self.ingredients.all()]

    def __repr__(self):
        return '<Post {title}>'.format(title=self.title)

whooshalchemy.whoosh_index(app, Post)


class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    text = db.Column(db.Text)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    def __init__(self, text, post_id):
        self.text = text
        self.post_id = post_id

    def __repr__(self):
        return "<Ingredient {text}>".format(text=self.text)


class Submission(db.Model):
    __table_args__ = (
        UniqueConstraint('user_id', 'post_id', name='user_id_post_id'),
    )
    id = db.Column(db.Integer, primary_key=True, index=True)
    url = db.Column(db.String(100))
    text = db.Column(db.Text)
    won = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    votes = db.relationship('User',
                            secondary=upvotes,
                            backref=db.backref('upvoted', lazy='dynamic'),
                            lazy='dynamic'
                            )

    @patch.object(ImgurClient, 'upload_from_path', Mock(return_value={'link': 'http://i.imgur.com/Sj6yA9J.jpg'}))
    # remove mock when going into "production"
    def __init__(self, path, text, user_id, post_id):
        # client = ImgurClient(imgur_client_id, imgur_client_secret)
        self.url = 'http://i.imgur.com/Sj6yA9J.jpg'  # client.upload_from_path(path, config=None, anon=True)['link']
        self.user_id = user_id
        self.post_id = post_id
        self.text = text
        self.won = False
        self.votes.append(User.query.filter_by(id=self.user_id).first())

    def make_winner(self):
        if not self.__class__.query.filter_by(post_id=self.post_id, won=True).all():
            pool = 200 * self.post.difficulty
            submissions = self.__class__.query.filter_by(post_id=self.post_id).all()
            total_votes = 0
            # half of the score is distributed according to number of upvotes
            for submission in submissions:
                total_votes += submission.count_upvotes()
            for submission in submissions:
                score = pool/2 * submission.count_upvotes()/total_votes
                submission.submitter.increase_score(score)
            # the other half is given to the winner
            self.submitter.increase_score(pool/2)
            # the author of the post gets score proportional to the interest (based on number of submission and upvotes)
            score = int(pool * math.log(len(submissions) + 1, 10) + pool/10 * math.log(total_votes + 1, 10))
            self.post.author.increase_score(score)
            self.won = True
        else:
            raise IntegrityError

    def toggle_upvote(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        if self.has_user_upvoted(user_id):
            self.votes.remove(user)
        else:
            self.votes.append(user)

    def count_upvotes(self):
        return self.votes.count()

    def has_user_upvoted(self, user_id):
        if self.votes.filter_by(id=user_id).first():
            return True
        return False

    def __repr__(self):
        return '<Submission by {user_id} to {post_id}: {url}, {text}>'.format(user_id=self.user_id,
                                                                              post_id=self.post_id,
                                                                              url=self.url,
                                                                              text=self.text)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)

    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return "<Tag {name}>".format(name=self.name)