from app import db
from app.models import User, Post
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
    def test_login_works(self):
        user = User(username='dan', email='dan@X.com', password='12345')
        db.session.add(user)
        response = self.app.post('/login', data={
            'username': 'dan',
            'password': '12345'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assert_contains_string(response.data, 'Welcome back, dan')

    def test_login_fails_with_wrong_pass(self):
        user = User(username='dan', email='dan@X.com', password='12345')
        db.session.add(user)
        response = self.app.post('/login', data={
            'username': 'dan',
            'password': '1245'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assert_contains_string(response.data, 'Password is incorrect')

    def test_login_fails_with_no_user(self):
        response = self.app.post('/login', data={
            'username': 'dan',
            'password': '1234'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assert_contains_string(response.data, 'No such user')
