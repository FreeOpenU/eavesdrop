from scapy.all import *
from getHTTPHeaders import HTTPHeaders, extractText
import os
import time



def eavesdrop(x,y):
    p = subprocess.call(x, shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #out = p.stdout.read()
    data = y
    a = rdpcap(data)
    sessions = a.sessions()
    for session in sessions:
        http_payload = ""
        for packet in sessions[session]:
            try:
                http_payload += str(packet[TCP].payload)
            except:
                pass

    text_file = open("Output.txt", "w")
    text_file.write("Payload:: " % http_payload)
    text_file.close()

