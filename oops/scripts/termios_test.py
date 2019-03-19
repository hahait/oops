#!/usr/bin/env python

import termios
import sys

# def getpass(prompt="Password: "):
#     fd = sys.stdin.fileno()
#     old = termios.tcgetattr(fd)
#     new = termios.tcgetattr(fd)
#     new[3] = new[3] & ~termios.ECHO          # lflags
#     try:
#         termios.tcsetattr(fd, termios.TCSADRAIN, new)
#         passwd = input(prompt)
#     finally:
#         termios.tcsetattr(fd, termios.TCSADRAIN, old)
#     return passwd
#
# password = getpass()
# print("我输入的密码: ", password)

#
# import sys, select, termios, tty
#
# def getKey():
#     tty.setraw(sys.stdin.fileno())
#     # select.select([sys.stdin], [], [], 0)
#     key = sys.stdin.read(1)
#     termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
#     return key
#
# if __name__=="__main__":
#     settings = termios.tcgetattr(sys.stdin)
#     key=getKey()
#     print(key)

import getpass

user = getpass.getuser()
passwd = getpass.getpass("your password:")
print(user, passwd)