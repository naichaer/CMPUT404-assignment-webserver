import os
import SocketServer

class MyWebServer(SocketServer.BaseRequestHandler):
  
    def handle(self):

        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)	
	#split request to find out method and part of path
	lines = self.data.splitlines()
	splitedLines= lines[0].split()
	method = splitedLines[0]
	direc = splitedLines[1]	 
	
	if method=="GET":
	    #direct path under folder www
	    path = os.path.abspath("www" + direc)

	    if os.path.isfile(path):
		#if path points to a file, get content type and send request
		mytype = path.split(".")[-1]
		if(mytype == "css" or mytype == "html"):
			content = open(path).read()
			self.setHeader("200 OK","text/"+mytype ,content)    
		else:
			self.setHeader("404 Not Found","text/plain","")

	    elif os.path.isdir(path):
		#if path points to a directory, redirects to index.html
		path = path + "/index.html"
		content = open(path).read()
		if os.path.isfile(path):
		    self.setHeader("200 OK","text/html",content)

	    else:
		#path can't be handled, report error
		self.setHeader("404 Not Found","text/plain","")

	else:	
	    #only method "GET" is allowed
	    self.setHeader("405 Method Not Allowed","text/plain","")
	
    def setHeader(self,status,mytype,content):
        response = "HTTP/1.1 "+status+"\r\n"+\
	            "Content-Type: "+mytype+";charset=UTF-8\r\n\r\n"+ \
	            content+"\r\n"
	self.request.sendall(response)
        return
    
if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()