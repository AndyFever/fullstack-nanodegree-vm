from flask import Blueprint
from functions.authentication import is_authenticated
from flask import session as login_session
from functions.db import *

mod = Blueprint('home', __name__)

@mod.route('/')
def show_homepage():
    """
    Displays all the categories and the first ten articles
    """
    categories = session.query(Category).all()
    articles = session.query(Article).limit(10)
    # Load  and return the last five records from History (if logged in)
    if is_authenticated():
        history = session.query(History).filter_by(
            viewer=login_session['username']).all()
        history.reverse()  # Get the most recent record first
        return render_template('homepage.html',
                               categories=categories,
                               articles=articles,
                               history=history[:5],
                               status=is_authenticated())
    else:
        return render_template('homepage.html',
                               categories=categories,
                               articles=articles,
                               status=is_authenticated())
