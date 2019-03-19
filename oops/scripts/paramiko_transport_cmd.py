#!/usr/bin/env python

import paramiko
import os
import select
import sys
import termios
import tty
from paramiko.channel import Channel

paramiko.util.log_to_file("haha.log")

trans = paramiko.Transport(('192.168.0.19', 22))
trans.start_client()

prikey = paramiko.RSAKey.from_private_key_file("/root/.ssh/id_rsa")
trans.auth_publickey(username='root', key=prikey)

channel = trans.open_session()
channel.get_pty()
channel.invoke_shell()

oldtty = termios.tcgetattr(sys.stdin)
try:
    tty.setraw(sys.stdin)
    channel.settimeout(0)

    while True:
        readlist, writelist, errlist = select.select([channel, sys.stdin,], [], [])
        if sys.stdin in readlist:
            input_cmd = sys.stdin.read(1)
            channel.sendall(input_cmd)

        if channel in readlist:
            result = channel.recv(1024)
            if len(result) == 0:
                print("\r\n**** EOF **** \r\n")
                break
            sys.stdout.write(result.decode())
            sys.stdout.flush()
finally:
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldtty)

channel.close()
trans.close()