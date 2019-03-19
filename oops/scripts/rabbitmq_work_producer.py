#!/usr/bin/env python

import json
import pika
import time

def Producer():
    credentials = pika.PlainCredentials('guest', 'Abcd1234!')
    connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.0.22',5672,'/celery',credentials))
    n = 0
    while True:
        n = n + 1
        chanel = connection.channel()
        chanel.exchange_declare(exchange="direct_test",exchange_type="direct")
        chanel.queue_declare(queue='direct_test_queue')
        msg = "消息[ %s ]: Just For Test Direct Model"  %(n)
        chanel.basic_publish(exchange='direct_test',
                             routing_key='direct_test_queue_route',
                             body =msg)
        print(msg)
        chanel.close()

    connection.close()

if __name__ == "__main__":
    Producer()