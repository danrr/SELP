import os
from werkzeug.utils import secure_filename
from flask import render_template, redirect, flash, g, url_for, request, jsonify
from flask.ext.login import login_user, current_user, logout_user, login_required
from app import app, login_manager, db
from app.forms import LoginForm, RegistrationForm, PostForm, SubmissionForm
from app.models import User, Post, Submission


@app.before_request
def before_request():
    g.user = current_user


@app.route("/", methods=["GET"])
def home():
    context = {
        'title': 'Cooking challenge',
        'posts': []
    }

    for post in Post.query.order_by(Post.id.desc()).limit(5):
        if not post.is_visible():
            continue
        context['posts'] += [{
            'id': post.id,
            'title': post.title,
            'content': post.body
        }]

    return render_template('index.html', **context)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if is_user_logged_in():
        return redirect(url_for('home'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            flash('No such user')
            return redirect((url_for('register')))

        if not user.check_password(form.password.data):
            flash('Password is incorrect')
            return redirect((url_for('login')))

        login_user(user, remember=form.remember_me.data)
        flash('Welcome back, {user}'.format(user=form.username.data))
        return redirect((url_for('home')))
    return render_template('login.html',
                           title='Sign In',
                           form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        old_user = User.query.filter_by(username=form.username.data).first()
        if old_user is not None:
            flash('User {user} already exists'.format(user=form.username.data))
            return redirect((url_for('register')))
        old_user = User.query.filter_by(email=form.email.data).first()
        if old_user is not None:
            flash('{email} already used'.format(email=form.email.data))
            return redirect((url_for('register')))
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Please login to your new account'.format(user=form.username.data))
        return redirect((url_for('login')))
    return render_template('register.html',
                           title='Register',
                           form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/user/<username>/')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first()

    if user is None:
        flash('User {username} not found.'.format(username=username))
        return redirect(url_for('home'))

    context = {
        'title': 'Cooking challenge',
        'rank': user.get_rank(),
        'score': user.score,
        'posts': []
    }
    for post in user.posts:
        context['posts'] += [{
            'id': post.id,
            'title': post.title,
            'content': post.body
        }]

    return render_template('userpage.html', **context)


@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        if form.startnow.data:
            date = None
        else:
            if not form.date.data:
                flash('You must input date if start now checkbox is deselected')
                return redirect(url_for('new_post'))
            date = form.date.data
        post = Post(form.title.data, form.body.data, g.user.id, publish_time=date)
        db.session.add(post)
        db.session.commit()
        return redirect((url_for('home')))
    return render_template('new-post.html',
                           title='New post',
                           form=form)


@app.route('/post/<int:id>/', methods=['GET', 'POST'])
def post(id):
    post = Post.query.filter_by(id=id).first()
    if post is None or not post.is_visible():
        flash('Post not found')
        return redirect(url_for('home'))

    author = User.query.filter_by(id=post.user_id).one()


    if is_current_user(author.id):
        if request.args.get('edit', '') == 't':
            if post.is_archived():
                flash('Archived posts cannot be modified')
                return redirect(url_for('post', id=id))

            form = PostForm()

            if form.validate_on_submit():
                post.title = form.title.data
                post.body = form.body.data
                db.session.commit()
                return redirect(url_for('post', id=id))

            form.title.data = post.title
            form.body.data = post.body
            form.startnow.data = False
            form.date.data = post.publish_time
            return render_template('new-post.html',
                                   title='Edit post',
                                   form=form)

        if request.args.get('delete', '') == 't':
            if post.is_archived():
                flash('Archived posts cannot be deleted')
                return redirect(url_for('post', id=id))
            db.session.delete(post)
            db.session.commit()
            return redirect(url_for('home'))

        if request.args.get('submit', '') == 't':
            flash('Cannot submit entry to own challenge')
            return redirect(url_for('post', id=id))
    else:
        if request.args.get('submit', '') == 't':
            if not is_user_logged_in():
                flash('Please log in to submit')
                return redirect(url_for('login'))
            if Submission.query.filter_by(user_id=g.user.id, post_id=id).all():
                flash("Submission already exists")
                return redirect(url_for('post', id=id))
            if not post.are_submissions_open():
                flash('Submissions are not open for this post')
                return redirect(url_for('post', id=id))

            form = SubmissionForm()
            if form.validate_on_submit():
                path = 'uploads/' + secure_filename(form.image.data.filename)
                form.image.data.save(path)
                text = form.body.data
                submission = Submission(path, text, g.user.id, id)
                db.session.add(submission)
                db.session.commit()
                os.remove(path)
                flash("Submission successful")
                return redirect(url_for('post', id=id))

            return render_template('submit.html',
                                   title='Submit entry',
                                   form=form)

    can_edit = is_current_user(author.id) and not post.is_archived()
    context = {
        'title': post.title,
        'content': post.body,
        'author': author.username,
        'can_edit': can_edit,
        'post_id': post.id,
        'post_closed': post.is_closed(),
        'submissions_open': post.are_submissions_open(),
        'submissions': []
    }

    for submission in Submission.query.filter_by(post_id=post.id).all():
        author = User.query.filter_by(id=submission.user_id).one()
        context['submissions'] += [{
            'url': submission.url,
            'text': submission.text,
            'author': author.username,
            'author_id': author.id,
            'won': submission.won
        }]

    return render_template('post.html',
                           **context
                           )

@app.route('/upvote/', methods=['POST'])
@login_required
def upvote():
    if request.form["type"] == "submission":
        print request.form["author_id"]
        print request.form["post_id"]
        print g.user.id
    return jsonify()


#helpers
def is_user_logged_in():
    return g.user is not None and g.user.is_authenticated()


def is_current_user(user_id):
    return is_user_logged_in() and g.user.id == user_id


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))