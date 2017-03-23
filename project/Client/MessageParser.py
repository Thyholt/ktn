import json
from MessageReceiver import MessageReceiver


class MessageParser():
    def __init__(self):
        self.possible_responses = {
            'error': self.parse_error,
            'info': self.parse_info,
            'msg': self.parse_message,
            'history': self.parse_history
        }

    def parse(self, payload):
        if payload['response'] in self.possible_responses:
            return self.possible_responses[payload['response']](payload)
        else:
            return "Response not valid"

    def parse_error(self, payload):
        return "[Error]" + payload['content']

    def parse_info(self, payload):
        return "[Info] " + payload['content']

    def parse_message(self, payload):
        return "[" + str(payload["timestamp"]) + " - " + str(payload['sender']) + "] " + str(payload["content"]) 

    def parse_history(self, payload):
        history = "\n"
        for message in payload['content']:
            parser = MessageParser()
            history += parser.parse(message) + "\n"
        return history