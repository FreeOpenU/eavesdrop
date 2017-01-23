from scapy.all import *
from getHTTPHeaders import HTTPHeaders, extractText
import os
import time


# os.system("tshark  -T fields -e _ws.col.Info -e http -e frame.time -e  "
# "data.data -w Eavesdrop_Data.pcap -c 1000")
def eavesdrop(x,y,T):
    #subprocess.Popen(x, shell=True)
    z = "tshark  -T fields -e _ws.col.Info -e http -e frame.time -e data.data -w Eavesdrop_Data.pcap -c 10"
    subprocess.Popen(x, shell=True,stdout=subprocess.PIPE,)
    p = subprocess.Popen(["cmd", "arg1"], stdout=subprocess.PIPE, bufsize=1)
    with p.stdout:
        for line in iter(p.stdout.readline, b''):
            print line,
    p.wait()
    while not os.path.exists(y):
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
            text = extractText(headers,http_payload,T)
            if text is not None:
                try:
                    text_file = open("Output.txt", "w")
                    text_file.write("Payload:: " % text)
                    text_file.close()
                except:
                    pass

