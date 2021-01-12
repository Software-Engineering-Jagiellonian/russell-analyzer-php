FROM python:3.8.6

WORKDIR /app

COPY main.py .
COPY db.py .
COPY db.py .
COPY variables.py .
COPY db_create_table.sql .

RUN pip3 install pika
RUN pip3 install psycopg2

RUN apt-get update
RUN apt-get -y install php-xml
RUN apt-get -y install pdepend
#RUN composer global require 'pdepend/pdepend=*'

CMD [ "python3", "main.py" ]