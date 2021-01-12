# Frege Analyzer PHP

## Local run
To run this app locally you need a Python3 and `pika` lib.
To install `pika` run `pip3 install pika`.
The application calculates statistics based on the `pdepend` application.

To run this app you need set environment variables: `DB_HOST, DB_PORT, DB_USERNAME, DB_PASSWORD, DB_DATABASE, RMQ_HOST, RMQ_PORT, RMQ_REJECTED_PUBLISH_DELAY`

Then just type `python3 main.py`