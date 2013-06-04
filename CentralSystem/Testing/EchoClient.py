#!/usr/bin/env python 

""" 
A simple echo client 
""" 

import socket 

host = 'localhost' 
port = 8091
size = 1024 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.connect((host,port)) 
s.send('Hello') 
data = s.recv(size) 
s.close() 
print 'Received:', data