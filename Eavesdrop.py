
import subprocess
from scapy.all import *
from getHTTPHeaders import HTTPHeaders, extractText
import os
import time


# os.system("tshark  -T fields -e _ws.col.Info -e http -e frame.time -e  "
# "data.data -w Eavesdrop_Data.pcap -c 1000")
def eavesdrop(x,y):
    subprocess.Popen(x, shell=True)
    while not os.path.exists(x):
        time.sleep(1)
    if os.path.isfile(x):
        data = y
        a = rdpcap(data)
        sessions = a.sessions()
        carved_texts = 1
        for session in sessions:
            http_payload = ""
            for packet in sessions[session]:
                try:
                    if packet[TCP].dport == 80 or packet[TCP].sport == 80:
                     http_payload += str(packet[TCP].payload)
                except:
                    pass
            headers = HTTPHeaders(http_payload)
            if headers is None:
             continue
            text = extractText(headers,http_payload)
            if text is not None:
                try:
                    text_file = open("Output.txt", "w")
                    text_file.write("Payload:: " % text)
                    text_file.close()
                except:
                    pass
