import os
from

os.system("tshark  -T fields -e  data.data -e frame.time -w Eavesdrop_Data.pcap > Eavesdrop_Data.txt -F pcap -c 1000")

# run this to give wireshark root access /Applications/Wireshark.app/Contents/MacOS/Wireshark
data = " Eavesdrop_Data.pcap"
def http_payload_assembler(data):
    texts_detected = 0
    a = s.rdpcap(data)
    sessions = a.sessions()
    for session in sessions:
        http_payload = ""
        for packet in sessions[session]:
            if (packet[s.TCP].dport == 80 or packet[s.TCP].sport == 80):
                http_payload += str(packet[s.TCP].payload)
                print http_payload