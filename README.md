# Frege Analyzer PHP

## Docker environment variables

   * `RMQ_HOST` - RabbitMQ host
   
   * `RMQ_PORT` - RabbitMQ port 

   * `DB_HOST` - PostgreSQL server host

   * `DB_PORT` - PostgreSQL server host 

   *  `DB_DATABASE` - Database name

   *  `DB_USERNAME` - Database username

   *  `DB_PASSWORD` - Database password
   
   *  `RMQ_REJECTED_PUBLISH_DELAY` - After recieving NACK service will wait as many seconds as the value of this variable is before trying to publish message again

**All the environment variables mentioned above are required to run the container**

## Docker application
Docker image of this app is available as **jagiellonian/frege-analyzer-php**

To run just type e.g. `docker run -it -v /home:/home -e DB_HOST="172.17.0.4" -e DB_PORT="5432" -e DB_USERNAME="postgres" -e DB_PASSWORD="frege_password" -e DB_DATABASE="frege" -e RMQ_HOST="172.17.0.2" -e RMQ_PORT="5672" -e RMQ_REJECTED_PUBLISH_DELAY="5" jagiellonian/frege-analyzer-php:latest
`

To rebuild type `docker build -t jagiellonian/frege-analyzer-php .`