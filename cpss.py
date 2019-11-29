import functools
import git
import os
import pika
import threading
import json

from config import RABBIT_HOST, EXCHANGE_NAME, QUEUE_NAME

THREAD_NUMBER = 4

CLONE_PATH = "./temp/"


def analyze(repo):
    repo_path = CLONE_PATH + '/' + repo['name'] + '/'

    print("cloning:", repo['full_name'])
    clone_url = repo['clone_url']
    try:
        os.mkdir(CLONE_PATH)
    except FileExistsError:
        pass
    git.Repo.clone_from(url=clone_url, to_path=repo_path)

    print("Executing cppcheck")
    report_name = repo['full_name'].replace('/', '.')
    os.system("cppcheck " + repo_path + " --quiet --xml 2>reports/" + repo['full_name'].replace('/', '.') + ".xml")

    print("removing the folder for", repo['name'])
    os.system("rm -rf " + repo_path)


def ack_message(channel, delivery_tag):
    if channel.is_open:
        channel.basic_ack(delivery_tag)


def do_work(connection, channel, delivery_tag, body):
    repo = json.loads(body.decode('utf-8'))
    analyze(repo)

    # send ack
    cb = functools.partial(ack_message, channel, delivery_tag)
    connection.add_callback_threadsafe(cb)


def on_message(channel, method_frame, header_frame, body, args):
    (connection, threads) = args
    delivery_tag = method_frame.delivery_tag
    t = threading.Thread(target=do_work, args=(connection, channel, delivery_tag, body))
    t.start()
    threads.append(t)


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

    threads = []
    callback = functools.partial(on_message, args=(connection, threads))

    rabbitmq.basic_qos(prefetch_count=THREAD_NUMBER)
    rabbitmq.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=False)

    try:
        rabbitmq.start_consuming()
    except KeyboardInterrupt:
        rabbitmq.stop_consuming()

    for thread in threads:
        thread.join()


if __name__ == '__main__':
    main()
