from Message import *
from StpSwitch import *


class Switch(StpSwitch):

    def __init__(self, idNum, topolink, neighbors):
        super(Switch, self).__init__(idNum, topolink, neighbors)

        self.root = self.switchID
        self.distance = 0
        self.upstream = (self.switchID, self.distance)
        self.downstream = []

    def send_initial_messages(self):
        for link in self.links:
            self.send_message(
                Message(self.root, self.distance, self.switchID, link, False))
        return

    def process_message(self, message):
        if message.pathThrough == True and (message.origin not in self.downstream):
            self.downstream.append(message.origin)

        if message.pathThrough == False and message.origin in self.downstream:
            self.downstream.remove(message.origin)

        if (message.root < self.root) or ((message.root == self.root) and (message.distance < self.upstream[1])) or ((message.root == self.root) and (message.distance == self.upstream[1]) and (self.upstream[0] > message.origin)):
            self.root = message.root
            self.distance = message.distance + 1
            self.upstream = (message.origin, message.distance)
            for link in self.links:
                if link != message.origin:
                    self.send_message(
                        Message(self.root, self.distance, self.switchID, link, False))
                else:
                    self.send_message(
                        Message(self.root, self.distance, self.switchID, link, True))
        return

    def generate_logstring(self):
        if self.upstream[0] != self.switchID:
            self.downstream.append(self.upstream[0])

        active_links = list(
            map(lambda link: '{} - {}'.format(self.switchID, link), sorted(self.downstream)))

        return ', '.join(active_links)
