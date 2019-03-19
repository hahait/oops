#!/usr/bin/env python
import socket
import sys

messages = ['This is the message. ',
            'It will be sent ',
            'in parts.',
            ]
server_address = ('localhost', 10001)
# Create a TCP/IP socket
socks = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print('connecting to %s port %s' % server_address)
socks.connect(server_address)

for message in messages:
    socks.send(message.encode("utf8"))

while True:
    data = socks.recv(1024)
    print( '%s: received "%s"' % (socks.getsockname(), data))
    if not data:
        print(sys.stderr, 'closing socket', socks.getsockname())
        socks.close()