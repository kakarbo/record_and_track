#!/usr/bin/env python3
'''holds class customers'''

from os import getenv

import sqlalchemy
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.orm import relationship

import models
from models.base_model import BaseModel, Base


class Customer(BaseModel, Base):
    '''representation of customers'''
    __tablename__ = 'customers'

    fist_name = Column(String(60), nullable=False)
    last_name = Column(String(60), nullable=False)
    address = Column(String(60), nullable=False)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    is_active = Column(Boolean, nullable=False)
    work_order = relationship('Work_orders', backref='customer')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
