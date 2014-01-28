#!/usr/bin/env python
import SocketServer
import socket
import register
import sys

realTargetPort = 0

class MyTCPHandler(SocketServer.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def setup(self):
        global realTargetPort
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(('localhost', realTargetPort))

    def __del__(self):
        self.sock.close()

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print "{} wrote:".format(self.client_address[0])
        print repr(self.data)

def runProxy(realPort, fakePort):
    global realTargetPort
    realTargetPort = realPort
    server = SocketServer.TCPServer(('', fakePort), MyTCPHandler)
    register.registerAirDrop('MITM-Proxy', fakePort)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()

if __name__ == "__main__":
    if len(sys.argv) < 1:
        sys.stderr.write('Provide port airdrop running on localhost')
        sys.exit(1)
    runProxy(int(sys.argv[1]), 65518)

