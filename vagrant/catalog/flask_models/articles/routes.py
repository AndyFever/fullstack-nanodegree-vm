from flask import Blueprint
from functions.authentication import is_authenticated
from functions.formater import format_text
from flask import session as login_session
from functions.db import *
import bleach
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s:%(levelno)s:%(message)s')

file_handler = logging.FileHandler('article.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


art = Blueprint('article', __name__)


@art.route('/catalog/<int:catalog_id>/items')
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


@art.route('/catalog/<int:catalog_id>/<int:article_id>')
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
        logger.info('Successfully updated history')
    line_text = "\n" + format_text(article.article_text)
    return render_template('article.html',
                           article=article,
                           text=line_text,
                           status=status,)


@art.route('/catalog/<int:article_id>/edit', methods=['GET', 'POST'])
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

            session.add(record)
            session.commit()
            logger.info('Article: {} was successfully editied by {}'.format(title, username))
            flash('Article has been successfully edited')
            return redirect('/', code=302)
    else:
        return redirect('/login')


@art.route('/catalog/add_article', methods=['GET', 'POST'])
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

            new_article = Article(title=title,
                                  article_text=description,
                                  parent_id=category,
                                  owner_id=owner)
            session.add(new_article)
            session.commit()
            logger.info('Article: {} was succesfully created'.format(title))
            flash('New article succesfully created')
            return redirect('/', code=302)
    else:
        return redirect('/login')


@art.route('/catalog/<int:article_id>/delete', methods=['GET', 'POST'])
def delete_article(article_id):
    """
    Allows the user to delete an article
    * The user must be logged in to view this page
    * If not logged in, they should be redirected to the login page
    """
    article = session.query(Article).filter_by(id=article_id).first()
    if is_authenticated():
        if request.method == 'GET':
            print("Article id: {}, User id: {}".format(
                article.owner_id, login_session['user_id']))
            if article.owner_id == str(login_session['user_id']):
                return render_template('delete_article.html')
            else:
                flash('You are not authorised to delete that article.')
                logger.warning('{} tried unsuccessfully to delete article'.format(login_session['user_id']))
                return redirect('/', code=302)
        elif request.method == 'POST':
            # Delete the specified article
            delete_article = session.query(Article).filter_by(
                id=article_id).first()
            session.delete(delete_article)
            session.commit()
            flash('Article has been succsefully deleted')
            logger.info('Article: {} was succesfully deleted'.format(article.title))
            return redirect('/', code=302)
    else:
        return redirect('/login')
