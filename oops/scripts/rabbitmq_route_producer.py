#!/usr/bin/env python

import json
import pika
import time

def Producer():
    credentials = pika.PlainCredentials('guest', 'Abcd1234')

    n = 1
    while True:
        n = n + 1
        time.sleep(2)
        connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.0.19', 5672, '/celery', credentials))
        chanel = connection.channel()
        chanel.exchange_declare(exchange='route_test', exchange_type='direct')
        msg_error = "消息[ %s ]: 哈喽,我是一个 ERROR 级别消息....." %(n)
        msg_warning = "消息[ %s ]: 哈喽,我是一个 WARNING 级别消息....." % (n)
        msg_info = "消息[ %s ]: 哈喽,我是一个 INFO 级别消息....." % (n)
        chanel.basic_publish(exchange='route_test',routing_key="error",body =msg_error)
        chanel.basic_publish(exchange='route_test', routing_key="warning", body=msg_warning)
        chanel.basic_publish(exchange='route_test', routing_key="info", body=msg_info)
        print(msg_error)
        print(msg_warning)
        print(msg_info)
        connection.close()


if __name__ == "__main__":
    Producer()
