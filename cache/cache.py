#!/usr/bin/env python3

from redis import Redis, ConnectionError


def connect():
    try:
        return Redis(host='localhost', port=6379, db=0)
    except ConnectionError as error:
        print(f'Error de conexión a Redis: {error}')

def Submit_event(event):
    client = connect()
    client.xadd('Orden de servicio finalizada', event)
