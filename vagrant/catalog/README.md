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
pip install Flask-Markdown
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

You can see all the users of the application by going to the following the
[Users endpoint](http://localhost:5000/users.json)

You can also see all the categories and articles in the database though the
[Catalog endpoint](http://localhost:5000/users.json)

### History

Once you have logged in, you can see all the articles you have viewed or edited
recently.
