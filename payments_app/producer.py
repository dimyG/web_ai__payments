import pika
import json
from payments_prj.settings import rabbitmg_host

exchanges = {
    'payments': 'fanout',
}


def publish_message(exchange_name, message, routing_key=''):
    print(f'publishing message to exchange: {exchange_name}, routing_key: {routing_key} message: {message}')
    exchange_type = exchanges.get(exchange_name)

    # Establish a connection to RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmg_host))
    channel = connection.channel()

    # Declare the exchange
    channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_type, durable=True)

    # Publish the message to the exchange
    channel.basic_publish(exchange=exchange_name, routing_key=routing_key, body=json.dumps(message))

    # Close the connection
    connection.close()
