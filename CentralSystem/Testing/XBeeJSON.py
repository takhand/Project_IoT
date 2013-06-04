import serial
from xbee import XBee 
import json


#open serial port at baud rate of 9600 for Apple's Macintosh OSX
ser = serial.Serial('/dev/tty.usbserial-A100RZ4D',9600)

#create object called xbee in respect to the open serial port
xbee = XBee(ser, escaped=True)

class kobe:
	def bryant(self): 
		return 'hello'
c = kobe()

g = [2,3,5,555]
cool = [1,2,4,577,85,g]
data = {'a':'A','b':(2,4),'c':3, 'cool':cool, 'class':c.bryant()}
# print 'DATA', repr(data)

unsort = json.dumps(data)
sep = json.dumps(data, separators=(',',':'))
newR = unsort.replace('}]',')')
newR = newR.replace('[{','(')
print unsort

print type(unsort)
print len(unsort)
d = '}'
print sep
print len(sep)
print newR

# d = 'hello world'
# print d
xbee.tx(dest_addr='\x00\x02', data = sep)
# packet = xbee.wait_read_frame()

ser.close()
