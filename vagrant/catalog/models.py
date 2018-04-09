from sqlalchemy import Table, Column, Integer, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import(TimedJSONWebSignatureSerializer as Serializer,
 BadSignature, SignatureExpired)
import random, string

Base = declarative_base()

# Secret key used for token based authentication
secret_key = ''.join(random.choice(string.ascii_uppercase + string.digits)
    for x in range(32))

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(32), index=True)
    picture = Column(String)
    email = Column(String)
    password_hash = Column(String(64))
    is_active = Column(String, unique=False, default='False')

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        s = Serializer(secret_key, expires_in = expiration)
        return s.dumps({'id': self.id })

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(secret_key)
        try:
            data = s.loads(token)
        except SignatureExpired:
            #Valid Token, but expired
            return None
        except BadSignature:
            #Invalid Token
            return None
        user_id = data['id']
        print('user id: {}'.format(user_id))
        return user_id

    @property
    def serialize(self):
        return {'id': self.id,
        'username': self.username,
        'picture': self.picture,
        'email': self.email,
        }


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    category = Column(String(32))

    @property
    def serialize(self):
        return {'id': self.id,
        'category': self.category,
        }


class Article(Base):
    __tablename__ = 'article'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('categories.id'))
    title = Column(Text)
    article_text = Column(Text, nullable=False)
    owner = Column(String, nullable=False)
    category = relationship("Category")

    @property
    def serialize(self):
        return {'id': self.id,
        'title': self.title,
        'article_text': self.article_text,
        }


class History(Base):
    __tablename__ = 'history'
    id = Column(Integer, primary_key=True)
    viewer = Column(String, nullable=False)
    action = Column(String, nullable=False)
    viewed_article = Column(Integer, ForeignKey('article.id'))
    article = relationship("Article")


engine = create_engine('sqlite:///catalog.db')
Base.metadata.create_all(engine)
