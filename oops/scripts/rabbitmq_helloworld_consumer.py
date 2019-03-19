#!/usr/bin/env python

import pika,time
import json

def backcall(ch,method,properties,body):
    print("Body: %s" %(body.decode('utf8')))
    print("properties: %s" % (properties))

def Consumer():
    credentials = pika.PlainCredentials('guest', 'Abcd1234')
    connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.0.23',56721,'/celery',credentials))
    channel = connection.channel()
    channel.queue_declare(queue='celery',durable=True)
    channel.basic_consume(backcall,queue='celery',no_ack=True)
    print('waiting for message To exit   press CTRL+C')
    channel.start_consuming()

if __name__ == "__main__":
    Consumer()