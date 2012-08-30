
#! /usr/bin/python

import select
import socket

BUFSIZ = 1024

class ChatServer(object):
	"""simple ChatServer"""
	def __init__(self, port):
		self.port = port

		self.srvsock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
		self.srvsock.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
		self.srvsock.bind( ("", port) )
		self.srvsock.listen( 5 )

		self.descriptors = [self.srvsock]
		print 'ChatServer started on port %s' % port

	def run(self):
		while 1:
			(sread, swrite, sexc) = select.select( self.descriptors, [], [] )
			for sock in sread:
				if sock == self.srvsock:
					self.accept_new_connection()
				else:

					incomming_string_f_client = sock.recv(BUFSIZ)

					if incomming_string_f_client == '':
						host,port = sock.getpeername()
						incomming_string_f_client = 'Client left %s:%s\r\n' % (host, port)
						self.broadcast_string( incomming_string_f_client, sock )
						sock.close
						self.descriptors.remove(sock)
					else:
						host,port = sock.getpeername()
						newstr = '[%s:%s] %s' % (host, port, incomming_string_f_client)
						self.broadcast_string( newstr, sock )

	def broadcast_string( self, strng, omit_sock ):
		for sock in self.descriptors:
			if sock != self.srvsock and sock != omit_sock:
				sock.sendall(strng)

	def accept_new_connection( self ):
		newsock, (remhost, remport) = self.srvsock.accept()
		self.descriptors.append( newsock )
		newsock.sendall("You're connected to the Python chatserver\r\n")
		message = 'Client joined %s:%s\r\n' % (remhost, remport)
		self.broadcast_string( message, newsock )


myServer = ChatServer( 2626 )
myServer.run()