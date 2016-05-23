#!/usr/bin/env python

import pigpio
import socket, select

connected = False

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', 50007))

pi = pigpio.pi()
pi.set_PWM_frequency(14, 50)

while True:
    #s.bind(('', 50007))
    s.listen(1)
    (c_sock, addr) = s.accept()
    connected = True
    while connected:
        #read_sockets, write_sockets, error_sockets = select.select([s], [], [])
        print "Reading: "
        data = c_sock.recv(4096)#read_sockets[0].recv(4096)
        if not data:
            s.shutdown(socket.SHUT_RDWR)
            connected = False
        else:
            if (data == "open"):
		pi.set_PWM_dutycycle(14, 0)
            elif (data == "close"):
                pi.set_PWM_dutycycle(14, 255)
            print data

