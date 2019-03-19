#!/usr/bin/env python

import json
import pika
import time

def msg_generator(key_word,n):
    return "消息[ %s ]: 哈喽,我是一个 %s 级别消息....." % (n,key_word)

def Producer():
    credentials = pika.PlainCredentials('guest', 'Abcd1234!')
    connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.1.130', 5672, '/celery', credentials))

    n = 1
    while True:
        n = n + 1
        time.sleep(2)
        chanel = connection.channel()
        chanel.exchange_declare(exchange='topic_test', exchange_type='topic')
        chanel.basic_publish(exchange='topic_test', routing_key="sys.log.info", body=msg_generator("SYS INFO",n))
        print(msg_generator("SYS INFO",n))
        chanel.basic_publish(exchange='topic_test', routing_key="sys.log.warning", body=msg_generator("SYS WARNING",n))
        print(msg_generator("SYS WARNING",n))
        chanel.basic_publish(exchange='topic_test',routing_key="sys.log.error",body =msg_generator("SYS ERROR",n))
        print(msg_generator("SYS ERROR",n))
        chanel.basic_publish(exchange='topic_test', routing_key="cron.log.info", body=msg_generator("CRON INFO",n))
        print(msg_generator("CRON INFO",n))
        chanel.basic_publish(exchange='topic_test', routing_key="cron.log.warning", body=msg_generator("CRON WARNING",n))
        print(msg_generator("CRON WARNING",n))
        chanel.basic_publish(exchange='topic_test', routing_key="cron.log.error", body=msg_generator("CRON ERROR",n))
        print(msg_generator("CRON ERROR",n))
        chanel.basic_publish(exchange='topic_test', routing_key="oops.log.info", body=msg_generator("OOPS INFO",n))
        print(msg_generator("OOPS INFO",n))
        chanel.basic_publish(exchange='topic_test', routing_key="oops.log.warning", body=msg_generator("OOPS WARNING",n))
        print(msg_generator("OOPS WARNING",n))
        chanel.basic_publish(exchange='topic_test', routing_key="oops.log.error", body=msg_generator("OOPS ERROR",n))
        print(msg_generator("OOPS ERROR",n))

        chanel.close()

    connection.close()


if __name__ == "__main__":
    Producer()
