#!/usr/bin/env python

# shellys = {"192.168.2.21":"Spuelmaschine", "192.168.2.22":"AP Klaus", "192.168.2.23":"AP Claudia"}
shellys = {"192.168.2.21":"Spuelmaschine", "192.168.2.22":"AP Klaus", "192.168.2.23":"AP Claudia"}

print("start....")

for key, value in shellys.items():
    print("IP {} Alias: {}".format(key, value))
