from flask import g


def is_user_logged_in():
    return g.user is not None and g.user.is_authenticated()


def is_current_user(user_id):
    return is_user_logged_in() and g.user.id == user_id
