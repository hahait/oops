#!/usr/bin/env python

import pika,time
import json

def callback(ch,method,properties,body):
    print("收到: ",body.decode('utf8'))

def Consumer():
    credentials = pika.PlainCredentials('guest', 'Abcd1234!')
    connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.1.130',5672,'/celery',credentials))
    channel = connection.channel()
    channel.exchange_declare(exchange="topic_test",exchange_type="topic")
    result = channel.queue_declare(exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange="topic_test", queue=queue_name, routing_key="*.log.*")
    channel.queue_bind(exchange="topic_test", queue=queue_name, routing_key="#.error")
    channel.queue_bind(exchange="topic_test", queue=queue_name, routing_key="cron.#")
    channel.basic_consume(callback,queue=queue_name,no_ack=True)

    print('waiting for message....To exit press CTRL+C')
    channel.start_consuming()

if __name__ == "__main__":
    Consumer()