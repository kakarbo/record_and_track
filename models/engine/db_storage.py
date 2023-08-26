#!/usr/bin/env python3
'''Contains the class DBStorage'''

from datetime import datetime
from os import getenv

from dotenv import load_dotenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import models
from models.base_model import BaseModel, Base
from models.customer import Customer
from models.work_orders import Work_order
from models.work_orders import Status

classes = {"Customer": Customer, "Work_order": Work_order}


class DBStorage:
    '''Interacts with the PostgreSQL database'''
    __engine = None
    __session = None

    def __init__(self):
        '''instantiate a DBStorage object'''
        load_dotenv()
        POSTGRES_USER = getenv('POSTGRES_USER')
        POSTGRES_PWD = getenv('POSTGRES_PWD')
        POSTGRES_DB = getenv('POSTGRES_DB')
        POSTGRES_HOST = getenv('POSTGRES_HOST')
        self.__engine = create_engine(
            f'postgresql://{POSTGRES_USER}:{POSTGRES_PWD}@{POSTGRES_HOST}/{POSTGRES_DB}'
        )

    def all(self, cls=None):
        '''query on the current database session'''
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
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
    
    def get_id_fo_name_client(self, cls, search_client):
        result = self.__session.query(cls).filter(cls.first_name == search_client)
        for client in result:
            return client.id

    def get_client(self, cls, search_client):
        return self.__session.query(cls).filter(cls.first_name == search_client)

    def update(self, customer, work_order, search_client):
        client = self.get_client(customer, search_client)
        id = self.get_id_fo_name_client(customer, search_client)
        client.update(
            {customer.is_active: True, customer.start_date: datetime.utcnow()}
        )
        self.__session.query(work_order).filter(
            work_order.customer_id == id
        ).update({work_order.status: Status.DONE})
        self.__session.commit()
        return client

    def other_update(self, customer, work_order, search_client):
        id = self.get_id_fo_name_client(customer, search_client)
        client = self.get_client(customer, search_client)
        client.update(
            {customer.is_active: False, customer.end_date: datetime.utcnow()}
        )
        self.__session.query(work_order).filter(
            work_order.customer_id == id
        ).update({work_order.status: Status.CANCELLED})
        self.__session.commit()
