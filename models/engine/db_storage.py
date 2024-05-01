#!/usr/bin/python3
"""

"""
from os import getenv
from sqlalchemy import create_engine
from models.base import Base, BaseModel

class DBStorage:
    """

    """
    __engine = None
    __session = None

    def __init__(self):
        """

        """
        username = getenv(HBNB_MYSQL_USER)
        password = getenv(HBNB_MYSQL_PWD)
        host = getenv(HBNB_MYSQL_HOST)
        db_name = getenv(HBNB_MYSQL_DB)
        DATABASE_URL = "mysql+mysqldb://{}:{}@{}:3306/{}".format(
            username, password, host, db_name
        )
        self.__engine = create_engine(
            DATABASE_URL,
            pool_pre_ping=True #check if connection is active
        )
        if env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        objects = dict()
        all_classes = (User, State, City, Amenity, Place, Review)
        if cls == None:
            for class_type in all_classes:
                query = self.__session.query(class_type)
                for obj in query.all():
                    obj_key = '{}.{}'.format(obj.__class__.__name__, obj.id)
                    objects[obj_key] = obj
        else:
            query = self.__session.query(cls)
            for obj in query.all():
                obj_key = '{}.{}'.format(obj.__class__.__name__, obj.id)
                objects[obj_key] = obj
        return objects

    def delete(self, obj=None):
        """Removes an object from the storage database"""
        if obj is not None:
            self.__session.query(type(obj)).filter(
                type(obj).id == obj.id).delete(
                synchronize_session=False
            )

    def new(self, obj):
        """Adds new object to storage database"""
        if obj is not None:
            try:
                self.__session.add(obj)
                self.__session.flush()
                self.__session.refresh(obj)
            except Exception as ex:
                self.__session.rollback()
                raise ex

    def save(self):
        """Commits the session changes to database"""
        self.__session.commit()

    def reload(self):
        """Loads storage database"""
        Base.metadata.create_all(self.__engine)
        SessionFactory = sessionmaker(
            bind=self.__engine,
            expire_on_commit=False
        )
        self.__session = scoped_session(SessionFactory)()

    def close(self):
        """Closes the storage engine."""
        self.__session.close()    