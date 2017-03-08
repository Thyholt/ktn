# This skeleton is valid for both Python 2.7 and Python 3.
# You should be aware of your additional code for compatibility of the Python version of your choice.

import time
from socket import *
from datetime import datetime


# Get the server hostname and port as command line arguments                    
host = '127.0.0.1'# FILL IN START		# FILL IN END
port = 12000# FILL IN START		# FILL IN END
timeout = 5 # in seconds

clientSocket = socket(AF_INET,SOCK_DGRAM)
clientSocket.settimeout(1)

time = time.clock()

# FILL IN END

# Sequence number of the ping message
ptime = 0  

# Ping for 10 times
while ptime < 10:
    ptime += 1
    data = "Ping" + str(ptime) + str(time) 
    
    try:
        timeStart = datetime.now()
        clientSocket.sendto(data.encode("utf-8"), (host, port))
        response, serverAddr = clientSocket.recvfrom(1024)
        timeRecive = datetime.now()
        print("Server response from" + serverAddr[0] + ": " + response.decode("utf-8"))
    except Exception as e:
        print(e)
        print("Request timed out.")
        continue
    totalTime = timeRecive - timeStart
    print ("\nRecived package {} of {} in a total of {} seconds".format(ptime,10,totalTime))

# Close the client socket
clientSocket.close()
