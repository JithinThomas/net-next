#!/usr/bin/python

import socket

HOST = "127.0.0.1"
PORT = 54321
MSG_SIZE = 256 

sk = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
sk.bind(( HOST, PORT ))

msg_id = 0 

while 1:
    msg = sk.recv( MSG_SIZE )
    print "[", msg_id, "]", msg 
    msg_id = msg_id + 1 
