#!/usr/bin/env python

import json
import pika
import time

def Producer():
    credentials = pika.PlainCredentials('guest', 'Abcd1234!')
    connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.0.22',5672,'/celery',credentials))
    n = 0
    while n < 200:
        n = n + 1
        time.sleep(1)
        chanel = connection.channel()
        chanel.queue_declare(queue='hello_world')
        msg = "消息[ %s ]: Just For Test Hello World Model"  %(n)
        ''' 
            需要说明的是,下面的 routing_key 要和上面定义的 queue 名一致，
            这是因为 使用的是 默认的 exchange,有这样的限制和特性
       '''
        chanel.basic_publish(exchange='',
                             routing_key='hello_world',
                             body =msg)
        print(msg)

    connection.close()

if __name__ == "__main__":
    Producer()