from threading import Thread

global a 
a = 1
def counter():
	global a
	while True:
		 a += 1

t = Thread(target=counter)

t.start()

while True:
	print a
