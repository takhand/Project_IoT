
import threading 
import logging 
import time
from random import randint

logging.basicConfig(level = logging.DEBUG, 
					format = '[%(levelname)s] (%(threadName)s) %(message)s')

log = logging.debug

def waiting2(cv):
	print threading.currentThread().getName()
	with cv:
		cv.wait() 
	log('hello world2\n')

def waiting(cv):
	with cv:
		cv.wait() 
		log('hello world\n')

def notifying(cv):
	log('starting at 5 seconds\n')
	time.sleep(5)
	with cv:
		cv.notify()
		log('notified!\n')

def main():
	cv = threading.Condition()
	c2 = threading.Condition()

	w2 = threading.Thread(name='waiting2', target=waiting2, args=(c2,))
	w = threading.Thread(name='waiting', target=waiting, args=(cv,))
	n = threading.Thread(name='notifying', target=notifying, args=(c2,))

	w.start()
	n.start()
	w2.start()

if __name__=='__main__':
	main() 