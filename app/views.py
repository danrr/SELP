from flask import render_template, redirect, flash
from app import app
from app.forms import LoginForm, RegistrationForm


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
    form = LoginForm()
    if form.validate_on_submit():
        flash('Welcome back, {user}'.format(user=form.username.data))
        return redirect('/')
    return render_template('login.html',
                           title='Sign In',
                           form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('Welcome {user}'.format(user=form.username.data))
        return redirect('/')
    return render_template('register.html',
                           title='Register',
                           form=form)