import logging 
from random import randint
from threading import Thread
from threading import currentThread
from threading import enumerate 
from time import sleep


logging.basicConfig(level = logging.DEBUG, 
					format = '[%(levelname)s] (%(threadName)s) %(message)s',)

log =logging.debug

def daemon():
	log('starting')
	sleep(2)
	log('exiting')

d = Thread(name='daemon', target=daemon)
# d.setDaemon(True)

def non_daemon():
	log('starting')
	log('exiting')

def worker(num):
	log('Worker: '+str(num))
	return

def worker2():
	t = currentThread()
	pause = randint(1,5)
	log('sleeping %s', pause)
	sleep(pause)
	log('ending')
	return

# for i in range(3):
# 	t = Thread(target=worker2)
# 	t.setDaemon(True)
# 	t.start()

# main_thread = currentThread()
# for t in enumerate():
# 	if t is main_thread:
# 		continue 
# 	log('joining %s', t.getName())
# 	t.join()

t = Thread(name='non_daemon', target=non_daemon)

d.start()
t.start() 

# d.join(1)
# print 'd.isAlive()', d.isAlive()
# t.join()




# threads = []

# for i in range(5):
# 	t = Thread(name = 'worker', target=worker, args= (i,))
# 	threads.append(t)
# 	t.start()
	
	