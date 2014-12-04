from datetime import datetime, timedelta
from mock import patch, Mock
from imgurpython import ImgurClient
from werkzeug.security import check_password_hash, generate_password_hash
from app import db
from app.config import imgur_client_id, imgur_client_secret


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

    def __repr__(self):
        return '<User {username}>'.format(username=self.username)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.Text)
    publish_time = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    submissions = db.relationship('Submission', backref='post', lazy='dynamic')

    def __init__(self, title, body, user_id, publish_time=None):
        self.title = title
        self.body = body
        self.user_id = user_id
        if not publish_time:
            publish_time = datetime.utcnow()
        self.publish_time = publish_time

    def is_visible(self):
        return self.publish_time <= datetime.utcnow()

    def is_archived(self):
        return self.is_closed() and any(submission.won for submission in self.submissions.all())

    def are_submissions_open(self):
        return self.is_visible() and self.publish_time < datetime.utcnow() + timedelta(days=7)

    def is_closed(self):
        return self.is_visible() and not self.are_submissions_open()

    def __repr__(self):
        return '<Post {title}>'.format(title=self.title)


class Submission(db.Model):
    id = db.Column(db.Integer)
    url = db.Column(db.String(100))
    text = db.Column(db.Text)
    won = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), primary_key=True)

    @patch.object(ImgurClient, 'upload_from_path', Mock(return_value={'link': 'http://i.imgur.com/Sj6yA9J.jpg'}))
    # remove mock when going into "production"
    def __init__(self, path, text, user_id, post_id):
        # client = ImgurClient(imgur_client_id, imgur_client_secret)
        self.url = 'http://i.imgur.com/Sj6yA9J.jpg' # client.upload_from_path(path, config=None, anon=True)['link']
        self.user_id = user_id
        self.post_id = post_id
        self.text = text
        self.won = False

    def make_winner(self):
        if not self.__class__.query.filter_by(post_id=self.post_id).all():
            # TODO: increase scores for author of the post, and submitters
            self.won = True
        else:
            raise Exception('There is a winner already')

    def __repr__(self):
        return '<Submission by {user_id} to {post_id}: {url}, {text}>'.format(user_id=self.user_id,
                                                                              post_id=self.post_id,
                                                                              url=self.url,
                                                                              text=self.text)