#!/usr/bin/env python

import pika,time
import json

def backcall(ch,method,properties,body):
    print("Body: %s" %(body.decode('utf8')))
    print("delivery_tag: ", method.delivery_tag)
    ch.basic_ack(delivery_tag = method.delivery_tag)

def Consumer():
    credentials = pika.PlainCredentials('guest', 'Abcd1234!')
    connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.0.22',5672,'/celery',credentials))
    channel = connection.channel()
    channel.exchange_declare(exchange="direct_test",exchange_type="direct")
    channel.queue_declare(queue='direct_test_queue')
    channel.queue_bind(exchange="direct_test", queue="direct_test_queue",routing_key="direct_test_queue_route")
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(backcall,queue='direct_test_queue',no_ack=False)
    print('waiting for message To exit   press CTRL+C')
    channel.start_consuming()

if __name__ == "__main__":
    Consumer()