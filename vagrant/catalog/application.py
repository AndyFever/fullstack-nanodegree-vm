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
from flaskext.markdown import Markdown
from behave import given, when, then, step

auth = HTTPBasicAuth()
engine = create_engine('sqlite:///catalog.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)
Markdown(app)

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

    line_text = format_text(article.article_text)
    if status:
        txt = "Hi {}, this article is yours, please feel free to amend it!\n"\
            .format(username)
    else:
        txt = "Please login to edit articles\n"

    text = txt + line_text
    return render_template('article.html',
                           article=article,
                           text=text,
                           status=status,)


@app.route('/catalog/<int:article_id>/edit', methods=['GET', 'POST'])
def edit_article(article_id):
    """
    Allows the user to edit and save an article
    * The user must be logged in to view this page
    * If not logged in, they should be redirected to the login page
    * The user should only be allowed to edit if they are the owner.
        - If unauthorised, they should be redirected to add and article
    """
    if is_authenticated():
        article = session.query(Article).filter_by(id=article_id).first()
        categories = session.query(Category).filter_by(id=article.parent_id)

        if request.method == 'GET':
            # Check the user authored the article

            if article.owner_id == str(login_session['user_id']):
                return render_template('edit_article.html',
                                       categories=categories,
                                       article=article,)
            else:
                flash("""
                      * You are not authorised to edit that article.
                      Please feel free to add a new one instead.
                      """)
                return render_template('add_article.html',
                                       categories=categories)

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
            flash('Article has been successfully edited')
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
            flash('New category created')
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
            owner = login_session['user_id']
            print("Owner: {}".format(owner))

            new_article = Article(title=title,
                                  article_text=description,
                                  parent_id=category,
                                  owner_id=owner)
            session.add(new_article)
            session.commit()
            flash('New article succesfully created')
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
    article = session.query(Article).filter_by(id=article_id).first()
    if is_authenticated():
        if request.method == 'GET':
            print("Article id: {}, User id: {}".format(article.owner_id, login_session['user_id']))
            if article.owner_id == str(login_session['user_id']):
                return render_template('delete_article.html')
            else:
                flash('You are not authorised to delete that article.')
                return redirect('/', code=302)
        elif request.method == 'POST':
            # Delete the specified article
            delete_article = session.query(Article).filter_by(
                id=article_id).first()
            session.delete(delete_article)
            session.commit()
            flash('Article has been succsefully deleted')
            return redirect('/', code=302)
    else:
        return redirect('/login')


@app.route('/catalog.json')
def catalog_json():
    """
    Return all of the catalog and articles in json form
    * The user must be logged in to view this page
    * If not logged in, they should be redirected to the login page
    """
    all_categories = session.query(Category).all()
    all_articles = session.query(Article).all()

    if is_authenticated():
        Categories = {"Category": []}
        for c in all_categories:
            current_category = [c.id, c.category, []]
            for a in all_articles:
                if a.parent_id == c.id:
                    current_article = {"id": a.id,
                                       "parent_id": a.parent_id,
                                       "title": a.title,
                                       "article_text": a.article_text,
                                       "owner": a.owner}
                    current_category[2].append(current_article)
            Categories['Category'].append(current_category)
        return jsonify(Categories)
    else:
        flash('Please login to see the catalog endpoint')
        return redirect('/login', code=302)


@app.route('/categories.json')
def categories_json():
    """
    Returns a json object of the current catalog Categories
    * The user must be logged in to see the catalog
    * If not, they should be directed to the home page
    """
    if is_authenticated():
        catalog = session.query(Category).all()
        return jsonify(Category=[i.serialize for i in catalog])
    else:
        flash('Please login to see the catalog endpoint')
        return redirect('/login', code=302)


@app.route('/category/<int:category_id>/category_articles.json')
def category_articles_json(category_id):
    """
    * User must me logged in.
    * If not, they are returned to the login page
      :param catalog_id: integer related to a specific article
      :return: A list of articles for a category in the JSON format
    """
    if is_authenticated():
        articles = session.query(Article).filter_by(parent_id=category_id)
        return jsonify(Article=[i.serialize for i in articles])
    else:
        flash('Please login to see the articles endpoint')
        return redirect('/login', code=302)


@app.route('/article/<int:article_id>/article.json')
def article_json(article_id):
    """
    * User must me logged in.
    * If not, they are returned to the login page
      :param article_id:
      :return: A single article in the json format
    """
    if is_authenticated():
        article = session.query(Article).filter_by(id=article_id)
        return jsonify(Article=[i.serialize for i in article])
    else:
        flash('Please login to see the article endpoint')
        return redirect('/login', code=302)


@app.route('/users.json')
def users_json():
    """Return all of the users in json form - should be logged in
    * The user must be logged in to view this page
    * If not logged in, they should be redirected to the login page
    """
    if is_authenticated():
        users = session.query(User).all()
        return jsonify(User=[i.serialize for i in users])
    else:
        flash('Please login to see the users endpoint')
        return redirect('/login', code=302)


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
        user = session.query(User).first()
        # The user exists, abort the action
        if username != "" and password != "":
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
    try:
        session.commit()
    except:
        session.rollback()




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

    add_google_user(login_session['username'], login_session['user_id'], login_session['email'], login_session['picture'])

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
    flash('User has been successfully logged out')


def format_text(text):
    """Returns the text in a format ready for markdown"""

    tags = [["<strong>", "**"], ["</strong>", "**"],
            ["<em>", "_"], ["</em>", "_"],
            ["<del>", "~~"], ["</del>", "~~"]]

    formated_text = ""

    # Replace all the formating tags with markdown
    for tag in tags:
        if tag[0] in text:
            text = text.replace(tag[0], tag[1])

    # Replace the styling tag with a new line
    lines = text.split("<br>")

    for line in lines:
        line = line + "\n\n"
        formated_text += line
    return formated_text


if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'super_secret_key'
    app.run(host='0.0.0.0', port=5000)
