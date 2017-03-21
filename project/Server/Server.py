# -*- coding: utf-8 -*-
import socketserver as SocketServer
import json, re, time

class ClientHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request
        self.user = None

        self.possible_requests = {
            'login': self.login,
            'logout': self.logout,
            'msg': self.message,
            'names': self.names,
            'help': self.help,
            'history': self.history
        }

        server.connections.append(self)

        while True:
            try:
                recv_msg = json.loads(self.connection.recv_msg(4096).decode('utf-8'))
            except Exception as e:
                #self.logout(False)
                break
            if(len(recv_msg['request'])):
                self.possible_requests[recv_msg['request']](recv_msg)
            else:
                self.error('Unknown request')



    def history(self, recv_msg):
        if(self.user == None):
            self.error('Not logged in')
        else:
            payload = {'timestamp': int(time.time()), 'sender': '[Server]', 'response': 'history', 'content': []}
            for message in server.messages:
                payload['content'].append(message)
            self.TX_payload(json.dumps(payload))
    
    def login(self, recv_msg):
        if re.match("^[A-Za-z0-9_-]+$", recv_msg['content']):
            print(recv_msg['content'],'logged in')
            self.user = recv_msg['content']
            self.history(recv_msg)      
            msg = {'timestamp': int(time.time()), 'sender': '[Server]', 'response': 'info', 'content': self.user+' connected'}
            payload = json.dumps(msg)   
            for connected in server.connections:
                if(connected.user != None):
                    connected.TX_payload(payload)
            server.messages.append(msg)
        else:
            self.error('Invalid username')
        
    def logout(self, recv_msg):
        if(self.user == None):
            self.error('Not logged in')
        else:
            if(self.user == None):
                self.error('Not logged in')
            else:
                server.connections.remove(self)
                self.connection.close()
                print(self.user,'logged out')
                msg = {'timestamp': int(time.time()), 'sender': '[Server]', 'response': 'info', 'content': self.user+' disconnected'}
                payload = json.dumps(msg)   
                for connected in server.connections:
                    if(connected.user != None):
                        connected.TX_payload(payload)
                server.messages.append(msg)
        
    def message(self, recv_msg):
        if(self.user == None):
                    self.error('Not logged in')
        else:
            msg = {'timestamp': int(time.time()), 'sender': self.user, 'response': 'msg', 'content': recv_msg['content']}
            payload = json.dumps(msg)   
            for connected in server.connections:
                if(connected.user != None):
                    connected.TX_payload(payload)
            server.messages.append(msg)
    
    def names(self, recv_msg):
        if(self.user == None):
            self.error('Not logged in')
        else:
            names=""
            for connected in server.connections:
                if(connected.user != None):
                    names+=connected.user+', '
            payload=json.dumps({'timestamp': int(time.time()), 'sender': '[Server]', 'response': 'info', 'content': 'Connected users: '+names}) 
            self.TX_payload(payload)
        
    def help(self, recv_msg):
        payload=json.dumps({'timestamp': int(time.time()), 'sender': '[Help]', 'response': 'info', 'content': 'Avaleable commands: login <uname>, logout, msg <message>, names, help, history'})
        self.TX_payload(payload)
        
    def TX_payload(self, data):
        self.connection.send(bytes(data, 'UTF-8'))
        
    def error(self, msg):
        payload=json.dumps({'timestamp': int(time.time()), 'sender': '[Error]', 'response': 'error', 'content': msg})
        self.TX_payload(payload)

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    allow_reuse_address = True
    
    connections=[]
    messages=[]

if __name__ == "__main__":
    HOST, PORT = '', 9998
    print('Server running...')  

    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()