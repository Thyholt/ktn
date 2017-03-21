# -*- coding: utf-8 -*-
import socketserver as SocketServer
import json, re, time

class ClientHandler(SocketServer.BaseRequestHandler):
    """
    This is the ClientHandler class. Everytime a new client connects to the
    server, a new ClientHandler object will be created. This class represents
    only connected clients, and not the server itself. If you want to write
    logic for the server, you must write it outside this class
    """

    def handle(self):
        """
        This method handles the connection between a client and the server.
        """
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request
        self.user = None
        server.connections.append(self)
        
        # Loop that listens for messages from the client
        while True:
            try:
                recv = json.loads(self.connection.recv(4096).decode('utf-8'))
            except Exception as e:
                self.logout()
                break
            
            if(recv['request'] == 'login'):
                self.login(recv)
            elif(recv['request'] == 'logout'):
                if(self.user == None):
                    self.error('Not logged in')
                else:
                    self.logout()
                    break
            elif(recv['request'] == 'msg'):
                if(self.user == None):
                    self.error('Not logged in')
                else:
                    self.message(recv)
                pass
            elif(recv['request'] == 'names'):
                if(self.user == None):
                    self.error('Not logged in')
                else:
                    self.names()
            elif(recv['request'] == 'help'):
                self.help()
            else:
                self.error('Unknown request')
    
    def history(self):
        payload = {'timestamp': int(time.time()), 'sender': '[Server]', 'response': 'history', 'content': []}
        for message in server.messages:
            payload['content'].append(message)
        self.send_payload(json.dumps(payload))
    
    def login(self, recv):
        if re.match("^[A-Za-z0-9_-]+$", recv['content']):
            print(recv['content'],'logged in')
            self.user = recv['content']
            
            #GET HISTORY
            self.history()      
            
            msg = {'timestamp': int(time.time()), 'sender': '[Server]', 'response': 'info', 'content': self.user+' connected'}
            payload = json.dumps(msg)   
            for connected in server.connections:
                if(connected.user != None):
                    connected.send_payload(payload)
            server.messages.append(msg)
        else:
            self.error('Invalid username')
        
    def logout(self):
        server.connections.remove(self)
        self.connection.close()
        if(self.user != None):
            print(self.user,'logged out')
            msg = {'timestamp': int(time.time()), 'sender': '[Server]', 'response': 'info', 'content': self.user+' disconnected'}
            payload = json.dumps(msg)   
            for connected in server.connections:
                if(connected.user != None):
                    connected.send_payload(payload)
            server.messages.append(msg)
        
    def message(self, recv):
        msg = {'timestamp': int(time.time()), 'sender': self.user, 'response': 'msg', 'content': recv['content']}
        payload = json.dumps(msg)   
        for connected in server.connections:
            if(connected.user != None):
                connected.send_payload(payload)
        server.messages.append(msg)
    
    def names(self):
        names=""
        for connected in server.connections:
            if(connected.user != None):
                names+=connected.user+', '
        payload=json.dumps({'timestamp': int(time.time()), 'sender': '[Server]', 'response': 'info', 'content': 'Connected users: '+names}) 
        self.send_payload(payload)
        
    def help(self):
        payload=json.dumps({'timestamp': int(time.time()), 'sender': '[Help]', 'response': 'info', 'content': 'Avaleable commands: login <uname>, logout, msg <message>, names, help'})
        self.send_payload(payload)
        
    def send_payload(self, data):
        self.connection.send(bytes(data, 'UTF-8'))
        
    def error(self, msg):
        payload=json.dumps({'timestamp': int(time.time()), 'sender': '[Error]', 'response': 'error', 'content': msg})
        self.send_payload(payload)

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    """
    This class is present so that each client connected will be ran as a own
    thread. In that way, all clients will be served by the server.
    No alterations is necessary
    """
    allow_reuse_address = True
    
    connections=[]
    messages=[]

if __name__ == "__main__":
    """
    This is the main method and is executed when you type "python Server.py"
    in your terminal.
    No alterations is necessary
    """
    HOST, PORT = '', 9998
    print('Server running...')  
    
    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()