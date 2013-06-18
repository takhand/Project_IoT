#! /usr/bin/python

import random
import logging
import threading
import time

logging.basicConfig(level = logging.DEBUG, 
					format = '(%(threadName)-10s) %(message)s')
log = logging.debug 

def wait_for_event(e):
	"""wait for the event to be set before doing anything"""
	log('wait_for_event starting')
	event_is_set = e.wait()
	log('event set: %s', event_is_set)

def wait_for_event_timeout(e,t):
	"""wait t seconds and then timeout"""
	while not e.isSet():
		log('wait_for_event_timeout starting')
		event_is_set = e.wait(t)
		log('event set: %s', event_is_set)

		if event_is_set:
			log('processing event')
		else:
			log('doing other work')

class Counter(object):
	def __init__(self, start=0):
		self.lock = threading.Lock()
		self.value = start

	def increment(self):
		log('waiting for lock')
		self.lock.acquire()
		try:
			log('acquire lock')
			self.value = self.value + 1
		finally: 
			self.lock.release()

def worker(c):
	for i in range(2):
		pause = random.random()
		log('Sleeping %0.02f', pause)
		time.sleep(pause)
		c.increment()
	log('Done')


def lock_holder(lock):
	log('Starting')
	while True: 
		lock.acquire()
		try:
			log('Holding')
			time.sleep(0.5)
		finally:
			log('Not Holding')
			lock.release()
		time.sleep(0.5)
	return

def worker2(lock):
	log('Starting')
	num_tries = 0
	num_acquires = 0

	while num_acquires < 3:
		time.sleep(0.5)
		log('Trying to acquire')
		have_it = lock.acquire(False)
		try:
			num_tries += 1
			if have_it:
				log('Iteration %d: acquired', num_tries)
				num_acquires +=1
			else:
				log('Iteration %d: Not acquired', num_tries)
		finally:
			if have_it:
				lock.release()
	log('Done after %d iteration', num_tries)


def worker_with(lock):
	with lock:
		log('Lock acquired via with')

def worker_no_with(lock):
	lock.acquire()
	try:
		log('Lock acquired directly')
	finally:
		lock.release()

def event():
	e = threading.Event()
	t1 = threading.Thread(name='block', target=wait_for_event, args=(e,))
	t1.start()

	t2 = threading.Thread(name='non_block', target=wait_for_event_timeout, args=(e,2))
	t2.start()

	log('waiting before calling Event.set()')
	time.sleep(3)
	e.set()
	log('Event is set')

def resources():
	for i in range(2):
		t = threading.Thread(target = worker, args = (counter,))
		t.start()

	log('waiting for worker threads')
	main_thread = threading.currentThread()
	for t in threading.enumerate():
		if t is not main_thread:
			t.join()
	log('Couter: %d', counter.value)

def resources2():
	holder = threading.Thread(target=lock_holder, args=(lock,), name = 'LockHolder')
	holder.setDaemon(True)
	holder.start()

	worker = threading.Thread(target = worker2, args=(lock,), name = 'Worker' )
	worker.start()

def recources3():
	lock = threading.Lock()
	w = threading.Thread(target=worker_with, args=(lock,))
	nw = threading.Thread(target=worker_no_with, args=(lock,))

	w.start()
	nw.start()

if __name__ == "__main__" :
	# event()
	# resources()
	# resources2()
	recources3()