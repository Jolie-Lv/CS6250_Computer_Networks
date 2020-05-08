# Project 4 for CS 6250: Computer Networks
#
# This defines a DistanceVector (specialization of the Node class)
# that can run the Bellman-Ford algorithm. The TODOs are all related 
# to implementing BF. Students should modify this file as necessary,
# guided by the TODO comments and the assignment instructions. This 
# is the only file that needs to be modified to complete the project.
#
# Student code should NOT access the following members, otherwise they may violate
# the spirit of the project:
#
# topolink (parameter passed to initialization function)
# self.topology (link to the greater topology structure used for message passing)
#
# Copyright 2017 Michael D. Brown
# Based on prior work by Dave Lillethun, Sean Donovan, and Jeffrey Randow.
        											
from Node import *
from helpers import *

class DistanceVector(Node):
    
    def __init__(self, name, topolink, outgoing_links, incoming_links):
        super(DistanceVector, self).__init__(name, topolink, outgoing_links, incoming_links)

        self.distance_vector = { self.name: 0 }
        # Initially the DV contains only Node's outgoing links
        for link in self.outgoing_links:
            self.distance_vector[link.name] = int(link.weight)
        # Counter variable for counting rounds
        self.rounds = 0

    def send_initial_messages(self):
        msg = (self.name, [])
        for l in self.outgoing_links:
            msg[1].append((l.name, int(l.weight)))
        self.advertise(msg)

    def process_BF(self):      
        update = False
        for msg in self.messages:
            cost = int(self.get_outgoing_neighbor_weight(msg[0]))
            for vertex in msg[1]:
                if vertex[0] not in self.distance_vector.keys():
                    self.distance_vector[vertex[0]] = cost + vertex[1]
                    update = True
                else:
                    # A Node will never advertise a negative distance to itself
                    if vertex[0] != self.name:
                        path_weight = self.distance_vector[vertex[0]]
                        # If downstream advertised -99, set the cost to -99
                        if vertex[1] == -99 and path_weight != -99:
                            self.distance_vector[vertex[0]] = -99
                            update = True
                        elif path_weight != -99 and path_weight > cost + vertex[1]:
                            # Udate path weight to minimum if not in a negative cycle
                            if self.rounds <= len(self.distance_vector.keys()) - 1:
                                self.distance_vector[vertex[0]] = cost + vertex[1]
                                update = True
                            else:
                                # Negative cycle detected! Set the path weight to -99
                                self.distance_vector[vertex[0]] = -99
                                update = True
        # Empty queue
        self.messages = []
        # Send updated DV to neighbors
        if update == True:
            # Increase count
            self.rounds += 1
            msg = (self.name, [])
            for z in self.distance_vector:
                msg[1].append((z, self.distance_vector[z]))
            self.advertise(msg)
    
    def advertise(self, msg):
        for neighbor in self.neighbor_names:
            self.send_msg(msg, neighbor)

    def log_distances(self):       
        add_entry(self.name, self.dv_string())

    def dv_string(self):
        distance_vector = list(
            map(lambda i: '{}{}'.format(i, self.distance_vector[i]), self.distance_vector))

        return ','.join(distance_vector)
