from datetime import datetime, timedelta
from app import db
from mock import patch, Mock, call
from app.models import User, Submission, Post
from tests.base_test import BaseTest


class TestUserModel(BaseTest):
    def setUp(self):
        super(TestUserModel, self).setUp()
        self.user = User('Dan', 'aa@aa.com', '12345')

    @patch('app.models.generate_password_hash')
    def test_user_model_can_init(self, patch_hash):
        user1 = User('Dan1', 'aa@aa.com', '12345')
        self.assertEqual(user1.username, 'Dan1')
        self.assertEqual(user1.email, 'aa@aa.com')
        patch_hash.assert_called_with('12345')
        self.assertEqual(user1.score, 0)

    def test_user_model_login_methods(self):
        self.assertEqual(self.user.is_authenticated(), True)
        self.assertEqual(self.user.is_active(), True)
        self.assertEqual(self.user.is_anonymous(), False)

    def test_user_model_can_increase_score(self):
        self.assertEqual(self.user.score, 0)
        self.user.increase_score(10)
        self.assertEqual(self.user.score, 10)

    @patch('app.models.generate_password_hash', Mock(return_value='abcdef'))
    @patch('app.models.check_password_hash')
    def test_user_model_can_check_password(self, patch_check_hash):
        user1 = User('Dan1', 'aa@aa.com', '12345')
        user1.check_password('1234')
        patch_check_hash.assert_called_with('abcdef', '1234')

    def test_user_model_ranking(self):
        user1 = User('Dan1', 'aaa@aa.com', '12345')
        self.user.increase_score(10)
        db.session.add(self.user)
        db.session.add(user1)
        db.session.commit()
        self.assertEqual(self.user.get_rank(), 1)
        self.assertEqual(user1.get_rank(), 2)


class TestPostModel(BaseTest):
    def test_post_model_can_init(self):
        date = datetime.strptime('2014-12-12', '%Y-%m-%d')
        post = Post('Title', 'Body', 1, publish_time=date, difficulty=2)
        self.assertEqual(post.title, 'Title')
        self.assertEqual(post.body, 'Body')
        self.assertEqual(post.user_id, 1)
        self.assertEqual(post.publish_time, date)
        self.assertEqual(post.difficulty, 2)

    def test_post_model_is_visible(self):
        date = datetime.utcnow() - timedelta(1)
        post = Post('Title', 'Body', 1, publish_time=date, difficulty=2)
        self.assertTrue(post.is_visible())
        date = datetime.utcnow() + timedelta(1)
        post = Post('Title', 'Body', 1, publish_time=date, difficulty=2)
        self.assertFalse(post.is_visible())

    @patch('app.models.ImgurClient.upload_from_path', Mock())
    @patch('app.models.Post.is_closed', Mock(return_value=True))
    def test_post_model_is_archived(self):
        user = User('dan', 'dan@aadf.com', '12345')
        db.session.add(user)
        db.session.commit()

        post = Post('Title', 'Body', user.id, difficulty=5)
        db.session.add(post)
        db.session.commit()
        self.assertFalse(post.is_archived())

        submission = Submission('a/b/c', 'abcdef', user_id=user.id, post_id=post.id)
        submission.won = True
        db.session.add(submission)
        db.session.commit()

        self.assertTrue(post.is_archived())

    @patch('app.models.Post.is_visible', Mock(return_value=True))
    def test_post_model_are_submissions_open(self):
        date = datetime.utcnow() + timedelta(1)
        post = Post('Title', 'Body', 1, publish_time=date, difficulty=3)
        self.assertTrue(post.are_submissions_open())

        date = datetime.utcnow() + timedelta(8)
        post = Post('Title', 'Body', 1, publish_time=date, difficulty=3)
        self.assertFalse(post.are_submissions_open())

    def test_post_model_difficulty_string(self):
        post = Post('Title', 'Body', 1, difficulty=1)
        self.assertEqual(post.get_difficulty_string(), "Beginner")
        post.difficulty = 2
        self.assertEqual(post.get_difficulty_string(), "Novice")
        post.difficulty = 3
        self.assertEqual(post.get_difficulty_string(), "Intermediate")
        post.difficulty = 4
        self.assertEqual(post.get_difficulty_string(), "Hard")
        post.difficulty = 5
        self.assertEqual(post.get_difficulty_string(), "Expert")
        post.difficulty = 99
        self.assertEqual(post.get_difficulty_string(), "Intermediate")


class TestSubmissionModel(BaseTest):
    @patch('app.models.ImgurClient.upload_from_path', Mock())
    def setUp(self):
        super(TestSubmissionModel, self).setUp()
        self.user1 = User('Dan', 'aa@aa.com', '12345')
        self.user2 = User('Dan1', 'aaa@aa.com', '12345')
        db.session.add(self.user1)
        db.session.add(self.user2)
        db.session.commit()
        self.post = Post('Title', 'Body', self.user1.id, difficulty=1)
        db.session.add(self.post)
        db.session.commit()
        self.submission = Submission('a/b/c', 'abcdef', user_id=self.user1.id, post_id=self.post.id)
        db.session.add(self.submission)
        db.session.commit()

    @patch('app.models.ImgurClient.upload_from_path')
    def test_submission_model_can_init(self, patch_imgur):
        submission = Submission('a/b/c', 'abcdef', 1, 1)
        self.assertEqual(submission.text, 'abcdef')
        # uncomment when imgur upload is enabled
        # patch_imgur.assert_called_with('a/b/c', config=None, anon=True)

    def test_submission_model_knows_user_upvoted(self):
        self.assertTrue(self.submission.has_user_upvoted(self.user1.id))
        self.assertFalse(self.submission.has_user_upvoted(self.user2.id))

    @patch('app.models.Submission.has_user_upvoted', Mock(return_value=False))
    def test_submission_model_can_toggle_upvotes_to_true(self):
        self.assertEqual(self.submission.votes.all(), [self.user1])
        self.submission.toggle_upvote(self.user2.id)
        db.session.commit()
        self.assertEqual(self.submission.votes.all(), [self.user1, self.user2])

    @patch('app.models.Submission.has_user_upvoted', Mock(return_value=True))
    def test_submission_model_can_toggle_upvotes_to_false(self):
        self.assertEqual(self.submission.votes.all(), [self.user1])
        self.submission.toggle_upvote(self.user1.id)
        db.session.commit()
        self.assertEqual(self.submission.votes.all(), [])

    def test_submission_model_can_count_upvotes(self):
        self.assertEqual(self.submission.count_upvotes(), 1)
        self.submission.votes.append(self.user2)
        self.assertEqual(self.submission.count_upvotes(), 2)

    @patch('app.models.ImgurClient.upload_from_path', Mock())
    @patch('app.models.User.increase_score')
    def test_submission_model_can_make_winner(self, mock_increase_score):
        self.submission.make_winner()
        db.session.commit()
        self.assertTrue(self.submission.won)
        submission1 = Submission('a/b/c', 'abcdef', user_id=self.user2.id, post_id=self.post.id)
        db.session.add(submission1)
        db.session.commit()
        self.assertRaises(Exception, submission1.make_winner)
        mock_increase_score.assert_has_calls([call(100), call(100)])