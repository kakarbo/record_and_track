#!/usr/bin/env python3
""" app """

from argparse import ArgumentParser
from datetime import datetime
import json

from event.event import Submit_event
import models
from models.customer import Customer
from models.base_model import BaseModel
from models.work_orders import Work_order

classes = {"Customer": Customer, "BaseModel": BaseModel, "Work_order": Work_order}


def config_parser():
    parser = ArgumentParser(description='Description')
    parser.add_argument('type', type=str)
    parser.add_argument('client', type=str)
    parser.add_argument('dict', type=str)
    return parser

def create(cls, obj, client=None):
    new_obj = json.loads(obj)
    if cls in classes:
        if client == None:
            instance = classes[cls](**new_obj)
        else:
            id = models.storage.get_id_fo_name_client(classes['Customer'], client)
            new_obj['customer_id'] = id
            instance = classes[cls](**new_obj)

    instance.save()

def finally_order(client):
    result = models.storage.update(
        classes['Customer'],
        classes['Work_order'],
        client
    )
    event = {}
    for client in result:
        event = {
            'id': client.id,
            'first_name': client.first_name,
            'last_name': client.last_name,
            'address': client.address,
            'start_date': client.start_date.strftime("%Y-%m-%d %H:%M:%S"),
            'is_active': str(int(client.is_active)),
            'created_at': client.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
    Submit_event(event)
    print('Su orden a finalizado')

def create_other_order(client, obj):
    models.storage.other_update(
        classes['Customer'],
        classes['Work_order'],
        client
    )
    create('Work_order', obj, client)

def app():
    obj = config_parser()
    args = obj.parse_args()
    type_arg = args.type
    name_class = type_arg.split(' ')[1]
    client = args.client
    name_client = client.split(' ')[1]
    if name_class == 'Customer' or name_class == 'Work_order':
        create(name_class, args.dict, name_client)
    elif name_class == 'finalizar_orden':
        finally_order(name_client)
    elif name_class == 'otra_orden':
        create_other_order(name_client, args.dict)
    

if __name__ == '__main__':
    app()
