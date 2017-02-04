import pcapy
from getHTTPHeaders import HTTPHeaders, extractText
import os
import time
import subprocess
from scapy.all import *
import subprocess

# os.system("tshark  -T fields -e _ws.col.Info -e http -e frame.time -e  "
# "data.data -w Eavesdrop_Data.pcap -c 1000")
x = "tshark  -T fields -e _ws.col.Info -e http -e frame.time -e data -p -w  E.pcap -c 1"
#y = 'Eavesdrop_Data.pcap'
y = 'Eavesdop_Data.pcap'
T= "text/plain"


def eavesdrop(x,y):
    subprocess.call(x, shell=True)



class Eavesdrop():
    #print device list
    def __init__(self):
        p = subprocess.Popen("tshark -D", stdout=subprocess.PIPE, shell=True)
        self.devList = p.communicate()[0]

    # use to print tshark versions and options then exits
    def info(self):
        p = subprocess.Popen("tshark -h", stdout=subprocess.PIPE, shell=True)
        result = p.communicate()
        self.devList = result[0]
    def contSniff(self):
        p = subprocess.Popen("tshark -V  -p -l  -S '::::END OF PACKET::::::' ", stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, shell=True)
        for line in iter(p.stdout.readline, '\r\n\r\n'):
            data = ""
            if ('::::END OF PACKET::::::' not in line):
                data += line
            print data

