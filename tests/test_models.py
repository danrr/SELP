from mock import patch, Mock
from app.models import User
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