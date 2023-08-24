'''Contains the class DBStorage'''

from os import getenv

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import models
from models.base_model import BaseModel, Base


class DBStorage:
    '''Interacts with the PostgreSQL database'''
    __engine = None
    __session = None

    def __init__(self):
        '''instantiate a DBStorage object'''
        POSTGRE_USER = getenv('POSTGRE_USER')
        POSTGRE_PWD = getenv('POSTGRE_PWD')
        POSTGRE_DB = getenv('POSTGRE_DB')
        POSTGRE_HOST = getenv('POSTGRE_HOST')
        self.__engine = create_engine(
            f'postgresql://{POSTGRE_USER}:{POSTGRE_PWD}@{POSTGRE_HOST}/{POSTGRE_DB}'
        )

    def all(self, cls=None):
        '''query on the current database session'''
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = f'{obj.__class_.__name__}.{obj.id}'
                    new_dict[key] = obj
        return new_dict

    def new(self, obj):
        '''add the object to the current database session'''
        self.__session.add(obj)

    def save(self):
        '''commit all changes of the current database session'''
        self.__session.commit()

    def delete(self, obj=None):
        '''delete from the current database session obj if not None'''
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        '''reloads data from the database'''
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        '''call remove method on the private session attibute'''
        self.__session.remove()

    def get(self, cls, id):
        '''
        Returns the object based on the class name and its ID, or
        None if not found
        '''
        if cls not in classes.values():
            return None

        all_cls = models.storage.all(cls)
        for value in all_cls.values():
            if value.id == id:
                return value
        
        return None
