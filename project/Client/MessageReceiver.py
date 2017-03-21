# -*- coding: utf-8 -*-
from threading import Thread
import json

class MessageReceiver(Thread):
    def __init__(self, client, connection):
        Thread.__init__(self)
        self.daemon = True
        self.client = client
        self.connection = connection
        self.stop = False

    def run(self):
        while not self.stop:
            msg = self.connection.recv(4096).decode('utf-8')
            if not msg:
                break
            else:
                self.client.RX_message(json.loads(msg))