import logging 
import serial
import threading
import requests
from xbee import XBee
from time import sleep

logging.basicConfig(level = logging.DEBUG, 
					format = '(%(threadName)-10s) %(message)s')

log = logging.debug 

ser = serial.Serial('/dev/tty.usbserial-AE01CQAS',9600)

xbee = XBee(ser)

class sendToCloud(threading.Thread):
	def __init__(self, group=None, target=None, 
				name=None, args=(), kwargs=None, verbose=None):

		threading.Thread.__init__(self, group=group, target=target, 
									name=name, verbose=verbose)

		self.data = args[0]['rf_data']
		self.dest = args[0]['source_addr']
		return

	def run (self):
		log('data recieved %s from XBee ID %s', self.data, self.dest.encode('hex'))
		
		log('Send to to the Cloud')
		self.httpGET()   

		sleep(2)  
		xbee.tx(dest_addr=self.dest, data = '1')
		
		log('send ACK to XBee MY: %s', self.dest.encode('hex'))
		return 

	def httpGET(self):
		while True:
			try: 
				payload = {'value': self.data, 'sensor': 'test', 
							'temp': self.dest.encode('hex')}
				r = requests.get("http://smart-seating-app.appspot.com/add", 
									params = payload, timeout = 5)
				log(r.url)
				
				if r.status_code is 200:
					log('HTTP Response: %s', r.status_code)
					break
				else: 
					log(r.status_code)
			except: 
				# log(r.history)
				# log(r.status_code)
				log('GET request timeout!!!\n')
				break
		return


class main:
	def listener (self): 
		while True: 
			try:
				log('waiting for packets...')
				packet = xbee.wait_read_frame()
				log('got packet')

				t = sendToCloud(args=(packet,))

				sourceID = packet['source_addr'].encode('hex')
				t.setName('XBee: ' + sourceID)
				t.start()

				log(threading.active_count())
				log(threading.enumerate())
			
			except KeyboardInterrupt:
				break
		ser.close()
		return


if __name__ == "__main__" :
	router = main()
	router.listener()
	log('XBee router stops')