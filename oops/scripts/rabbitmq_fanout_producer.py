#!/usr/bin/env python

import json
import pika

def Producer():
    credentials = pika.PlainCredentials('guest', 'Abcd1234!')

    n = 1
    while True:
        n = n + 1
        connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.0.22', 5672, '/celery', credentials))
        chanel = connection.channel()
        chanel.exchange_declare(exchange='fanout_test', exchange_type='fanout')
        msg = "消息[ %s ]: 哈喽,我是一个 fanout 消息....." %(n)
        chanel.basic_publish(exchange='fanout_test',routing_key='',body =msg)
        print(msg)
        connection.close()


if __name__ == "__main__":
    Producer()
