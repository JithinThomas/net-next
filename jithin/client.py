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

    (rsvd, ins_cnt, max_hop_cnt, tot_hop_cnt) = struct.unpack('B B B B', buf[4:8])
    ins_cnt = ins_cnt & 0x1F
    print "rsvd: ", rsvd
    print "ins_cnt: ", ins_cnt
    print "max_hop_cnt: ", max_hop_cnt
    print "tot_hop_cnt: ", tot_hop_cnt

    ins_mask = struct.unpack('H', buf[8:10])[0]
    print "ins_mask: 0x%2X" % ins_mask
    
    idx = 12
    num_int_md_vals = ins_cnt * tot_hop_cnt
    for i in range(num_int_md_vals):
        print i, ": ", socket.ntohl(struct.unpack('I', buf[idx:idx+4])[0])
        idx = idx + 4
