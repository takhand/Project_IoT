import logging 
import threading 

import socket

import serial
from xbee import XBee 

# This logging will help keep track on which thread the message is printed out
logging.basicConfig(level = logging.DEBUG,
					format = '(%(threadName)-10s) %(message)s')
#Instantiate the log debug object for easy log type print
log = logging.debug 

#open serial port at baud rate of 9600 for Apple's Macintosh OSX
ser = serial.Serial('/dev/tty.usbserial-AE01CQAS',9600)

#create object called xbee in respect to the open serial port
xbee = XBee(ser)

host = '' 
port = 8091 
backlog = 5 
size = 20
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.bind((host,port)) 
s.listen(backlog)

def sendToXBee(num):
	xbee.tx(dest_addr='\x00\x02', data = num)


def main():
	while 1: 
		
		log('Listening Request from the Cloud...')
		client, address = s.accept()
		print '...connected from:', address
		data = client.recv(size) 

		log(str(data))

		if data:
			client.send(data)

		client.close()

		data1 = str(data)

		sendToXBee(data1)
		

		
main()

