from models import Base, User, Article, Category
from flask import Flask, jsonify, request, render_template, abort, redirect, g
from flask_httpauth import HTTPBasicAuth
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
auth = HTTPBasicAuth()
engine = create_engine('sqlite:///catalog.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)


@app.route('/')
def show_homepage():
    """Displays all the categories and the first ten articles"""
    categories = session.query(Category).all()
    articles = session.query(Article).limit(10)

    return render_template('homepage.html',
     categories=categories,
     articles=articles,
     status=False,)


@app.route('/catalog/<int:catalog_id>/items')
def show_articles_by_category(catalog_id):
    """Displays all the articles associated with a specific category"""
    # Get the category title and related articles
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(id=catalog_id)
    articles = session.query(Article).filter_by(parent_id=catalog_id)
    # TODO Return all the data - status is set to True until login is done
    return render_template('articles_by_category.html',
     category=category,
     categories=categories,
     articles=articles,
     status=True,)


@app.route('/catalog/<int:catalog_id>/<int:article_id>')
def show_article(catalog_id, article_id):
    """Displays a specific article - if logged in you can edit the article"""
    # Get the details of the article to be displayed
    article = session.query(Article).filter_by(id=article_id)
    # TODO Return status of true until login completed, then remove
    return render_template('article.html',
     article=article,
     status=True,)


@app.route('/catalog.json')
@auth.login_required
def catalog_json():
    """Return all of the catalog in json form - should be logged in"""
    # TODO Remove default status of true once login func completed
    all_categories = session.query(Category).all()
    return jsonify(Category=[i.serialize for i in all_categories])


@app.route('/users.json')
@auth.login_required
def users_json():
    """Return all of the users in json form - should be logged in"""
    # TODO Remove default status of true once login func completed
    users = session.query(User).all()
    return jsonify(User=[i.serialize for i in users])


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Allow users to login to the website"""
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        # Check the username and password
        if session.query(User).filter_by(username=username).first():
            # User exists, check the password
            user = session.query(User).filter_by(username=username).first()
            result = user.verify_password(password)
            if result:
                print('User {} has been succesfully validated - result: {}'.format(user.username, result))
                # Set the session variable to a logged in state
                g.user = user
            return redirect('/', code=302)
        else:
            # User doesn't exist flash error message
            print('User - {}, unsucceful login attempt'.format(user.username))
            return redirect('/', code=302)
    else:
        # Display the login page
        return render_template('login.html')


@app.route('/new_user', methods=['GET', 'POST'])
def create_user():
    """Allows the creation of a new user"""
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        user = session.query(User).first()
        # The user exists, abort the action
        # TODO Add an error page for the problematic user request
        add_user(username, password)
        #  TODO Can we put a flash message here
        return redirect('/', code=302)
    else:
        # Display the new user form
        return render_template('new_user.html')


@app.route('/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return redirect('/', code=302)


@auth.verify_password
def verify_password(username_or_token, password):
    #Try to see if it's a token first
    user_id = User.verify_auth_token(username_or_token)
    if user_id:
        user = session.query(User).filter_by(id = user_id).one()
    else:
        user = session.query(User).filter_by(username = username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


def add_user(username, password):
    # Check the user doesn't exist in the database
    if session.query(User).filter_by(username=username).first():
        return False
    else:
        user = User(username = username)
        user.hash_password(password)
        session.add(user)
        session.commit()


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
