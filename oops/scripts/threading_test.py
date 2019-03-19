from threading import Thread,Event
import threading
import queue
import time
import random

def consumer(name):
    time.sleep(1)
    a = q.get()
    print("%s 消费到了消息 %s" %(name,a))
    # q.task_done()

def producer():
    for i in range(10):
        print("现在生产了消息 %s" %(i))
        q.put("message: %s" %(i))

q = queue.Queue(maxsize=10)

q.join()
producer()
# for j in range(3):
#     thread_name = "producer-" + str(j)
#     th_pro = threading.Thread(target=producer,name=thread_name, args=(thread_name,))
#     th_pro.start()

threadings = []
for i in range(2):
    thread_name = "consumer-" + str(i)
    thread = threading.Thread(target=consumer,name=thread_name,args=(thread_name,))
    thread.start()
    threadings.append(thread)

for j in threadings:
    j.join()

print("我最后或的 queue 元素是: ", q.get())
print("现在队列的长度: ", q.qsize())

