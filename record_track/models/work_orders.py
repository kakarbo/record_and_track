'''holds class work_orders'''

import sqlalchemy
from sqlalchemy import Column, DateTime, String, Foreignkey
from sqlalchemy.orm import relationship

import models
from models.base_model import BaseModel, Base


class Work_orders(BaseModel, Base):
    '''representation of work_orders'''
    __tablename__ = 'work_orders'

    customer_id = Column(String(60), Foreignkey('customers.id'), nullable=False)
    title = Column(String(60), nullable=False)
    planned_date_begin = Column(DateTime, nullable=False)
    planned_date_end = Column(DateTime, nullable=False)
    status = Column(Enum_status, nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
