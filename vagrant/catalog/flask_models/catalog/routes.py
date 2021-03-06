from flask import Blueprint
from functions.authentication import is_authenticated
from flask import session as login_session
from functions.db import *
import bleach
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s:%(levelno)s:%(message)s')

file_handler = logging.FileHandler('catalog.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

catalog = Blueprint('catalog', __name__)


@catalog.route('/category/add_category', methods=['GET', 'POST'])
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
            logging.info('Category {} was succesfully created'.format(category))
            return redirect('/', code=302)

    else:
        return redirect('/login')
