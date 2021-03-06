#!/usr/bin/python

import subprocess
import socket
import time

import inspect, os, sys
# From http://stackoverflow.com/questions/279237/python-import-a-module-from-a-folder
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"..")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)

import mosq_test

rc = 1
keepalive = 60
connect_packet = mosq_test.gen_connect("test-helper", keepalive=keepalive)
connack_packet = mosq_test.gen_connack(rc=0)

publish_packet = mosq_test.gen_publish("bridge/reconnect", qos=1, mid=1, payload="bridge-reconnect-message")
puback_packet = mosq_test.gen_puback(mid=1)

disconnect_packet = mosq_test.gen_disconnect()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("localhost", 1889))
sock.send(connect_packet)
connack_recvd = sock.recv(len(connack_packet))

if mosq_test.packet_matches("connack", connack_recvd, connack_packet):
    sock.send(publish_packet)

    puback_recvd = sock.recv(len(puback_packet))

    if mosq_test.packet_matches("puback", puback_recvd, puback_packet):
        sock.send(disconnect_packet)
        rc = 0

sock.close()
    
exit(rc)

