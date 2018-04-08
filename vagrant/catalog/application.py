from models import Base, User, Article, Category, History
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

auth = HTTPBasicAuth()
engine = create_engine('sqlite:///catalog.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = 'Product Catalog'


@app.route('/')
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
                               status=is_authenticated(),)
    else:
        return render_template('homepage.html',
                               categories=categories,
                               articles=articles,
                               status=is_authenticated(),)


@app.route('/catalog/<int:catalog_id>/items')
def show_articles_by_category(catalog_id):
    """
    Displays all the articles associated with a specific category
    """
    # Get the category title and related articles
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(id=catalog_id)
    articles = session.query(Article).filter_by(parent_id=catalog_id)
    status = is_authenticated()
    return render_template('articles_by_category.html',
                           category=category,
                           categories=categories,
                           articles=articles,
                           status=status,)


@app.route('/catalog/<int:catalog_id>/<int:article_id>')
def show_article(catalog_id, article_id):
    """Displays a specific article - if logged in you can edit the article"""
    # Get the details of the article to be displayed
    article = session.query(Article).filter_by(id=article_id).first()
    status = is_authenticated()
    # Add the viewing history to the database if the user is logged in
    if status:
        username = login_session['username']
        record = History(viewer=username,
                         action='viewed',
                         viewed_article=article_id)
        session.add(record)
        session.commit()

    return render_template('article.html',
                           article=article,
                           status=status,)


@app.route('/catalog/<int:article_id>/edit', methods=['GET', 'POST'])
def edit_article(article_id):
    """
    Allows the user to edit and save an article
    * The user must be logged in to view this page
    * If not logged in, they should be redirected to the login page
    """
    if is_authenticated():
        article = session.query(Article).filter_by(id=article_id).first()
        # Below may be wrong and why only one cat is brought back
        categories = session.query(Category).filter_by(id=article.parent_id)

        if request.method == 'GET':
            return render_template('edit_article.html',
                                   categories=categories,
                                   article=article,)
        elif request.method == 'POST':
            title = bleach.clean(request.form['title'])
            description = bleach.clean(request.form['my_article'])
            category = bleach.clean(request.form['category'])

            # Update any records that have been returned
            if title:
                article.title = title
            if description:
                article.article_text = description
            if category:
                article.parent_id = category
            # Add and commit the record
            session.add(article)
            session.commit()

            # Update the history for the article
            username = login_session['username']
            record = History(viewer=username,
                             action='edited',
                             viewed_article=article_id)
            print('Adding record')
            session.add(record)
            session.commit()
            flash('Article has been amended')
            return redirect('/', code=302)
    else:
        return redirect('/login')


@app.route('/catalog/add_category', methods=['GET', 'POST'])
def add_category():
    """
    Allows the user to create a new category
    * The user must be logged in to view this page
    * If not logged in, they should be redirected to the login page
    """
    if is_authenticated():
        if request.method == 'GET':
            return render_template('add_category.html')
        if request.method == 'POST':
            # Get the request info and add the new request to the database
            category = bleach.clean(request.form['category'])

            # Create the new record and add to the database
            new_category = Category(category=category)
            session.add(new_category)
            session.commit()
            return redirect('/', code=302)

    else:
        return redirect('/login')

@app.route('/catalog/add_article', methods=['GET', 'POST'])
def add_article():
    """
    Allows the user to create and save an article
    * The user must be logged in to view this page
    * If not logged in, they should be redirected to the login page
    """
    if is_authenticated():
        if request.method == 'GET':
            #  Get the list of categories so the user can select
            categories = session.query(Category).all()
            # Display the add_article page
            return render_template('add_article.html', categories=categories)
        elif request.method == 'POST':
            # Get the request info and add the new request to the database
            title = bleach.clean(request.form['title'])
            description = bleach.clean(request.form['description'])
            category = bleach.clean(request.form['category'])

            # TODO Update the owner once login functionality is complete
            new_article = Article(title=title,
                                  article_text=description,
                                  parent_id=category,
                                  owner='admin')
            session.add(new_article)
            session.commit()
            flash('Record created')
            return redirect('/', code=302)
    else:
        return redirect('/login')


@app.route('/catalog/<int:article_id>/delete', methods=['GET', 'POST'])
def delete_article(article_id):
    """
    Allows the user to delete an article
    * The user must be logged in to view this page
    * If not logged in, they should be redirected to the login page
    """
    if is_authenticated():
        if request.method == 'GET':
            # Display the delete article page
            return render_template('delete_article.html')
        elif request.method == 'POST':
            # Delete the specified article
            delete_article = session.query(Article).filter_by(
                id=article_id).first()
            session.delete(delete_article)
            session.commit()
            flash('Article deleted')
            return redirect('/', code=302)
    else:
        return redirect('/login')


@app.route('/catalog.json')
@auth.login_required
def catalog_json():
    """
    Return all of the catalog and articles in json form
    * The user must be logged in to view this page
    * If not logged in, they should be redirected to the login page
    """
    all_categories = session.query(Category).all()
    all_articles = session.query(Article).all()
    data = []
    for cat in all_categories:

        articles = []
        for art in all_articles:
            if cat.id == art.parent_id:
                new_article = ["article_id", art.id,
                               "title", art.title,
                               "text", art.article_text,
                               "owner", art.owner]
                new_article = new_article
                articles.append(new_article)
        data.append([cat.category, articles])
    return jsonify(dict(data))


@app.route('/users.json')
@auth.login_required
def users_json():
    """Return all of the users in json form - should be logged in
    * The user must be logged in to view this page
    * If not logged in, they should be redirected to the login page
    """
    users = session.query(User).all()
    return jsonify(User=[i.serialize for i in users])


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
                return redirect('/', code=302)
            else:
                # User doesn't exist flash error message
                print('User - {}, unsucceful login attempt'.format(
                    user.username))
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
        user = session.query(User).first()
        # The user exists, abort the action
        # TODO Add an error page for the problematic user request
        if username != "" and password != "":
            add_user(username, password)
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
        print "Token's client ID does not match app's."
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
    login_session['gplus_id'] = gplus_id
    login_session['authenicated?'] = True

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
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


def log_user_out():
    """Logs the current user out"""
    login_session['authenicated?'] = False
    login_session['username'] = None
    login_session['gplus_id'] = None
    g.user = None

if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'super_secret_key'
    app.run(host='0.0.0.0', port=5000)
