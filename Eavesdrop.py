# had to install pyshark
# using Python 2.7.12
import pyshark
#cap is where I am saving the packets I get from tshark (cap == capture)
#interface is en0 because I have a mac
# may make this amendable with simple user interface
# using a display_filter because I do not know yet how to make it a capture filter from pyshark
cap = pyshark.LiveCapture(interface='en0', display_filter='http.request.method =="POST"')
#still need to find better parameter for sniff
cap.sniff(timeout=50)
cap
#saving each captured file into a txt file *should I make it a pcap file?
for pkt in cap:
    with open("Saved_Data.txt", "w") as text_file:
        text_file.write("Packet: {}".format(pkt))

print ('Done!')