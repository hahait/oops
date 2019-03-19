#!/usr/bin/env python

import socketserver
import subprocess

class MyHandler(socketserver.BaseRequestHandler):
    def setup(self):
        print("我接收一个新的连接,客户端地址: ", self.client_address)
        self.request.settimeout(5)

    def handle(self):
        while True:
            cmd = self.request.recv(1024)
            cmd_str = cmd.decode("utf8").strip()
            cmd_result_pre = subprocess.Popen(cmd_str, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            cmd_result = cmd_result_pre.stdout.read()
            cmd_err = cmd_result_pre.stderr.read()
            if cmd_err:
                self.request.sendall(cmd_err)
            else:
                self.request.sendall(cmd_result)

    def finish(self):
        print("我要断开连接了....")

host = ("0.0.0.0",10003)

server = socketserver.ThreadingTCPServer(host,MyHandler)
# server.timeout = 5

server.serve_forever()