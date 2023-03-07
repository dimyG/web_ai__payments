import pika
import json
import logging
import ssl

logger = logging.getLogger('payments')

exchanges = {
    'payments': 'fanout',
}


class BasicPikaClient:
    def __init__(self, rabbitmq_broker_id, rabbitmq_user, rabbitmq_psw, region: str = 'eu-central-1',
                 rabbitmq_host: str = None, rabbitmq_port: int = None):
        # if rabbitmq_broker_id then we don't use rabbitmq_host and rabbitmq_port
        self.rabbitmq_broker_id = rabbitmq_broker_id
        self.rabbitmq_user = rabbitmq_user
        self.rabbitmq_psw = rabbitmq_psw
        self.region = region
        self.rabbitmq_host = rabbitmq_host
        self.rabbitmq_port = rabbitmq_port

    def connection(self):
        # if rabbitmq_broker_id then we are running on AWS, and we use
        # different connection settings from running locally.
        if self.rabbitmq_broker_id:
            # SSL Context for TLS configuration of Amazon MQ for RabbitMQ
            ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
            ssl_context.set_ciphers('ECDHE+AESGCM:!ECDSA')

            url = f"amqps://{self.rabbitmq_user}:{self.rabbitmq_psw}@{self.rabbitmq_broker_id}.mq.{self.region}.amazonaws.com:5671"
            parameters = pika.URLParameters(url)
            parameters.ssl_options = pika.SSLOptions(context=ssl_context)

            return pika.BlockingConnection(parameters)

        else:
            return pika.BlockingConnection(pika.ConnectionParameters(host=self.rabbitmq_host, port=self.rabbitmq_port))


class PublishClient(BasicPikaClient):

    def publish_message(self, exchange_name, message, routing_key=''):
        logger.debug(f'publishing message to exchange: {exchange_name}, routing_key: {routing_key} message: {message}')
        exchange_type = exchanges.get(exchange_name)

        # Establish a connection to RabbitMQ
        connection = self.connection()
        channel = connection.channel()

        # Declare the exchange
        channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_type, durable=True)

        # Publish the message to the exchange
        channel.basic_publish(exchange=exchange_name, routing_key=routing_key, body=json.dumps(message))

        # Close the connection
        connection.close()
