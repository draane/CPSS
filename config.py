import os

RABBIT_HOST = os.getenv('RABBIT_HOST', '192.168.1.104')
EXCHANGE_NAME = 'repository_exchange'
QUEUE_NAME = 'cppcheck'
