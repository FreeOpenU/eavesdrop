# eavesdrop

 ## Synopsis
A sniffing app to pull redundant copies of submission forms or 
other Ethernet traffic. Part of Unhackable Server Project. 

## Code Information

Eavesdrop, sniffs the network, parses out text and saves it to a file.
    Using the command line, it initiates a packet capture that pipes the stdout into the python progra.
    The capture pipes the ENTIRE packet but does not save it because it is not needed. 
    I will save the finished packet as a variable, do what needs to be done and overwrite the variable with the nest packet.
    The app is meant to be as small as possible.
##User Interface
   The user interface, at this point only allows the user (let's call him Dave) to chose with device he want't to sniff on.
   I mean to add some nore functionality:
 
  -[x] Dave can choose what type of payload he wants to save.
  -[ ] Dave can go in and see how many of each kind of requests and responses the device has been receiving.
  -[ ] Dave can choose where the payload is being stored
  -[ ] Dave can kill the sniff
  -[ ] Dave can count/ see a graph of malformed packets to see if Hal is misbehaving
  -[x] Dave can choose which device to sniff on
 

## Installation

This code uses Python 2.7 and t-shark. It also used zlib, scappy,
os, and re (for regular expressions). You also must have root access. I will create a requirements file when I have 
most things functional.
