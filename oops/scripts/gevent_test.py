import gevent

def h1():
    print("我执行了 h1 ...")
    print("我回到了 h1 ...")

def h2():
    print("我执行了 h2 ...")
    print("我回到了 h2 ...")

def h3():
    print("我执行了 h3 ...")
    print("我回到了 h3 ...")

gevent.joinall([
    gevent.spawn(h1),
    gevent.spawn(h2),
    gevent.spawn(h3)
])