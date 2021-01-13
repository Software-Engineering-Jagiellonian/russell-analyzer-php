# Frege Analyzer PHP

## Local run
To run this app locally you need a `python3`, `php-xml`,`pdepend` and `pika`, `psycopg2` lib.

The application calculates statistics based on the `pdepend` application.

To run this app you need set environment variables: `DB_HOST, DB_PORT, DB_USERNAME, DB_PASSWORD, DB_DATABASE, RMQ_HOST, RMQ_PORT, RMQ_REJECTED_PUBLISH_DELAY`

Then just type `python3 main.py`

## Docker application
Docker image of this app is available as **jagiellonian/frege-analyzer-php**

To run just type e.g. `docker run -it -v /home:/home -e DB_HOST="172.17.0.4" -e DB_PORT="5432" -e DB_USERNAME="postgres" -e DB_PASSWORD="frege_password" -e DB_DATABASE="frege" -e RMQ_HOST="172.17.0.2" -e RMQ_PORT="5672" -e RMQ_REJECTED_PUBLISH_DELAY="5" kamilck13/frege-analyzer-php:latest
`

To rebuild type `docker build -t kamilck13/frege-analyzer-php .`