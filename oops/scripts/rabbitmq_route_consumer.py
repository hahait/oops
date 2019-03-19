#!/usr/bin/env python

import pika,time
import json

def callback(ch,method,properties,body):
    print("收到: ",body.decode('utf8'))

def Consumer():
    credentials = pika.PlainCredentials('guest', 'Abcd1234!')
    connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.0.23',56721,'/celery',credentials))
    channel = connection.channel()
    channel.exchange_declare(exchange="route_test",exchange_type="direct")
    result = channel.queue_declare(queue='myqueue',exclusive=False,durable=True)
    # queue_name = result.method.queue
    channel.queue_bind(exchange="route_test", queue="myqueue", routing_key="error")
    channel.basic_consume(callback,queue="myqueue",no_ack=True)

    print('waiting for message....To exit press CTRL+C')
    channel.start_consuming()

if __name__ == "__main__":
    Consumer()