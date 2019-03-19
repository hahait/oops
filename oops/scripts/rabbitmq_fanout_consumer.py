#!/usr/bin/env python

import pika,time
import json

def callback(ch,method,properties,body):
    print(body.decode('utf8'))

def Consumer():
    credentials = pika.PlainCredentials('guest', 'Abcd1234!')
    connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.0.22',5672,'/celery',credentials))
    channel = connection.channel()
    channel.exchange_declare(exchange="fanout_test",exchange_type="fanout")
    result = channel.queue_declare(exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange="fanout_test",queue=queue_name)
    channel.basic_consume(callback,queue=queue_name,no_ack=True)

    print('waiting for message....To exit press CTRL+C')
    channel.start_consuming()

if __name__ == "__main__":
    Consumer()