import pika
import json
import subprocess
import sys
import time
import xml.etree.ElementTree as ET

from db import Database
import variables


def RMQ_consumer_callback(ch, method, properties, body):
    ch.stop_consuming()

    try:
        x = json.loads(body.decode('utf-8'))
        repo_id = x["repo_id"]
        print(f" [x] From " + variables.QUEUE_IN + f" received: " + x["repo_id"])
        calculate_metrics(repo_id)
    except KeyError:
        print("The received message does not contain a valid variable")
    except json.decoder.JSONDecodeError:
        print("Message received is not a JSON")

    ch.basic_ack(delivery_tag=method.delivery_tag)


def RMQ_consumer(rabbitmq_host, rabbitmq_port, queue):
    while True:
        try:
            print(f"{variables.QUEUE_IN} - Connecting to RabbitMQ ({rabbitmq_host}:{rabbitmq_port})...")
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port))
            channel = connection.channel()
            print(f"{variables.QUEUE_IN} - Connected")

            channel.queue_declare(queue=queue, durable=True)

            while True:
                channel.basic_consume(queue=queue,
                                      auto_ack=False,
                                      on_message_callback=RMQ_consumer_callback)

                print(f'[*] {variables.QUEUE_IN} - Waiting for a message')
                channel.start_consuming()
        except pika.exceptions.AMQPConnectionError as exception:
            print(f"{variables.QUEUE_IN} - AMQP Connection Error: {exception}")
        except KeyboardInterrupt:
            print(" Exiting...")
            try:
                connection.close()
            except NameError:
                pass
            sys.exit(0)

def create_message(repo_id):
    message = {"repo_id": repo_id, "language_id": variables.LANGUAGE_ID}
    return json.dumps(message)

def RMQ_publisher(rabbitmq_host, rabbitmq_port, queue, repo_id):
    try:
        print(f"{variables.QUEUE_OUT} - Connecting to RabbitMQ ({rabbitmq_host}:{rabbitmq_port})...")
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port))
        channel = connection.channel()
        print(f"{variables.QUEUE_OUT} - Connected")

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
                print(f"{variables.QUEUE_OUT} - Message was received by RabbitMQ")
                break
            except pika.exceptions.NackError:
                print(f"{variables.QUEUE_OUT} - Message was REJECTED by RabbitMQ (queue {variables.QUEUE_OUT} full?) !")
                time.sleep(5)

    except pika.exceptions.AMQPConnectionError as exception:
        print(f"{variables.QUEUE_OUT} - AMQP Connection Error: {exception}")
    except KeyboardInterrupt:
        print(" Exiting...")
        try:
            connection.close()
        except NameError:
            pass
        sys.exit(0)

def calculate_metrics(repo_id):
    db = Database(variables.DB_DATABASE, variables.DB_USERNAME, variables.DB_PASSWORD, variables.DB_HOST,
                  variables.DB_PORT)

    execute_query = "SELECT f.file_path, f.id FROM repository_language_file as f INNER JOIN repository_language as r ON f.repository_language_id = r.id WHERE r.repository_id ='" + repo_id + "' AND language_id = " + variables.LANGUAGE_ID + " AND r.present = true AND r.analyzed = false"

    db.connect()
    for x in db.execute_query(execute_query, ""):
        print(x[0])
        subprocess.run(["pdepend", "--summary-xml=metrics.xml", x[0]])
        read_metric_from_file(db, x[1])
        print(x[1])

    execute_query = "UPDATE repository_language SET analyzed = true WHERE repository_id='" + repo_id + "' AND language_id = " + variables.LANGUAGE_ID
    db.update(execute_query, "")
    db.close()
    RMQ_publisher(variables.RMQ_HOST, variables.RMQ_PORT, variables.QUEUE_OUT, repo_id)  # send confirmation to gc

def read_metric_from_file(db, repository_language_file_id):
    tree = ET.parse('metrics.xml')
    root = tree.getroot()
    save_metrcis_project(root, db, repository_language_file_id)
    #save__metrics_package(root, db, repository_language_file_id)

def save_metrcis_project(root, db, repository_language_file_id):
    if root.tag == "metrics":
        ahh = 0 if root.attrib.get('ahh') == None else root.attrib.get('ahh')
        andc = 0 if root.attrib.get('andc') == None else root.attrib.get('andc')
        calls = 0 if root.attrib.get('calls') == None else root.attrib.get('calls')
        ccn = 0 if root.attrib.get('ccn') == None else root.attrib.get('ccn')
        ccn2 = 0 if root.attrib.get('ccn2') == None else root.attrib.get('ccn2')
        cloc = 0 if root.attrib.get('cloc') == None else root.attrib.get('cloc')
        clsa = 0 if root.attrib.get('clsa') == None else root.attrib.get('clsa')
        clsc = 0 if root.attrib.get('clsc') == None else root.attrib.get('clsc')
        eloc = 0 if root.attrib.get('eloc') == None else root.attrib.get('eloc')
        fanout = 0 if root.attrib.get('fanout') == None else root.attrib.get('fanout')
        leafs = 0 if root.attrib.get('leafs') == None else root.attrib.get('leafs')
        lloc = 0 if root.attrib.get('lloc') == None else root.attrib.get('lloc')
        loc = 0 if root.attrib.get('loc') == None else root.attrib.get('loc')
        maxDIT = 0 if root.attrib.get('maxDIT') == None else root.attrib.get('maxDIT')
        ncloc = 0 if root.attrib.get('ncloc') == None else root.attrib.get('ncloc')
        noc = 0 if root.attrib.get('noc') == None else root.attrib.get('noc')
        nof = 0 if root.attrib.get('nof') == None else root.attrib.get('nof')
        noi = 0 if root.attrib.get('noi') == None else root.attrib.get('noi')
        nom = 0 if root.attrib.get('nom') == None else root.attrib.get('nom')
        nop = 0 if root.attrib.get('nop') == None else root.attrib.get('nop')
        roots = 0 if root.attrib.get('roots') == None else root.attrib.get('roots')

        query = "INSERT INTO php_metrics_project (repository_language_file_id, ahh, andc, calls, ccn, ccn2, cloc, clsa, clsc, eloc, fanout, leafs, lloc, loc, maxDIT, ncloc, noc, nof, noi, nom, nop, roots)" \
                "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        db.insert(query, (repository_language_file_id, ahh, andc, calls, ccn, ccn2, cloc, clsa, clsc, eloc, fanout, leafs, lloc, loc, maxDIT, ncloc, noc, nof, noi, nom, nop, roots))



if __name__ == '__main__':
    #calculate_metrics('1')
    RMQ_consumer(variables.RMQ_HOST, variables.RMQ_PORT, variables.QUEUE_IN)
