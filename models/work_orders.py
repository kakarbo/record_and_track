#!/usr/bin/env python3
'''holds class work_orders'''

from datetime import datetime, timedelta
import enum

import sqlalchemy
from sqlalchemy import Column, DateTime, String, ForeignKey, Enum
from sqlalchemy.orm import relationship

import models
from models.base_model import BaseModel, Base


class Status(enum.Enum):
    NEW = 'new'
    DONE = 'done'
    CANCELLED = 'cancelled'


class Work_order(BaseModel, Base):
    '''representation of work_orders'''
    __tablename__ = 'work_orders'

    customer_id = Column(String(60), ForeignKey('customers.id'), nullable=False)
    title = Column(String(60), nullable=False)
    planned_date_begin = Column(DateTime, nullable=False)
    planned_date_end = Column(DateTime, nullable=False)
    status = Column(Enum(Status), default=Status.NEW, nullable=False)
    customer = relationship('Customer', back_populates='work_order')

    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            if key != "__class__":
                setattr(self, key, value)
            if kwargs.get("planned_date_begin", None) and type(self.created_at) is str:
                self.planned_date_begin = datetime.strptime(kwargs["planned_date_begin"], time)
            else:
                self.planned_date_begin = datetime.utcnow()
            if kwargs.get("planned_date_end", None) and type(self.updated_at) is str:
                self.planned_date_end = datetime.strptime(kwargs["planned_date_end"], time)
            else:
                self.planned_date_end = datetime.utcnow() + timedelta(days=14)
        super().__init__()

