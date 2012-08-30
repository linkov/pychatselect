#! /usr/bin/python
import sys
import socket
import select

BUFSIZ = 1024

class ChatClient():
	""" A simple command line chat client using select """
	
	def __init__(self, host='127.0.0.1', port=2626):
		self.port = int(port)
		self.host = host
		self.clisock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.clisock.connect((host, self.port))
		self.descriptors = [0,self.clisock]
		self.prompt = '> '



	def cmdloop(self):
		while 1:
			sys.stdout.write(self.prompt)
			sys.stdout.flush()
			(sread, swrite, sexc) = select.select(self.descriptors, [],[])
			for sock in sread:
				if sock == 0:
					data = sys.stdin.readline().strip()
					if data: self.clisock.sendall(data)
				elif sock == self.clisock:
					data = sock.recv(BUFSIZ)
					if not data:
						break
					else:
						sys.stdout.write(data + '\n')
						sys.stdout.flush()


if __name__ == "__main__":
	if len(sys.argv)<3:
		sys.exit('Usage: %s host port number' % sys.argv[0])

	client = ChatClient(sys.argv[1],sys.argv[2])
	client.cmdloop()


		