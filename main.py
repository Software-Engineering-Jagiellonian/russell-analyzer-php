import os
import pika
import sys
import json

LANGUAGE_ID = 7
QUEUE_IN = 'analyze-php'
QUEUE_OUT = 'gc'

REPO_ID = 0

try:
   DB_HOST = os.environ['DB_HOST']
except KeyError:
   print("Please set the environment variable DB_HOST")
   sys.exit(1)
try:
   DB_PORT = os.environ['DB_PORT']
except KeyError:
   print("Please set the environment variable DB_PORT")
   sys.exit(1)
try:
   DB_USERNAME = os.environ['DB_USERNAME']
except KeyError:
   print("Please set the environment variable DB_USERNAME")
   sys.exit(1)
try:
   DB_PASSWORD = os.environ['DB_PASSWORD']
except KeyError:
   print("Please set the environment variable DB_PASSWORD")
   sys.exit(1)
try:
   DB_DATABASE = os.environ['DB_DATABASE']
except KeyError:
   print("Please set the environment variable DB_DATABASE")
   sys.exit(1)
try:
   RMQ_HOST = os.environ['RMQ_HOST']
except KeyError:
   print("Please set the environment variable RMQ_HOST")
   sys.exit(1)
try:
   RMQ_PORT = os.environ['RMQ_PORT']
except KeyError:
   print("Please set the environment variable RMQ_PORT")
   sys.exit(1)


def RMQ_consumer_callback(ch, method, properties, body):
    ch.stop_consuming()

    try:
        x = json.loads(body.decode('utf-8'))
        REPO_ID = x["repo_id"]
    except KeyError:
        print("The received message does not contain a valid variable")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        sys.exit(1)
    except json.decoder.JSONDecodeError:
        print("Message received is not a JSON")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        sys.exit(1)

    print(f" [x] From " + QUEUE_IN + f" received: " + x["repo_id"])
    # tutaj wywolanie analizatora repozytorium
    ch.basic_ack(delivery_tag=method.delivery_tag)


def RMQ_consumer(rabbitmq_host, rabbitmq_port, queue):
    while True:
        try:
            print(f"Connecting to RabbitMQ ({rabbitmq_host}:{rabbitmq_port})...")
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port))
            channel = connection.channel()
            print("Connected")

            channel.queue_declare(queue=queue, durable=True)

            while True:
                channel.basic_consume(queue=queue,
                                      auto_ack=False,
                                      on_message_callback=RMQ_consumer_callback)

                print(' [*] Waiting for a message')
                channel.start_consuming()
        except pika.exceptions.AMQPConnectionError as exception:
            print(f"AMQP Connection Error: {exception}")
        except KeyboardInterrupt:
            print(" Exiting...")
            try:
                connection.close()
            except NameError:
                pass
            sys.exit(0)


if __name__ == '__main__':
    RMQ_consumer(RMQ_HOST, RMQ_PORT, QUEUE_IN)
