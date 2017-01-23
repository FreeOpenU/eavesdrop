# eavesdrop

 ## Synopsis
A sniffing app to pull redundant copies of submission forms or 
other Ethernet traffic. Part of Unhackable Server Project. 

## Code Information

Eavesdrop, sniffs the network, parses out plain texts and saves it to a file.
    Using the command line, it initiates a packet capture and saves it to a file called Eavesdrop_Data.pcap.
Then, it takes the pcap file, parses out form submissions, and saves them to a file. The capture is initialized to stop
 after 1,000 packet captures but you can change it manually by going into the code and changing the -c parameter 
 to whatever value you like:
 
The UI works for normal short term sniffs but I will have to figure out how to add functionality for long term use: 1) kill a sniff 2) process captures continously 3)download dependencies
## Installation

This code uses Python 2.7 and t-shark. It also used zlib, scappy,
os, and re (for regular expressions). You also must have root access.
