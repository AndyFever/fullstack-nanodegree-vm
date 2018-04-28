from models import Base, User, Article, Category, History
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from flask import session as login_session
from functions.db import *
import logging
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s:%(levelno)s:%(message)s')

file_handler = logging.FileHandler('user.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

logging.basicConfig(filename='log_info.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')


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
        logger.warning('User: {} already exists'.format(username))
    else:
        user = User(username=username)
        user.hash_password(password)
        session.add(user)
        session.commit()
        logger.info('User: {} was succesfully created'.format(username))
        return True


def add_google_user(username, usr_id, email, picture):
    user = User(username=username, id=usr_id, email=email, picture=picture)
    session.add(user)
    session.commit()
    logger.info('User: {} was successfully created'.format(username))


def log_user_out():
    """Logs the current user out"""
    user = login_session['username']
    login_session['authenicated?'] = False
    login_session['username'] = None
    login_session['gplus_id'] = None
    g.user = None
    flash('User has been successfully logged out')
    logger.info('User {} was succesfully logged out'.format(user))
