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

SRC_IP_POS = {}

while 1:
    nbytes, sender = sk.recvfrom_into(buf)
    print "============== [", msg_id, "] =============="
    for i in range(nbytes):
        sys.stdout.write("%02X " % buf[i])
        if (i % 4 == 3):
            sys.stdout.write('\n')
        
    msg_id = msg_id + 1

    src_ip = struct.unpack('I', buf[0:4])[0]
    dst_ip = struct.unpack('I', buf[4:8])[0]
    src_port = struct.unpack('H', buf[8:10])[0]
    dst_port = struct.unpack('H', buf[10:12])[0]
    vni_and_proto = struct.unpack('I', buf[12:16])[0]
    vni = vni_and_proto >> 8
    protocol = vni_and_proto & 0x000000FF
    (rsvd, ins_cnt, max_hop_cnt, tot_hop_cnt) = struct.unpack('B B B B', buf[20:24])
    ins_cnt = ins_cnt & 0x1F
    print "srcIP: %08X" %src_ip
    print "dstIP: %08X" % dst_ip
    print "srcPort: %04X" % src_port
    print "dstPort: %04X" % dst_port
    print "vni_and_proto: %08X" % vni_and_proto
    print "vni: %08X" % vni
    print "proto: %02X" % protocol
    print "rsvd: ", rsvd
    print "ins_cnt: ", ins_cnt
    print "max_hop_cnt: ", max_hop_cnt
    print "tot_hop_cnt: ", tot_hop_cnt

    ins_mask = struct.unpack('H', buf[24:26])[0]
    print "ins_mask: 0x%2X" % ins_mask

    idx = 28
    num_int_md_vals = ins_cnt * tot_hop_cnt
    for i in range(num_int_md_vals):
        print i, ": ", socket.ntohl(struct.unpack('I', buf[idx:idx+4])[0])
        idx = idx + 4
