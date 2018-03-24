from models import Base, User, Article, Category
from flask import Flask, jsonify, request, render_template, abort, redirect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

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
     status=True,)


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
def catalog_json():
    """Return all of the catalog in json form - should be logged in"""
    # TODO Remove default status of true once login func completed
    categories = session.query(Category).all()
    return jsonify(categories)

@app.route('/new_user')
def create_user():
    """Allows the creation of a new user"""
    if request.method = "POST":
        username = request.form['username']
        password = request.form['password']

        # Check the user doesn't exist in the database
        if session.query(User).filter_by(username=username).first():
            # The user exists, abort the action
            # TODO Add an error page for the problematic user request
            abort(400)
        else:
            hashed_pwd = hash_password(password)
            user = User(username=username, hashed_pwd)
            session.add(user)
            session.commit()
            #  TODO Can we put a flash message here
            return redirect('/', code=302)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
