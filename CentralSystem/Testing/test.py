#!/usr/bin/env python 

""" 
A simple echo server 
""" 

import socket 

host = '' 
port = 8088

backlog = 5 
size = 20
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.bind((host,port)) 
s.listen(backlog) 

while 1: 
	print 'waiting for packet'
 	client, address = s.accept() 
 	print '...connected from:', address 
 	data = client.recv(size) 
 	print data
 	if data: 
 	    client.send(data) 
 	client.close() 
