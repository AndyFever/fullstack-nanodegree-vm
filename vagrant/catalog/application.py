#!/usr/bin/env python2
from models import User, Article, Category, History, Base
from flask import Flask, jsonify, request, render_template, abort, redirect
from flask import g, flash
from flask_httpauth import HTTPBasicAuth
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from flask import session as login_session
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
import random
import string
import bleach
from flaskext.markdown import Markdown
from functions.authentication import is_authenticated, log_user_out
from functions.authentication import add_google_user, add_user
from functions.formater import format_text
from functions.db import *

from flask_models.articles.routes import art
from flask_models.api.routes import api
from flask_models.catalog.routes import catalog
from flask_models.homepage.routes import mod

auth = HTTPBasicAuth()

app = Flask(__name__)
Markdown(app)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = 'Product Catalog'


app.register_blueprint(art)
app.register_blueprint(mod)
app.register_blueprint(catalog)
app.register_blueprint(api, url_prefix='/api')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Allow users to login to the website"""
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    if request.method == "POST":
        username = bleach.clean(request.form['username'])
        password = bleach.clean(request.form['password'])
        if username == "" or password == "":
            # Incorrect details provided
            return render_template('login_with_error.html')
        else:
            # Check the username and password
            if session.query(User).filter_by(username=username).first():
                # User exists, check the password
                user = session.query(User).filter_by(username=username).first()
                result = user.verify_password(password)
                if result:
                    # Set the session variable to a logged in state
                    g.user = user
                    login_session['authenicated?'] = True
                    login_session['username'] = user.username
                    login_session['user_id'] = user.id
                return redirect('/', code=302)
            else:
                # User doesn't exist flash error message
                flash('Unsuccessful login attempt - please try again')
                return redirect('/', code=302)
    elif request.method == 'GET':
        # Display the login page
        return render_template('login.html', STATE=state)


@app.route('/new_user', methods=['GET', 'POST'])
def create_user():
    """Allows the creation of a new user"""
    if request.method == "POST":
        username = bleach.clean(request.form['username'])
        password = bleach.clean(request.form['password'])
        if username != "" and password != "":
            user = session.query(User).filter_by(username=username).first()
            if user is not None:
                # The user exists, abort the action
                flash("User already exists")
                return redirect('/', code=302)
            else:
                add_user(username, password)
                flash('New user created')
            return redirect('/', code=302)
        else:
            # Return error message
            return render_template('new_user_with_error.html')
    elif request.method == 'GET':
        # Display the new user form
        return render_template('new_user.html')


@app.route('/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()

    return redirect('/', code=302)


@auth.verify_password
def verify_password(username_or_token, password):
    #  Try to see if it's a token first
    user_id = User.verify_auth_token(username_or_token)
    if user_id:
        user = session.query(User).filter_by(id=user_id).one()
    else:
        user = session.query(User).filter_by(
            username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    login_session['authenicated?'] = True
    return True


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('User is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['user_id'] = gplus_id
    login_session['authenicated?'] = True

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    print("session: {}".format(login_session['gplus_id']))

    add_google_user(login_session['username'],
                    login_session['user_id'],
                    login_session['email'],
                    login_session['picture'])

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += """ " style = "width: 300px; height: 300px;border-radius: 150px;
                  -webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
              """
    flash("* You're now logged in as %s" % login_session['username'])
    print("done!")
    return output


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    """Logs the current user out of the application"""
    if request.method == 'GET':
        # Display the logout page
        return render_template('logout.html')

    elif request.method == 'POST':
        # Log the current user out
        print('Loging the user out')
        log_user_out()
        status = is_authenticated()
        return redirect('/', code=302)


if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'super_secret_key'
    app.run(host='0.0.0.0', port=5000)
