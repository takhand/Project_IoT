#------------------ 
#Central Hub - Thasin 
#------------------ 

#--------------Import Library-------------- 
import logging #Used for printing for debug 
import threading #Used for threading 
import requests #Used for HTTP 
import socket 
import json 
from time import sleep 

#Used in conjuction with XBee library 
#for serial communications 
import serial 
#XBee library configure XBee in API mode
from xbee import XBee 
#------------------------------------------- 

host = '' 
port = 8014
backlog = 5 
size = 20
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.bind((host,port)) 
s.listen(backlog)

# This logging will help keep track on which thread the message is printed out
logging.basicConfig(level = logging.DEBUG, format = '(%(threadName)-10s) %(message)s')
#Instantiate the log debug object for easy log type print
log = logging.debug 

#open serial port at baud rate of 9600 for Raspberry Pi's Raspbian
# ser = serial.Serial('/dev/ttyUSB0',9600)

#open serial port at baud rate of 9600 for Apple's Macintosh OSX 
ser = serial.Serial('/dev/tty.usbserial-A100RZ4D', 9600) 

#create object called xbee in respect to the open serial port 
xbee = XBee(ser, escaped=True) 

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
		self.httpPOST() #Call the method that will send the data to the cloud

		sleep(2) #2second delay to limite quota GAE
		
		#Send ACK to the client unit
		try:
			if json.loads(self.data)['R'][0] == True:
				xbee.tx(dest_addr=self.dest, data = '1')
				
				log('send ACK to XBee MY: %s', self.dest.encode('hex'))
		except (TypeError, ValueError) as err:
			log('Error: %s', err)

		return 

	#method where it does HTTP GET request to send information by URL
	def httpPOST(self):
		count = 0;
		while True:
			try: 
				url = str(json.loads(self.data)['Dest'])
				log('Destination: %s', url)
				headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
				r = requests.post(url, data=self.data, headers=headers, timeout=5)

				# #Create the parameters that creats the payload for HTTP request 
				# payload = {'value': self.data, 'sensor': 'test', 
				# 			'temp': self.dest.encode('hex')}
				# #Does the HTTP GET request, sets a timeout for 5 seconds 
				# r = requests.get("http://smart-seating-app.appspot.com/add", 
				# 					params = payload, timeout = 5)


				log(r.url)
				
				if r.status_code is 200: #valid acknowledgement from Cloud
					log('HTTP Response: %s', r.status_code)
					break
				else: #invalid acknowledgement from cloud
					log('HTTP Response: %s', r.status_code)
					count+=1
					if count == 4:
						log('Too much tries!!! send ACK')
						break

			except (TypeError, ValueError) as err: #Handler of HTTP timeout GET request 
				# log(r.history)
				# log(r.status_code)
				log('GET request timeout!!!\n')
				log('Error: %s', err)
				break
		return

class sendToXBee(threading.Thread):
	#instatiate the constructor
	def __init__(self, group=None, target=None, 
				name=None, args=(), kwargs=None, verbose=None):
		#instiateing the thread default parameters 
		threading.Thread.__init__(self, group=group, target=target, 
									name=name, verbose=verbose)
		self.encode = args[0]
		self.decode = args[1]
		self.ack = None 
		return

	def run (self):
		xbee.tx(dest_addr=self.decode['D'], data = self.encode)

		try: 
			while True and self.decode['R'][0] == True:
				self.ack = xbee.wait_read_frame()
				unpackACK = json.loads(self.ack)
				if (unpackACK['S'] == self.decode['D']) and unpackACK['R'][1] == True:
					self.httpACK()
					log('Receive Ack Packet')
					break
		except (TypeError, ValueError) as err: 
			log ('Error: %s', err)

		return 

	def httpACK(self):
		count = 0;
		while True:
			try: 
				url = self.decode['D']
				headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
				r = requests.post(url, data=self.ack, headers=headers, timeout=5)
				log(r.url)
				if r.status_code is 200: 
					log('HTTP Response: %s', r.status_code)
					break
				else: 
					log('HTTP Response: %s', r.status_code)
					count+=1
					if count == 5:
						break
			except (TypeError, ValueError) as err: 
				log('Get request timeout\n')
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

				# while True: 
				# 	#Busy waiting for a packet via XBee transfer 
				# 	packet = xbee.wait_read_frame()
				# 	log('got packet')
				# 	unpack = json.loads(packet['rf_data'])
				# 	try: 
				# 		if unpack['ack'] == True:
				# 			continue 
				# 		else:
				# 			break 
				# 	except: 			
				# 		break
				#Busy waiting for a packet via XBee transfer 
				packet = xbee.wait_read_frame()
				log('got packet')
				log(packet['rf_data'])
				t = sendToCloud(args=(packet,)) #instatiate the sendToCloud thread class

				#decode the hex value of source address to String
				sourceID = packet['source_addr'].encode('hex')	
				t.setName('Sensor: ' + sourceID) #set the name of the thread to the source ID
				t.start() #Start the Thread
				# log('Number of Threads active: ' + threading.active_count())
				# log('Number of Threads running: ' + threading.enumerate())
			
			except KeyboardInterrupt:
				break
			except (TypeError, ValueError) as err:
				log("Error: %s", err)
				log("Try again!\n")

		#Close Serial Port
		ser.close()
		return

	def toCloud(self):
		while True: 
			try:
				log('Listening Request from the Cloud at Port %d', port)
				client, address = s.accept()
				print '...connected from:', address
				
				encodedData = client.recv(size) 
				decodedData = json.loads(encodedData)

				t = sendToXBee(args=(encodedData,decodedData))
				t.setName('Actuator: ' + decodedData['Destination'])
				t.start()

				client.close()
			except (TypeError, ValueError) as err :
				log("error: %s", err)

		client.close()


if __name__ == "__main__" :
	listen = listener()

	ltx = threading.Thread(name='ListenToXBee', target=listen.toXBee)
	ltc = threading.Thread(name='ListenToCloud', target=listen.toCloud)

	log('Initialize Listener')

	ltx.start()
	ltc.start()