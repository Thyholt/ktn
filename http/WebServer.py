from socket import *    

serverSocket = socket(AF_INET, SOCK_STREAM)

serverPort = 6666
serverSocket.bind(('',serverPort))
serverSocket.listen(1)


while True:
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()

    try:
	# Receives the request message from the client
    message =  connectionSocket.recv(1024)
    filepath = message.split()[1]

    f = open(filepath[1:])
    outputdata = f.readlines()
    kk = "HTTP/1.1 200 OK\r\n\r\n"
    connectionSocket.send(OK)
	
    for i in range(0, len(outputdata)):  
        connectionSocket.send(outputdata[i])
    connectionSocket.send("\r\n")
	
    connectionSocket.close()

except IOError:
    NOT_FOUND = "HTTP/1.1 404 NOT FOUND\n\n"
    connectionSocket.send(NOT_FOUND);
	
    connectionSocket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n")

    connectionSocket.close()

serverSocket.close()  

