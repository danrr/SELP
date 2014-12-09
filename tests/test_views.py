import datetime
from flask import g
from mock import Mock, patch
from app import db
from app.models import User, Post, Submission
from tests.base_test import BaseTest


class TestHomeView(BaseTest):
    def test_homepage_displays_with_no_posts(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assert_contains_string(response.data, '<nav role="navigation"')
        self.assert_does_not_contain_string(response.data, '<div class="post"')

    def test_homepage_displays_with_posts(self):
        user = User(username='dan', email='dan@X.com', password='12345')
        db.session.add(user)
        post = Post(title='POSTTITLE', body='POSTBODY', user_id=user.id, difficulty=2)
        db.session.add(post)
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assert_contains_string(response.data, '<nav role="navigation"')
        self.assert_contains_string(response.data, '<div class="post"')
        self.assert_contains_string(response.data, 'POSTBODY')


class TestLoginView(BaseTest):
    def setUp(self):
        super(TestLoginView, self).setUp()
        self.user = User(username='dan', email='dan@X.com', password='12345')
        db.session.add(self.user)

    def test_login_works(self):
        response = self.app.post('/login', data={
            'username': 'dan',
            'password': '12345'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assert_contains_string(response.data, 'Welcome back, dan')

    def test_login_fails_with_wrong_pass(self):
        response = self.app.post('/login', data={
            'username': 'dan',
            'password': '1245'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assert_contains_string(response.data, 'Password is incorrect')

    def test_login_fails_with_no_user(self):
        response = self.app.post('/login', data={
            'username': 'dana',
            'password': '12345'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assert_contains_string(response.data, 'No such user')


class TestRegisterView(BaseTest):
    def test_register_view_adds_user(self):
        response = self.app.post('/register', data={
            'username': 'dan',
            'password': '12345',
            'confirm': '12345',
            'email': 'a@a.com'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assert_contains_string(response.data, 'Please login to your new account')
        self.assertEqual(User.query.first().username, 'dan')

    def test_register_view_fails_when_username_taken(self):
        user = User(username='dan', email='dan@X.com', password='12345')
        db.session.add(user)
        response = self.app.post('/register', data={
            'username': 'dan',
            'password': '12345',
            'confirm': '12345',
            'email': 'a@a.com'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assert_contains_string(response.data, 'User dan already exists')

    def test_register_view_fails_when_email_taken(self):
        user = User(username='dan', email='dan@X.com', password='12345')
        db.session.add(user)
        response = self.app.post('/register', data={
            'username': 'dana',
            'password': '12345',
            'confirm': '12345',
            'email': 'dan@X.com'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assert_contains_string(response.data, 'dan@X.com already used')


class TestUserView(BaseTest):
    def test_user_view_redirects_when_user_not_found(self):
        response = self.app.get('/user/dan/')
        self.assertEqual(response.status_code, 302)

    @patch('app.models.ImgurClient.upload_from_path', Mock())
    def test_user_view_displays_posts_and_submissions(self):
        user = User(username='dan', email='dan@X.com', password='12345')
        db.session.add(user)
        db.session.commit()
        post = Post(title="POSTTITLE", body="POSTBODY", user_id=user.id, difficulty=1)
        db.session.add(post)
        db.session.commit()
        submission = Submission(path="a/b/c", text="SUBMISSIONTEXT", user_id=user.id, post_id=post.id)
        db.session.add(submission)
        db.session.commit()
        response = self.app.get('/user/{username}/'.format(username=user.username))
        self.assertEqual(response.status_code, 200)
        self.assert_contains_string(response.data, "POSTTITLE")
        self.assert_contains_string(response.data, "SUBMISSIONTEXT")


class TestNewPostView(BaseTest):
    def test_post_view_displays(self):
        response = self.app.get('/post/new')
        self.assertEqual(response.status_code, 200)
        self.assert_contains_string(response.data, "ingredients-0")

    @patch('app.views.current_user', Mock(id=1))
    def test_post_view_creates_new_post(self):
        self.assertEqual(Post.query.count(), 0)
        self.app.post('/post/new', data={
            'title': 'title',
            'body': 'body',
            'start_time': datetime.datetime.now().strftime("%d-%m-%Y %H:%M"),
            'difficulty': 1,
            'ingredients-0': 'ingredients-0'
        })
        self.assertEqual(Post.query.count(), 1)