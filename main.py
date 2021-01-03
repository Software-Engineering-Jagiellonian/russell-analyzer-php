import sys
import pika
import json
import subprocess
import sys
import time

from db import Database
import variables

def RMQ_consumer_callback(ch, method, properties, body):
    ch.stop_consuming()

    try:
        x = json.loads(body.decode('utf-8'))
        repo_id = x["repo_id"]
    except KeyError:
        print("The received message does not contain a valid variable")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        sys.exit(1)
    except json.decoder.JSONDecodeError:
        print("Message received is not a JSON")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        sys.exit(1)

    print(f" [x] From " + variables.QUEUE_IN + f" received: " + x["repo_id"])
    # tutaj wywolanie analizatora repozytorium:
    # 1. Pobierz z bazy danych listę plików
    # 2. Przeanalizuj każdy plik z osobna, każdy plik z osobna oznacz w tabeli jako przeanalizowany
    # 3. Wyślij do tabeli 'gc' potwierdzenie przeanalizowania całego repozytorium
    db_get_files(repo_id)
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

def create_message(repo_id):
    message = {"repo_id": repo_id, "language_id": 7}
    return json.dumps(message)

def RMQ_publisher(rabbitmq_host, rabbitmq_port, queue, repo_id):
        try:
            print(f"Connecting to RabbitMQ ({rabbitmq_host}:{rabbitmq_port})...")
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port))
            channel = connection.channel()
            print("Connected")

            channel.confirm_delivery()

            channel.queue_declare(queue=queue, durable=True)

            while True:
                try:
                    channel.basic_publish(exchange='',
                                      routing_key=queue,
                                      properties=pika.BasicProperties(
                                          delivery_mode=2,  # make message persistent
                                      ),
                                      body=bytes(create_message(repo_id), encoding='utf8'))
                    print("Message was received by RabbitMQ")
                    break
                except pika.exceptions.NackError:
                    print("Message was REJECTED by RabbitMQ (queue full?) !")
                    time.sleep(5)

        except pika.exceptions.AMQPConnectionError as exception:
            print(f"AMQP Connection Error: {exception}")
        except KeyboardInterrupt:
            print(" Exiting...")
            try:
                connection.close()
            except NameError:
                pass
            sys.exit(0)

def db_get_files(repo_id):
    # Db init
    db = Database(variables.DB_DATABASE, variables.DB_USERNAME, variables.DB_PASSWORD, variables.DB_HOST, variables.DB_PORT)

    execute_query = "SELECT f.file_path, f.id FROM repository_language_file as f INNER JOIN repository_language as r ON f.repository_language_id = r.id WHERE r.repository_id ='"+repo_id+"' AND language_id = 7 AND r.present = true AND r.analyzed = false"

    db.connect()
    for x in db.execute_query(execute_query):
        print(x[0])
        subprocess.run(["pdepend", "--summary-xml=metrics.xml", x[0]])

    execute_query = "UPDATE repository_language SET analyzed = true where repository_id='"+repo_id+"' AND language_id = 7"
    db.execute_query(execute_query)
    db.close()
    RMQ_publisher(variables.RMQ_HOST, variables.RMQ_PORT, variables.QUEUE_OUT, repo_id)


if __name__ == '__main__':
    RMQ_consumer(variables.RMQ_HOST, variables.RMQ_PORT, variables.QUEUE_IN)
