#!/usr/bin/env python

import pigpiod
import socket

s = socket.socket(socket.AF_INET, socket.SOC_STREAM)

s.bind((socket.gethostname(), 50007))

s.listen()
(c_sock, addr) = s.accept()
while True:
    read_sockets, write_sockets, error_sockets = select.select(s, [], [])
    data = read_socket[0].recv(4096)
    print data
