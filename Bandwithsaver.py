__author__ = 'anand'

#!/usr/bin/env python
import argparse
import string
import os
import sys
import gzip
import cStringIO
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 8800

class ReqHandlr(BaseHTTPRequestHandler):
    """ Our Custom request handler"""
    def do_GET(self):
        """ Handler for the GET requests """
        mystrlist = []
  
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.send_header('Content-Encoding','gzip')
        with open("input.txt", "r") as fobj:
            for line in fobj:
                mystrlist = [str(n) for n in line.strip().split(" ")]
        mystr = " ".join(mystrlist)
        HTML_CONTENT = "<html><body><h1>" + mystr + "</html>"
        zbuf = self.compress_buf(HTML_CONTENT)
        sys.stdout.write("Content-Encoding: gzip\r\n")
        self.send_header('Content-Length',len(zbuf))
        self.end_headers()
        # Send the message to browser
        zbuf = self.compress_buf(HTML_CONTENT)
        sys.stdout.write("Content-Encoding: gzip\r\n")
        sys.stdout.write("Content-Length: %d\r\n" % (len(zbuf)))
        sys.stdout.write("Original Content-Length: %d\r\n" % (len(HTML_CONTENT)))
        sys.stdout.write("compression saved %d chars\r\n" % (len(HTML_CONTENT) - len(zbuf)))
        sys.stdout.write("\r\n")
        self.wfile.write(zbuf)
        return

    def compress_buf(self, buf):
        zbuf = cStringIO.StringIO()
        zfile = gzip.GzipFile(mode = 'wb', fileobj = zbuf, compresslevel = 6)
        zfile.write(buf)
        zfile.close()
        return zbuf.getvalue()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='HTTP Server Compress request')
    parser.add_argument('--port', action="store", dest="port", type=int, default=DEFAULT_PORT)
    given_args = parser.parse_args()
    port = given_args.port
    server_address = (DEFAULT_HOST, port)
    server = HTTPServer(server_address, ReqHandlr)
    server.serve_forever()
