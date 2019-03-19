#!/usr/bin/env python

import socket
import time

sk = socket.socket()
sk.connect(("192.168.0.23", 10003))

while True:
    cmd = input("输入命令: ").strip()
    if not cmd: continue
    sk.sendall(cmd.encode('utf8'))
    try:
        cmd_len_response = sk.recv(1024)
        cmd_len = cmd_len_response.decode("utf8")
        cmd_len_dict = eval(cmd_len)
    except:
        print("没收到服务端返回来的相应内容长度")
        break
    else:
        sk.sendall("我收到了你发过来的 长度标识字符串....".encode("utf8"))

    len_rev = 0
    rev_str = ''
    while len_rev < cmd_len_dict["CMD_RESULT_SIZE"]:
        cmd_response = sk.recv(1024)
        cmd_response_str = cmd_response.decode("utf8")
        rev_str += cmd_response_str
        cmd_response_str_len = len(cmd_response_str)
        len_rev += cmd_response_str_len
    else:
        print(rev_str)
sk.close()