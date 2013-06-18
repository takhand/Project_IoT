import logging
import threading
import time

logging.basicConfig(level = logging.DEBUG, 
					format = '(%(threadName)s) %(message)s')
log = logging.debug 

def consumer(cond): 
	log('Starting consumers thread')
	t = threading.currentThread()
	with cond:
		cond.wait()
		log('Resource is available to consumer')

def producer(cond):
	"""set up the Resource to be used by the consuumer"""
	log('Starting producer thread')
	with cond:
		log('making resource available')
		cond.notifyAll()

def sync():
	condition = threading.Condition()

	c1 = threading.Thread(name='c1', target=consumer, args=(condition,))
	c2 = threading.Thread(name='c2', target=consumer, args=(condition,))
	p = threading.Thread(name='p', target=producer, args=(condition,))

	c1.start()
	time.sleep(2)
	c2.start()
	time.sleep(2)
	p.start()

if __name__ == "__main__" :
	sync()