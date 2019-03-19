#!/usr/bin/env python

import socket
import time

sk = socket.socket()
sk.connect(("192.168.0.23", 10003))

while True:
    cmd = input("输入命令: ").strip()
    if not cmd: continue
    sk.sendall(cmd.encode('utf8'))
    resv_str = sk.recv(1024)
    if not resv_str.decode("utf8"): break
    print(resv_str.decode("utf8"))

sk.close()