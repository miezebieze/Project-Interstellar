import socket

s = socket.socket()
host = socket.gethostname()
port = 12345

s.connect((host, port))
letters = 1024
print s.recv(letters)
s.close
