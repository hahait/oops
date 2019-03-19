#!/usr/bin/env python

import socket
import subprocess
import threading
import  socketserver

sk = socket.socket()
sk.bind(("0.0.0.0",10002))
sk.listen(1)
# sk.setblocking(False)

def treading_test(connect):
    while True:
        cmd = connect.recv(1024)
        cmd_str = cmd.decode("utf8").strip()
        # 如果接收不到数据，就只有一种情况：就是客户端断开了连接
        if not cmd_str: break
        cmd_result_pre = subprocess.Popen(cmd_str, shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        cmd_result = cmd_result_pre.stdout.read()
        cmd_err = cmd_result_pre.stderr.read()
        cmd_result_size = len(cmd_result.decode("utf8")) if not cmd_err.decode("utf8") else len(cmd_err.decode("utf8"))
        cmd_size = "{'CMD_RESULT_SIZE': %s}" % (cmd_result_size)
        if cmd_result_size == 0:
            cmd_result = "执行成功...".encode("utf8")
        connect.sendall(cmd_size.encode("utf8"))
        return_str = connect.recv(1024)
        print(return_str.decode("utf8"))
        if cmd_err:
            connect.sendall(cmd_err)
            continue
        connect.sendall(cmd_result)
    connect.close()

while True:
    print("我现在启动了 服务端....")
    connect,ipaddr = sk.accept()
    # connect.setblocking(False)
    print("[%s]我接受了一个客户端连接，客户端 IP: %s" % (connect.getpeername(), ipaddr))
    threading_obj = threading.Thread(target=treading_test,args=(connect,))
    threading_obj.start()
