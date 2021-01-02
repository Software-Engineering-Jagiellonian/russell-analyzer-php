# Frege Analyzer PHP

## Local run
To run this app locally you need a Python3 and `pika` lib.
To install `pika` run `pip3 install pika`

To run this app you need set a environment variables: `DB_HOST, DB_PORT, DB_USERNAME, DB_PASSWORD, DB_DATABASE, RMQ_HOST, RMQ_PORT`

Then just type `python3 main.py`

## Docker application
Docker image of this app is available as **jagiellonian/frege-analyer-php**

To run just type `docker run -it jagiellonian/frege-analyer-php`
