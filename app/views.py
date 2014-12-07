import os
from sqlalchemy.exc import IntegrityError
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
        'annotated_posts': [('Open posts', Post.get_open_posts()),
                            ('Closed posts', Post.get_closed_posts()),
                            ('Archived posts', Post.get_archived_posts())]
    }

    return render_template('index.html', **context)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if is_user_logged_in():
        return redirect(url_for('home'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            flash('No such user', 'error')
            return redirect((url_for('register')))

        if not user.check_password(form.password.data):
            flash('Password is incorrect', 'error')
            return redirect((url_for('login')))

        login_user(user, remember=form.remember_me.data)
        flash('Welcome back, {user}'.format(user=form.username.data), 'info')
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
            flash('User {user} already exists'.format(user=form.username.data), 'error')
            return redirect((url_for('register')))
        old_user = User.query.filter_by(email=form.email.data).first()
        if old_user is not None:
            flash('{email} already used'.format(email=form.email.data), 'error')
            return redirect((url_for('register')))
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Please login to your new account'.format(user=form.username.data), 'info')
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
        'user': user,
    }

    return render_template('userpage.html', **context)


@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    body=form.body.data,
                    user_id=g.user.id,
                    publish_time=form.start_time.data,
                    difficulty=form.difficulty.data)
        db.session.add(post)
        db.session.commit()
        return redirect((url_for('home')))
    return render_template('new-post.html',
                           title='New post',
                           form=form)


@app.route('/post/<int:id>/', methods=['GET', 'POST'])
def post(id):
    def reload_page():
        return redirect(url_for('post', id=id))

    post = Post.query.filter_by(id=id).first()
    if post is None or \
            (not post.is_visible() and not is_current_user(post.author.id)):
        flash('Post not found', 'error')
        return redirect(url_for('home'))

    if is_current_user(post.author.id):
        if request.args.get('edit', '') == "1":
            if post.is_archived():
                flash('Archived posts cannot be modified')
                return reload_page()

            form = PostForm()

            if form.validate_on_submit():
                post.title = form.title.data
                post.body = form.body.data
                post.difficulty = form.difficulty.data
                post.publish_time = form.start_time.data
                db.session.commit()
                return reload_page()

            form.title.data = post.title
            form.body.data = post.body
            form.start_time.data = post.publish_time
            form.difficulty.data = post.difficulty
            return render_template('new-post.html',
                                   title='Edit post',
                                   form=form)

        if request.args.get('delete', '') == "1":
            if post.is_archived():
                flash('Archived posts cannot be deleted', 'error')
                return reload_page()
            db.session.delete(post)
            db.session.commit()
            return redirect(url_for('home'))

        if request.args.get('submit', '') == "1":
            flash('Cannot submit entry to own challenge', 'error')
            return reload_page()

        winner = request.args.get('winner', '')
        if winner:
            submission = Submission.query.filter_by(id=winner).first()
            try:
                submission.make_winner()
                db.session.commit()
            except IntegrityError:
                flash("There is a winner already" 'error')
            return reload_page()
    else:
        if request.args.get('submit', '') == "1":
            if not is_user_logged_in():
                flash('Please log in to submit', 'error')
                return redirect(url_for('login'))
            if Submission.query.filter_by(user_id=g.user.id, post_id=id).all():
                flash('Submission already exists', 'error')
                return reload_page()
            if not post.are_submissions_open():
                flash('Submissions are not open for this post', 'error')
                return reload_page()

            form = SubmissionForm()
            if form.validate_on_submit():
                path = 'uploads/' + secure_filename(form.image.data.filename)
                form.image.data.save(path)
                text = form.body.data
                submission = Submission(path, text, g.user.id, id)
                db.session.add(submission)
                db.session.commit()
                os.remove(path)
                flash('Submission successful', 'info')
                return reload_page()

            return render_template('submit.html',
                                   title='Submit entry',
                                   form=form)

    context = {
        'post': post,
        'title': post.title,
        'is_author': is_current_user(post.author.id),
        'can_edit': is_current_user(post.author.id) and not post.is_archived(),
        'submissions': []
    }

    for submission in Submission.query.filter_by(post_id=post.id).all():
        context['submissions'] += [{
            'id': submission.id,
            'url': submission.url,
            'text': submission.text,
            'author': submission.submitter.username,
            'author_id': submission.submitter.id,
            'won': submission.won,
            'score': submission.count_upvotes(),
            'user_upvoted': is_user_logged_in() and submission.has_user_upvoted(g.user.id)
        }]

    return render_template('post.html',
                           **context
                           )


@app.route('/upvote/', methods=['POST'])
def upvote():
    if request.form["type"] == "submission":  # type can be used for upvoting other things, not just submissions
        if is_user_logged_in():
            post = Post.query.filter_by(id=request.form["post_id"]).first()
            if post.is_visible() and not post.is_archived():
                submission = Submission.query.filter_by(user_id=request.form["author_id"],
                                                        post_id=request.form["post_id"]).first()
                submission.toggle_upvote(g.user.id)
                db.session.commit()
                return jsonify({
                    "success": True,
                    "reason": None
                })
            else:
                return jsonify({
                    "success": False,
                    "reason": "Can't vote on this post as it has been archived"  # also returned to request for post
                                                                                 # that aren't visible but as it's not a
                                                                                 # valid use case there's no need for
                                                                                 # good user feedback
                })
    return jsonify({
        "success": False,
        "reason": "Please log in to vote"
    })


@app.route('/rankings/')
def rankings():
    users = User.query.order_by(User.score.desc()).all()
    users_context = []
    i = 0
    while i < len(users):
        #olympic rankings
        users_context.append({
            "username": users[i].username,
            "score": users[i].score,
            "rank": i + 1
        })
        i += 1
        while i < len(users) and users[i-1].score == users[i].score:
            users_context.append({
                "username": users[i].username,
                "score": users[i].score,
                "rank": users_context[i - 1]["rank"]
            })
            i += 1

    return render_template('rankings.html',
                           title="rankings",
                           users=users_context)


@app.route('/removetag/', methods=["POST"])
def remove_tag():
    post = Post.query.filter_by(id=request.form["post_id"]).first()
    if post is not None and is_current_user(post.author.id):
        post.remove_tag(request.form["tag"])
        db.session.commit()
        return jsonify()
    else:
        return jsonify(), 403


@app.route('/addtag/', methods=["POST"])
def add_tag():
    post = Post.query.filter_by(id=request.form["post_id"]).first()
    if post is not None:
        tag = post.add_tag(request.form["tag"])
        db.session.commit()
        if tag:
            return jsonify({
                "success": True,
                "html": render_template("partials/_tag.html",
                                        tag=tag,
                                        is_author=is_current_user(post.author.id),)
            })
        else:
            return jsonify({
                "success": False
            })
    else:
        return jsonify(), 403


#helpers
def is_user_logged_in():
    return g.user is not None and g.user.is_authenticated()


def is_current_user(user_id):
    return is_user_logged_in() and g.user.id == user_id


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))