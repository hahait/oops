import greenlet

def haha():
    print("我执行haha() 第一次...")
    he.switch()
    print("我执行haha() 第二次...")
    he.switch()

def hehe():
    print("我执行hehe() 第一次...")
    ha.switch()
    print("我执行hehe() 第二次...")

ha = greenlet.greenlet(haha)
he = greenlet.greenlet(hehe)

ha.switch()