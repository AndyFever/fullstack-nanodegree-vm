from models import Base, User, Article, Category, History
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from flask import session as login_session

def is_authenticated():
    """Determines if a user is currently logged into the application"""
    try:
        if login_session['authenicated?']:
            return True
    except KeyError:
        # Key doesn't exist yet
        login_session['authenicated?'] = False
        return False
    else:
        return False


def add_user(username, password):
    """Allows the current user to create an account"""
    # Check the user doesn't exist in the database
    if session.query(User).filter_by(username=username).first():
        return False
    else:
        user = User(username=username)
        user.hash_password(password)
        session.add(user)
        session.commit()
        return True


def add_google_user(username, usr_id, email, picture):
    user = User(username=username, id=usr_id, email=email, picture=picture)
    session.add(user)
    session.commit()
    

def log_user_out():
    """Logs the current user out"""
    login_session['authenicated?'] = False
    login_session['username'] = None
    login_session['gplus_id'] = None
    g.user = None
    flash('User has been successfully logged out')
