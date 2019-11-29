import json
import pika
import requests
import time

from config import RABBIT_HOST, EXCHANGE_NAME, QUEUE_NAME


def publish_repo_list(rabbitmq, pages=10):
    ignore_list = []
    f = open("ignore_list.txt", "r")
    for line in f:
        ignore_list.append(line.strip())

    if pages < 1 or pages > 10:
        pages = 10

    repo_list = []
    for page in range(1, pages+1):
        print("page:", page)
        url = "https://api.github.com/search/repositories?q=language:c&sort=stars&order=desc&per_page=100&page=" + str(page)
        r = requests.get(url)

        data = r.json()

        for repo in data['items']:
            if repo['full_name'] in ignore_list:
                continue

            rabbitmq.basic_publish(
                exchange=EXCHANGE_NAME,
                routing_key='',
                body=json.dumps(repo),
                properties=pika.BasicProperties(content_type='application/json')
            )
            repo_list.append(repo)
            print("new repo:", repo['full_name'])
        time.sleep(2)

    return repo_list


def connectRabbitMQ():
    rabbit_connection = pika.BlockingConnection(pika.ConnectionParameters(RABBIT_HOST))
    rabbitmq = rabbit_connection.channel()
    rabbitmq.exchange_declare(
        exchange=EXCHANGE_NAME,
        exchange_type='fanout',
        durable=True,
        auto_delete=False
    )
    rabbitmq.queue_declare(queue=QUEUE_NAME, durable=True)
    rabbitmq.queue_bind(
        queue=QUEUE_NAME,
        exchange=EXCHANGE_NAME
    )

    return rabbitmq, rabbit_connection


def main():
    rabbitmq, connection = connectRabbitMQ()
    publish_repo_list(rabbitmq=rabbitmq)

    connection.close()


if __name__ == '__main__':
    main()
