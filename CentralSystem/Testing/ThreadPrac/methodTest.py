import threading
import logging 


logging.basicConfig(level = logging.DEBUG, 
					format = '(%(threadName)s) %(message)s')
log = logging.debug 


class gender:
	def male(self):
		log("I am a boy\n")
	def girl(self):
		log("I am a girl\n")

if __name__ == "__main__":
	g = gender() 

	m = threading.Thread(name='male', target=g.male)
	f = threading.Thread(name='female', target = g.girl)

	m.start()
	f.start()
