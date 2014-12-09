import re
from flask import g


def is_user_logged_in():
    return g.user is not None and g.user.is_authenticated()


def is_current_user(user_id):
    return is_user_logged_in() and g.user.id == user_id


def parse_search_query(full_query):
    difficulty = re.search("(?<=difficulty:)\s*(beginner|intermediate|novice|hard|expert)", full_query, flags=re.IGNORECASE)
    if difficulty:
        difficulty = difficulty.group(0)
    query = re.sub("difficulty:\s*(beginner|intermediate|novice|hard|expert)", "", full_query, flags=re.IGNORECASE)

    tag = re.search("(?<=tag:)\s*[a-z0-9]+", query, flags=re.IGNORECASE)
    if tag:
        tag = tag.group(0)
    query = re.sub("tag:\s*[a-z0-9]+", "", query, flags=re.IGNORECASE)

    query = re.sub("\s+$", "", query)

    return query, difficulty, tag