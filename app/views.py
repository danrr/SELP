from flask import render_template, redirect, flash, g, url_for, request
from app import app, login_manager, db
from app.forms import LoginForm, RegistrationForm, PostForm
from app.models import User, Post
from flask.ext.login import login_user, current_user, logout_user, login_required



@app.before_request
def before_request():
    g.user = current_user


@app.route("/", methods=["GET"])
def home():
    context = {}
    context['title'] = 'Cooking challenge'
    context['posts'] = []
    for post in Post.query.order_by(Post.id.desc()).limit(5):
        context['posts'] += [{
            'id': post.id,
            'title': post.title,
            'content': post.body
        }]

    return render_template('index.html', **context)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated():
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
        flash('Welcome {user}'.format(user=form.username.data))
        return redirect((url_for('home')))
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

    context = {}
    context['title'] = 'Cooking challenge'
    context['rank'] = user.get_rank()
    context['score'] = user.score
    context['posts'] = []
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
        # TODO: deal with date
        post = Post(form.title.data, form.body.data, g.user.id)
        db.session.add(post)
        db.session.commit()
        return redirect((url_for('home')))
    return render_template('new-post.html',
                           title='New post',
                           form=form)


@app.route('/post/<int:id>/', methods=['GET', 'POST'])
def post(id):
    post = Post.query.filter_by(id=id).one()
    author = User.query.filter_by(id=post.user_id).one()
    if request.args.get('edit', '') == 't':
        form = PostForm()

        if form.validate_on_submit():
            post.title = form.title.data
            post.body = form.body.data
            db.session.commit()
            return redirect(url_for('post', id=id))
        
        form.title.data = post.title
        form.body.data = post.body
        return render_template('new-post.html',
                               title='Edit post',
                               form=form)

    if request.args.get('delete', '') == 't':
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('home'))
    can_edit = False
    if g.user is not None and g.user.is_authenticated() and g.user.id == author.id:
        can_edit = True
    return render_template('post.html',
                           title=post.title,
                           content=post.body,
                           author=author.username,
                           can_edit=can_edit,
                           post_id=post.id)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))