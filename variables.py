import os
import sys

QUEUE_IN = 'analyze-php'
QUEUE_OUT = 'gc'

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

