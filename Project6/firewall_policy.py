#!/usr/bin/python
# CS 6250 Spring 2020 - Project 6 - SDN Firewall
# build argyle-v12

from pyretic.lib.corelib import *
from pyretic.lib.std import *
from pyretic.lib.query import packets
from pyretic.core import packet

def make_firewall_policy(config):

    # You may place any user-defined functions in this space.
    # You are not required to use this space - it is available if needed.

    # feel free to remove the following "print config" line once you no longer need it
    # it will not affect the performance of the autograder
    print config

    # The rules list contains all of the individual rule entries.
    rules = []

    for entry in config:

        # TODO - This is where you build your firewall rules...
        # Note that you will need to delete the rule line below when you create your own
        # firewall rules.  Refer to the Pyretic github documentation for instructions on how to
        # format these commands.
        # Example (but incomplete)
        # rule = match(srcport = int(entry['port_src']))
        # The line below is hardcoded to match TCP Port 1080.  You must remove this line
        # in your completed assignments.  Do not hardcode your solution - you must use items
        # in the entry[] dictionary object to build your final ruleset for each line in the
        # policy file.

        # Delete this line when you build your implementation.
        rule = match(dstport=1080, ethtype=packet.IPV4, protocol=packet.TCP_PROTO)

        rules.append(rule)
        pass

    # Think about the following line.  What is it doing?
    allowed = ~(union(rules))

    return allowed
