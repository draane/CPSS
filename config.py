import os

RABBIT_HOST = os.getenv('RABBIT_HOST', 'localhost')
EXCHANGE_NAME = 'repository_exchange'
QUEUE_NAME = 'cppcheck'
