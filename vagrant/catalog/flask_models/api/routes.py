from flask import Blueprint
from functions.authentication import is_authenticated
from flask import session as login_session
from functions.db import *

api = Blueprint('api', __name__)


@api.route('/catalog.json')
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
                                       "owner": a.owner_id}
                    current_category[2].append(current_article)
            Categories['Category'].append(current_category)
        return jsonify(Categories)
    else:
        flash('Please login to see the catalog endpoint')
        return redirect('/login', code=302)


@api.route('/categories.json')
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


@api.route('/category/<int:category_id>/category_articles.json')
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


@api.route('/article/<int:article_id>/article.json')
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


@api.route('/users.json')
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
