import serial
from xbee import XBee
import json 


# ser = serial.Serial('/dev/tty.usbserial-AE01CQAS',9600)
ser = serial.Serial('/dev/tty.usbserial-A100RZ4D',9600)


xbee = XBee(ser, escaped=True)

class kobe:
	def bryant(self):
		return 'hello'
c = kobe()

g = [2,3,5,555]
cool = [1,2,4,577,85,g]
data = {'a':'A','b':(2,4),'c':3, 'cool':cool, 'class':c.bryant()}
data1 = {"pwm": { "8": 0, "9": 128 }}

sep = json.dumps(data1, separators=(',',':'))

while True:
	try:
		print "waiting for packet"

		packet = xbee.wait_read_frame()

		print packet['rf_data']

		c = json.loads(packet['rf_data'])
		print c
		# print c['Type']
		xbee.tx(dest_addr='\x00\x02', data = sep)
	except (TypeError, ValueError) as err:
		print "error, try again: %s", err