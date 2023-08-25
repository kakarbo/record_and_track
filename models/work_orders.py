#!/usr/bin/env python3
'''holds class work_orders'''

import enum

import sqlalchemy
from sqlalchemy import Column, DateTime, String, ForeignKey

import models
from models.base_model import BaseModel, Base


class Status(enum.Enum):
    NEW = 'new'
    DONE = 'done'
    CANCELLED = 'cancelled'


class Work_orders(BaseModel, Base):
    '''representation of work_orders'''
    __tablename__ = 'work_orders'

    customer_id = Column(String(60), ForeignKey('customers.id'), nullable=False)
    title = Column(String(60), nullable=False)
    planned_date_begin = Column(DateTime, nullable=False)
    planned_date_end = Column(DateTime, nullable=False)
    status = Column(Enum(Status), nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
