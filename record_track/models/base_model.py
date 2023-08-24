'''Contains class BaseModel'''

from datetime import datetime
from os import getenv
import uuid

import sqlalchemy
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

import models

time = '%Y-%m-%dT%H:%M:%S.%f'

Base = declarative_base()


class BaseModel:
    id = Column(String(60), primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()

    def delete(self):
        '''delete the current instance form the storage'''
        models.storage.delete(self)
