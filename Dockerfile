FROM python:3.8.6-slim-buster

WORKDIR /app

COPY main.py .

RUN pip3 install pika
RUN pip3 install psycopg2
RUN apt install pdepend
RUN composer global require 'pdepend/pdepend=*'

CMD [ "python3", "main.py" ]
