from flask import render_template, redirect, flash, g, url_for
from app import app, login_manager, db
from app.forms import LoginForm, RegistrationForm
from app.models import User
from flask.ext.login import login_user, current_user, logout_user, login_required



@app.before_request
def before_request():
    g.user = current_user


@app.route("/", methods=["GET"])
def home():
    context = {}
    context['title'] = 'Cooking challenge'
    context['posts'] = [
        {
            'title': "lorem ipsum",
            'content': """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce eu porttitor sem, vitae porta
                     ante. Duis accumsan nulla ut tristique accumsan. Sed a nunc ut augue tristique gravida nec ut urna.
                     Integer lacinia tristique nisl, et tempus est vulputate sit amet. Suspendisse orci urna, pulvinar
                     id lorem facilisis, ultricies egestas nunc. Etiam quis odio rhoncus, feugiat lectus a, euismod dui.
                     Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae;
                     Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas.
                     Vivamus convallis at nisi ut commodo. Donec sit amet libero gravida, vestibulum nibh sollicitudin,
                     fermentum nibh. Morbi ut enim quis nisl sodales iaculis vel nec augue. Proin quis ipsum lorem.
                     Vestibulum eu justo nulla. Nulla sit amet tempor nisi """
        },
        {
            'title': "lorem ipsum",
            'content': """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce eu porttitor sem, vitae porta
                     ante. Duis accumsan nulla ut tristique accumsan. Sed a nunc ut augue tristique gravida nec ut urna.
                     Integer lacinia tristique nisl, et tempus est vulputate sit amet. Suspendisse orci urna, pulvinar
                     id lorem facilisis, ultricies egestas nunc. Etiam quis odio rhoncus, feugiat lectus a, euismod dui.
                     Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae;
                     Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas.
                     Vivamus convallis at nisi ut commodo. Donec sit amet libero gravida, vestibulum nibh sollicitudin,
                     fermentum nibh. Morbi ut enim quis nisl sodales iaculis vel nec augue. Proin quis ipsum lorem.
                     Vestibulum eu justo nulla. Nulla sit amet tempor nisi """
        }
    ]

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


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))