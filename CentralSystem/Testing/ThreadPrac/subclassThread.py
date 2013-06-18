import threading 
import logging 
import time
from random import randint

logging.basicConfig(level = logging.DEBUG, 
					format = '[%(levelname)s] (%(threadName)s) %(message)s')

log = logging.debug

class MyThread(threading.Thread):
	def run (self):
		log('running')
		pause = randint(1,5)
		timer.sleep(pause)
		log('ending')

		return 

class MyThreadWithArgs(threading.Thread):
	def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
		threading.Thread.__init__(self, group=group, target=target, name=name, verbose=verbose)
		self.args = args
		self.kwargs = kwargs
		return 

	def run (self):
		log('running with %s and %s', self.args, self.kwargs)
		return 

# for i in range(5):
# 	t = MyThreadWithArgs(args=(i,), kwargs={'a':'A', 'b':'B'})
# 	t.start()

def delayed():
	log('worker running')
	return

t1 = threading.Timer(3, delayed)
t1.setName('t1')
t2 = threading.Timer(10, delayed)
t2.setName('t2')

log('starting timer')
t1.start()
t2.start()

log('waiting before cancelling %s', t2.getName())
time.sleep(2)
log('cancelling %s', t2.getName())
# t2.cancel()
log('done')

