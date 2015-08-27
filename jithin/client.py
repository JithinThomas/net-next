#!/usr/bin/python

import socket
import sys
import struct

HOST = "127.0.0.1"
PORT = 54321
MSG_SIZE = 256 

MAX_HOP_COUNT = 8 
MAX_INS_COUNT = 8 
MAX_MSG_SIZE = 12 + (MAX_HOP_COUNT * MAX_INS_COUNT * 4)

msg_id = 0 

sk = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
sk.bind(( HOST, PORT ))

buf = bytearray(MAX_MSG_SIZE)

while 1:
    nbytes, sender = sk.recvfrom_into(buf)
    print "============== [", msg_id, "] =============="
    for i in range(nbytes):
        sys.stdout.write("%02X " % buf[i])
        if (i % 4 == 3): 
            sys.stdout.write('\n')
                
    msg_id = msg_id + 1 

    print socket.ntohl(struct.unpack('I', buf[12:16])[0])
    print socket.ntohl(struct.unpack('I', buf[16:20])[0])

