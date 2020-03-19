#!/usr/bin/python
# CS 6250 Spring 2020 - Project 6 - SDN Firewall
# build argyle-v12

from pyretic.lib.corelib import *
from pyretic.lib.std import *
from pyretic.lib.query import packets
from pyretic.core import packet
from pyretic.core.language import match
from pyretic.core.network import IPAddr, MAC


def make_firewall_policy(config):
    print config
    # The rules list contains all of the individual rule entries.
    rules = []
    # Protocol constants from packet.
    both = (match(protocol=packet.TCP_PROTO, ethtype=packet.IPV4) |
            match(protocol=packet.UDP_PROTO, ethtype=packet.IPV4))
    tcp = match(protocol=packet.TCP_PROTO, ethtype=packet.IPV4)
    udp = match(protocol=packet.UDP_PROTO, ethtype=packet.IPV4)
    icmp = match(protocol=packet.ICMP_PROTO, ethtype=packet.IPV4)

    for entry in config:
        # The rules_items list contains all of the individual rule items.
        rule_items = []

        for key, value in entry.iteritems():
            if key != 'rulenum' and value != '-':
                if key == 'macaddr_src':
                    rule_items.append(match(srcmac=MAC(value)))
                elif key == 'macaddr_dst':
                    rule_items.append(match(dstmac=MAC(value)))
                elif key == 'ipaddr_src':
                    rule_items.append(match(srcip=IPAddr(value)))
                elif key == 'ipaddr_dst':
                    rule_items.append(match(dstip=IPAddr(value)))
                elif key == 'port_src':
                    rule_items.append(
                        match(srcport=int(value), ethtype=packet.IPV4))
                elif key == 'port_dst':
                    rule_items.append(
                        match(dstport=int(value), ethtype=packet.IPV4))
                elif key == 'protocol':
                    if value == 'T':
                        rule_items.append(tcp)
                    elif value == 'U':
                        rule_items.append(udp)
                    elif value == 'I':
                        rule_items.append(icmp)
                    elif value == 'B':
                        rule_items.append(both)
                elif key == 'ipproto':
                    rule_items.append(
                        match(protocol=int(value), ethtype=packet.IPV4))
        # Append only non-empty rules.
        if len(rule_items) > 0:
            rule = reduce(lambda x, y: x & y, rule_items)
            rules.append(rule)
        pass

    # Think about the following line.  What is it doing?
    # The line negates all traffic that matches the specified rules.
    allowed = ~(union(rules))

    print allowed

    return allowed
