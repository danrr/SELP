from datetime import datetime, timedelta
from imgurpython import ImgurClient
from app import db
from app.models import User, Post, Submission
from mock import Mock, patch


@patch.object(ImgurClient, 'upload_from_path', Mock(return_value={'link': 'http://i.imgur.com/Sj6yA9J.jpg'}))
def main():
    db.drop_all()
    db.create_all()

    today = datetime.today()

    user1 = User('Erik', 'Erik@ohemgeemail.com', '12345')
    user2 = User('Jane', 'Jane@coldmail.com', 'qwert')
    user3 = User('Mike', 'Mike@oxlarge.com', 'asdfg')
    user4 = User('John', 'John@headtome.com', 'zxcvb')
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.add(user4)
    db.session.commit()

    post1 = Post('Chickpea curry', 'Make chickpea curry', user3.id, publish_time=today - timedelta(11))
    post2 = Post('Black pudding', 'Make carrot cake', user3.id, publish_time=today - timedelta(8))
    post3 = Post('Carrot cake', 'Make carrot cake', user2.id, publish_time=today - timedelta(3))
    post4 = Post('Soup', 'Make soup', user1.id, publish_time=today)
    post5 = Post('Stew', 'Make stew', user1.id, publish_time=today + timedelta(3))
    db.session.add(post1)
    db.session.add(post2)
    db.session.add(post3)
    db.session.add(post4)
    db.session.add(post5)
    db.session.commit()

    submission1 = Submission('a/b/c', 'This is my chickpea curry', post_id=post1.id, user_id=user2.id)
    submission2 = Submission('a/b/c', 'This is my chickpea curry', post_id=post1.id, user_id=user1.id)
    submission3 = Submission('a/b/c', 'This is my black pudding', post_id=post2.id, user_id=user1.id)
    submission4 = Submission('a/b/c', 'This is my black pudding', post_id=post2.id, user_id=user2.id)
    submission5 = Submission('a/b/c', 'This is my carrot cake', post_id=post3.id, user_id=user3.id)
    submission6 = Submission('a/b/c', 'This is my carrot cake', post_id=post3.id, user_id=user4.id)
    submission7 = Submission('a/b/c', 'This is my carrot cake', post_id=post3.id, user_id=user1.id)
    db.session.add(submission1)
    db.session.add(submission2)
    db.session.add(submission3)
    db.session.add(submission4)
    db.session.add(submission5)
    db.session.add(submission6)
    db.session.add(submission7)
    db.session.commit()

    submission1.toggle_upvote(user1.id)
    submission1.toggle_upvote(user3.id)
    submission1.toggle_upvote(user4.id)
    submission2.toggle_upvote(user4.id)
    submission2.toggle_upvote(user3.id)
    submission3.toggle_upvote(user3.id)
    submission4.toggle_upvote(user4.id)
    submission5.toggle_upvote(user1.id)
    submission1.make_winner()
    db.session.commit()

if __name__ == "__main__":
    main()