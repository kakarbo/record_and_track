#!/usr/bin/python3
""" objects that handle all default RestFul API actions for Users """

from datetime import datetime

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from

from models.customer import Customer
from models.work_orders import Work_order
from models import storage
from models.work_orders import Status

@app_views.route('/client_active', methods=['GET'], strict_slashes=False)
@swag_from('documentation/customer/cliente_active.yml')
def get_client_active():
    """
    Retrieves the list of all clients actives
    """
    all_customer = storage.all(Customer, Customer.is_active, True).values()
    list_customer = []
    for user in all_customer:
        list_customer.append(user.to_dict())
    return jsonify(list_customer)


def convert_date(date):
    formato = '%Y-%m-%d %H:%M:%S'
    date = f'{date} 00:00:00'
    date_datetime = datetime.strptime(date, formato)
    return date_datetime

@app_views.route('/status/<status>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/Work_order/status.yml')
def get_order_status(status):
    list_status = ['new', 'done', 'cancelled']
    if status in list_status:
        all_status = storage.all(Work_order, Work_order.status, status.upper()).values()
    else:
        date = convert_date(status)
        all_status = storage.all(Work_order, Work_order.planned_date_begin, status).values()
    list_status = []
    for status in all_status:
        list_status.append(status.to_dict())
    return jsonify(list_status)

@app_views.route('/id/<id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/Work_order/status.yml')
def get_id(id):
    obj = storage.customer_id(Work_order, id)
    order = []
    for customer in obj:
        order.append(customer.to_dict())
    return jsonify(order)
