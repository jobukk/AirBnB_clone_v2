#!/usr/bin/python3
"""database storage engine"""
from os import getenv
from models.base_model import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import text
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        user = getenv('HBNB_MYSQL_USER')
        password = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST', default = 'localhost')
        database = getenv('HBNB_MYSQL_DB')

        self.__engine = create_engine(
            'mysql+mysqldb://' +
            user +
            ':' +
            password +
            '@' +
            host +
            '/' +
            database,
            pool_pre_ping=True
        )

        if getenv(HBNB_ENV) == 'test':
            Base.metadata.drop_all(bind = self.__engine)

def all(self, cls = None):
    '''query all from db'''
    classes = [User, State, City, Amenity, Place, Review]
    objects = {}

    if cls is not None:
        if cls in classes:
            return {obj.__class__.__name__ + '.' + obj.id:
                    obj for obj in self.__session.qeury(cls).all()}
        else:
            return {}
    else:
        for c in classes:
            for obj in self.__session.query(text(c.__name__)).all():
                objects[obj.__class__.name + '.' + obj.id] = obj
        return objects

def new(self, obj):
    '''adds obj to current db session'''
    if obj is not None:
        try:
            self.__session.add(obj)
            self.__session.flush()
            self.__session.refresh(obj)
        except Exception as x:
            self.__session.rollback()
            raise x

def save(self):
    '''commit all changes to db session'''
    self.__session.commit()

def delete(self, obj=None):
    '''delete from current db session '''
    if obj is not None:
        self.__session.query(type(obj)).filter(
            type(obj).id == obj.id).delete()

def reload(self):
    '''reload db'''
    Base.metadata.create_all(self.__engine)
    session_factory = sessionmaker(bind = self.__engine,
                                    expire_on_commit = False)
    self.__session = scoped_session(session_factory)()

def close(self):
    '''close SQLAlchemy session'''
    self.__session.close()       
