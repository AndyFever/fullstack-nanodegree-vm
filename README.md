# TestingBOK Catalog Application

Welcome to the TestingBOK Catalog application.  This is a project for the Udacity
course on full stack web development.

## Prerequisites

You have cloned this forked repository from the Udacity website and you have
Vagrant and VirtualBox installed.

## Setup Instructions

Navigate to the cloned directory containing this fork of the code.  Then:

1. Run ```vagrant up``` from your terminal window.  

2. Once the base image has been downloaded and installed, enter ```vagrant ssh``` followed by ```cd /vagrant/catalog```.

3. To prepare the database, run the following commands:

```
sudo pip install Flask-Markdown
cd /catalog
python models.py
python load_data.py
python application.py
```

You should now have a working application.

## Useful Features

### Log in

You can log in through a user account (which you will have to create first)
or through using the Google OAuth2 provider.

### API Endpoints

You can get full access to the data in TestingBoK as long as you have an
account and you're logged in. The endpoints are listed below.

#### Categories & Articles

You can see all the categories and articles in the database. To access specify:

**http://localhost:5000/.catalog.json**

#### Categories

You can see a list of all the current categories through the categories endpoint:

**http://localhost:5000/categories.json**

#### Article by Category

A list of articles for a particular category is available. You need to specify the category id.

**http://localhost/category/[category_id]/category_articles.json**

#### Article

A specific article is also available, you just need to specify the article ID

**http://localhost:5000//article/[article_id]/article.json**

#### Users

You can see all the users of the application.

**http://localhost:5000/users.json**

You can also see all the categories and articles in the database though the
[Catalog endpoint](http://localhost:5000/users.json)

### History

Once you have logged in, you can see all the articles you have viewed or edited
recently.
