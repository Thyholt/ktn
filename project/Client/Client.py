# -*- coding: utf-8 -*-
import socket
import json
import sys
import codecs
from MessageReceiver import MessageReceiver
from MessageParser import MessageParser

class Client:
    def __init__(self, host, server_port):
        self.host = host
        self.server_port = server_port
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.run()

    def run(self):
        self.connection.connect((self.host, self.server_port))
        self.thread = MessageReceiver(self, self.connection)
        self.thread.start()
        
        while True:
            text = input().split(' ', 1)
            if(len(text) > 0 and len(text) < 3):
                if(len(text)==1):
                    text.append('')
                if(text[0] == 'login'):
                    payload=json.dumps({'request': 'login', 'content': text[1]})
                    self.TX_payload(payload)
                elif(text[0] == 'msg'):
                    payload=json.dumps({'request': 'msg', 'content': text[1]})
                    self.TX_payload(payload)
                elif(text[0] == 'logout'):
                    self.disconnect()
                elif(text[0] == 'names'):
                    payload=json.dumps({'request': 'names'})
                    self.TX_payload(payload)
                elif(text[0] == 'help'):
                    payload=json.dumps({'request': 'help'})
                    self.TX_payload(payload)
                elif(text[0] == 'history'):
                    payload=json.dumps({'request': 'history'})
                    self.TX_payload(payload)
                else:
                    print('Unknown command, type "help" for help \n >', end='')
            else:
                print('Unknown command, type "help" for help \n >', end='')


    def disconnect(self):
        payload=json.dumps({'request': 'logout'})
        self.TX_payload(payload)
        sys.exit()

    def RX_message(self, message):
        parser = MessageParser()
        parsed_message = parser.parse(message)
        print(parsed_message,'\n> ',end='')

    def TX_payload(self, data):
        self.connection.send(bytes(data, 'UTF-8'))


if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.
    No alterations is necessary
    """
    connect_ip=input("Enter server ip to connect: ")
    print('Type "login <username>" to log in','\n> ',end='')
    client = Client(connect_ip, 9998)