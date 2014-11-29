from app import db
from app.models import User, Post
from tests.base_test import BaseTest


class TestViews(BaseTest):

    #home
    def test_homepage_displays_with_no_posts(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assert_contains_string(response.data, '<div class="navigation">')
        self.assert_does_not_contain_string(response.data, '<div class="post">')

    def test_homepage_displays_with_posts(self):
        user = User(username='dan', email='dan@X.com', password='12345')
        db.session.add(user)
        post = Post(title='POSTTITLE', body='POSTBODY', user_id=user.id)
        db.session.add(post)
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assert_contains_string(response.data, '<div class="navigation">')
        self.assert_contains_string(response.data, '<div class="post">')
        self.assert_contains_string(response.data, 'POSTBODY')
