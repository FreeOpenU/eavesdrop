# had to install pyshark
# using Python 2.7.12
class pysharkSniffer():
    import pyshark
    out_string = ""
#cap is where I am saving the packets I get from tshark (cap == capture)
#interface is en0 because I have a mac
# may make this amendable with simple user interface
# using a display_filter because I do not know yet how to make it a capture filter in pyshark
    cap = pyshark.LiveCapture(interface='en0')
#still need to find better parameter for sniff
    cap.sniff(packet_count=50)
# run command

#saving each captured file into a txt file *should I make it a pcap file?
    for pkt in cap:
        out_file = open("Eavesdrop_Data.txt", "w")
        out_string += str(pkt)
        out_string += "\n"
        out_file.write(out_string)
    cap.close()