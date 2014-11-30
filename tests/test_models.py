from app import db
from mock import patch, Mock
from app.models import User, Submission
from tests.base_test import BaseTest


class TestViews(BaseTest):

    #user model
    @patch('app.models.generate_password_hash')
    def test_user_model_can_init(self, patch_hash):
        user = User('Dan', 'aa@aa.com', '12345')
        self.assertEqual(user.username, 'Dan')
        self.assertEqual(user.email, 'aa@aa.com')
        patch_hash.assert_called_with('12345')
        self.assertEqual(user.score, 0)

    def test_user_model_login_methods(self):
        user = User('Dan', 'aa@aa.com', '12345')
        self.assertEqual(user.is_authenticated(), True)
        self.assertEqual(user.is_active(), True)
        self.assertEqual(user.is_anonymous(), False)

    def test_user_model_can_increase_score(self):
        user = User('Dan', 'aa@aa.com', '12345')
        self.assertEqual(user.score, 0)
        user.increase_score(10)
        self.assertEqual(user.score, 10)

    @patch('app.models.generate_password_hash', Mock(return_value='abcdef'))
    @patch('app.models.check_password_hash')
    def test_user_model_can_check_password(self, patch_check_hash):
        user = User('Dan', 'aa@aa.com', '12345')
        user.check_password('1234')
        patch_check_hash.assert_called_with('abcdef', '1234')

    def test_user_model_ranking(self):
        user1 = User('Dan', 'aa@aa.com', '12345')
        user2 = User('Dan1', 'aaa@aa.com', '12345')
        user1.increase_score(10)
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
        self.assertEqual(user1.get_rank(), 1)
        self.assertEqual(user2.get_rank(), 2)

    #submission model
    @patch('app.models.ImgurClient.upload_from_path')
    def test_submission_model_can_init(self, patch_imgur):
        submission = Submission('a/b/c', 'abcdef', 1, 1)
        self.assertEqual(submission.text, 'abcdef')
        # uncomment when imgur upload is enabled
        # patch_imgur.assert_called_with('a/b/c', config=None, anon=True)