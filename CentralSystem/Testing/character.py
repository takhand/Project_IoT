import serial
from xbee import XBee
import json 


# ser = serial.Serial('/dev/tty.usbserial-AE01CQAS',9600)
ser = serial.Serial('/dev/tty.usbserial-A100RZ4D',9600)


xbee = XBee(ser, escaped=True)

while True:
	print "waiting for packet"

	packet = xbee.wait_read_frame()

	print packet['rf_data']

	c = json.loads(packet['rf_data'])
	print c
	b = c['analog'][3]
	print b
	print type(c)
	print type(b)