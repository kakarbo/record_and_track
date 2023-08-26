# Record and Track

Este servicio permite registrar y realizar seguimiento a las órdenes de servicio para un predio o cliente particular.

## Execute
Para ejecutar las databases y la API
```
./buildconf/build
```

## App
Interactuar con la databases
### CLI
#### **type**: ```Customer```, ```Word_order```, ```finalizar_orden``` y ```otra_orden```

Para interactuar con la databases hay 4 opciones:

```Customer``` agregar nuevos clientes.

```Word_order``` crea nuevas ordenes de servicio, va con el nombre del ```cliente``` para anexarle la orden.

```finalizar_orden``` finaliza la orden de servicio, y se le pasa el nombre del ```cliente``` para finalizar la orden. 

```otra_orden``` crea otra nueva orden, cancelando la orden anterior, va con la opción ```cliente``` para anexarle la orden al cliente

#### **cliente**: client_name

Esta opción se utiliza con el **type** ```Word_order``` y ```otra_orden``` para anexarlo al cliente, las demas **type** se anexa vacia

#### **ultima opción**: {}

Esta opción recive un diccionario, con sus respectivos datos para ```Customer```, ```Word_order``` y ```otra_orden``` las demás type van vacias


#### Example
##### Nuevo cliente
```
python3 app.py "type Customer" "client " '{"first_name": "Morgan", "last_name": "Stark", "address": "Malibu0"}'
```
##### Nuevo orden
```
python3 app.py "type Work_order" "client Morgan" '{"title": "nuevo servicio"}'
```
##### Finalizar orden
```
python3 app.py "type finalizar_orden" "client Morgan" '{}' 
```

##### Crear otra nueva orden
```
python3 app.py "type otra_orden" "client Juliana" '{"title": "otro nuevo servicio"}'
```

## API

Verificar la documentación de la API
```
http://0.0.0.0:5000/apidocs/
```
