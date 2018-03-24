from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Category, Article, User

engine = create_engine('sqlite:///catalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

category_one = Category(category="Tools")
session.add(category_one)
session.commit()

category_two = Category(category="Process")
session.add(category_two)
session.commit()

category_three = Category(category="Techniques")
session.add(category_three)
session.commit()

category_four = Category(category="Resources")
session.add(category_four)
session.commit()

category_five = Category(category="Technologies")
session.add(category_five)
session.commit()

category_six = Category(category="Stories")
session.add(category_six)
session.commit()

article_one = Article(parent_id=1, title="Cucumber Automation", article_text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer ullamcorper, ex a mattis maximus, acu nibh bibendum ante, tincidunt varius justo velit ut risus.", owner='admin')
session.add(article_one)
session.commit()

article_two = Article(parent_id=2, title="Behavioral Driven Development", article_text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer ullamcorper, ex a mattis maximus, acu nibh bibendum ante, tincidunt varius justo velit ut risus.", owner='admin')
session.add(article_two)
session.commit()

article_three = Article(parent_id=3, title="Equivalence Partitioning", article_text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer ullamcorper, ex a mattis maximus, acu nibh bibendum ante, tincidunt varius justo velit ut risus.", owner='admin')
session.add(article_three)
session.commit()

article_four = Article(parent_id=4, title="Project Management BOK", article_text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer ullamcorper, ex a mattis maximus, acu nibh bibendum ante, tincidunt varius justo velit ut risus.", owner='admin')
session.add(article_four)
session.commit()

article_five = Article(parent_id=5, title="Restfull APIs", article_text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer ullamcorper, ex a mattis maximus, acu nibh bibendum ante, tincidunt varius justo velit ut risus.", owner='admin')
session.add(article_five)
session.commit()

article_six = Article(parent_id=6, title="Agile Testing in Action", article_text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer ullamcorper, ex a mattis maximus, acu nibh bibendum ante, tincidunt varius justo velit ut risus.", owner='admin')
session.add(article_six)
session.commit()

article_seven = Article(parent_id=1, title="Keyword Driven Testing", article_text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer ullamcorper, ex a mattis maximus, acu nibh bibendum ante, tincidunt varius justo velit ut risus.", owner='admin')
session.add(article_seven)
session.commit()

article_eight = Article(parent_id=2, title="Pair Development", article_text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer ullamcorper, ex a mattis maximus, acu nibh bibendum ante, tincidunt varius justo velit ut risus.", owner='admin')
session.add(article_eight)
session.commit()

article_nine = Article(parent_id=3, title="Boundary Analysis", article_text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer ullamcorper, ex a mattis maximus, acu nibh bibendum ante, tincidunt varius justo velit ut risus.", owner='admin')
session.add(article_nine)
session.commit()

article_ten = Article(parent_id=4, title="ISTQB Guide", article_text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer ullamcorper, ex a mattis maximus, acu nibh bibendum ante, tincidunt varius justo velit ut risus.", owner='admin')
session.add(article_ten)
session.commit()

article_eleven = Article(parent_id=5, title="Bootstrap", article_text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer ullamcorper, ex a mattis maximus, acu nibh bibendum ante, tincidunt varius justo velit ut risus.", owner='admin')
session.add(article_eleven)
session.commit()

article_twelve = Article(parent_id=6, title="From Design to Production in Minutes", article_text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer ullamcorper, ex a mattis maximus, acu nibh bibendum ante, tincidunt varius justo velit ut risus.", owner='admin')
session.add(article_twelve)
session.commit()

user_one = User(username='Dipl.-Ing. Sonya Eigenwillig MBA.', picture="http://www.galli-gentile.net/privacy.jsp", email='feijoo.nora@ferrandez.com')
session.add(user_one)
session.commit()

user_two = User(username='Dipl.-Ing. Eugenio Birnbaum', picture="http://www.taesche.com/", email='satterfield.burnett@hotmail.com')
session.add(user_two)
session.commit()
