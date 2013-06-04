#------------------  
#Central Hub - Thasin
#------------------

#--------------Import Library--------------
import logging #Used for printing for debug 
import threading #Used for threading
import requests #Used for HTTP
import socket
from time import sleep #

#Used in conjuction with XBee library 
#for serial communications
import serial 
#XBee library configure XBee in API mode
from xbee import XBee 
#-------------------------------------------

host = '' 
port = 8091 
backlog = 5 
size = 20
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.bind((host,port)) 
s.listen(backlog)

# This logging will help keep track on which thread the message is printed out
logging.basicConfig(level = logging.DEBUG, 
					format = '(%(threadName)-10s) %(message)s')

#Instantiate the log debug object for easy log type print
log = logging.debug 

#open serial port at baud rate of 9600 for Raspberry Pi's Raspbian
# ser = serial.Serial('/dev/ttyUSB0',9600)

#open serial port at baud rate of 9600 for Apple's Macintosh OSX
ser = serial.Serial('/dev/tty.usbserial-AE01CQAS',9600)

#create object called xbee in respect to the open serial port
xbee = XBee(ser)

#Thread Class where each inidividual client has its own thread class
class sendToCloud(threading.Thread):
	#instatiate the constructor
	def __init__(self, group=None, target=None, 
				name=None, args=(), kwargs=None, verbose=None):
		#instiateing the thread default parameters 
		threading.Thread.__init__(self, group=group, target=target, 
									name=name, verbose=verbose)

		self.data = args[0]['rf_data'] #Data payload in String
		self.dest = args[0]['source_addr'] #Source address in hex
		return

	def run (self):
		log('data recieved %s from XBee ID %s', self.data, self.dest.encode('hex'))
		
		log('Send to to the Cloud')
		self.httpGET() #Call the method that will send the data to the cloud

		sleep(2)#2second delay to limite quota GAE
		
		#Send ACK to the client unit
		xbee.tx(dest_addr=self.dest, data = '1')
		
		log('send ACK to XBee MY: %s', self.dest.encode('hex'))
		return 

	#method where it does HTTP GET request to send information by URL
	def httpGET(self):
		while True:
			try: 
				#Create the parameters that creats the payload for HTTP request 
				payload = {'value': self.data, 'sensor': 'test', 
							'temp': self.dest.encode('hex')}
				#Does the HTTP GET request, sets a timeout for 5 seconds 
				r = requests.get("http://smart-seating-app.appspot.com/add", 
									params = payload, timeout = 5)
				log(r.url)
				
				if r.status_code is 200: #valid acknowledgement from Cloud
					log('HTTP Response: %s', r.status_code)
					break
				else: #invalid acknowledgement from cloud
					log('HTTP Response: %s', r.status_code)
			except (TypeError, ValueError) as err: #Handler of HTTP timeout GET request 
				# log(r.history)
				# log(r.status_code)
				log('GET request timeout!!!\n')
				log('Error: %s', err)
				break
		return


#The Class where it listens from a given port for a packet
class listener:
	#This method Listen for a packet request via XBee moodule
	def toXBee (self): 
		while True: #Always loop until user sends interrupt or XBee port is invalid
			try:
				log('waiting for packets...')

				#Busy waiting for a packet via XBee transfer 
				packet = xbee.wait_read_frame()
				log('got packet')

				#instatiate the sendToCloud thread class
				t = sendToCloud(args=(packet,))
				#decode the hex value of source address to String
				sourceID = packet['source_addr'].encode('hex')
				#set the name of the thread to the source ID
				t.setName('XBee: ' + sourceID)
				#Start the Thread
				t.start()

				log('Number of Threads active: ' + threading.active_count())
				log('Number of Threads running: ' + threading.enumerate())
			
			except KeyboardInterrupt:
				break
		#Close Serial Port
		ser.close()
		return

	def toCloud(self):
		while True: 
			try:
				log('Listening Request from the Cloud at Port %d', port)
				log('Listening Request from the Cloud...')
				client, address = s.accept()
				print '...connected from:', address
				data = client.recv(size) 

				log(str(data))

				if data:
					client.send(data)

				client.close()

				data1 = str(data)

				# sendToXBee(data1)
				xbee.tx(dest_addr='\x00\x02', data = data1)
			except:
				break


if __name__ == "__main__" :
	listen = listener()

	ltx = threading.Thread(name='ListenToXBee', target=listen.toXBee)
	ltc = threading.Thread(name='ListenToCloud', target=listen.toCloud)

	log('Initialize Listener')

	ltx.start()
	ltc.start()
	