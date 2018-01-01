# FreeOpenU: Eavesdrop:
#    - T.U.I client
import json
import subprocess
import uuid

class Eavesdrop(object):

    version = "0.1"

    def __init__(self):  # instance variables
        self.pktCount = 0
        self.malcount = 0
        self.host_count = 0
        self.packet = {}
        self.current_frame = ""
        self.packet_id = ""
        self.f = open('pacFile.json', 'a')

    def getList(self):
        p = subprocess.Popen("tshark -D", stdout=subprocess.PIPE, shell=True)
        devlist = p.communicate()[0].split(b"\n")
        self.devList = [str(x) for x in devlist]
        return self.devList

    # use to print tshark versions and options then exits
    def info(self):
        p = subprocess.Popen("tshark -h", stdout=subprocess.PIPE, shell=True)
        result = p.communicate()
        self.tsharkInfo = result[0]
        return self.tsharkInfo
    # create T-shar sniff command
    def create_sniff_command(self, interfaces):
        interface = str(interfaces + 1)
        tshark_command = "tshark -i  %s -V  -l -p -S '::::END OF PACKET::::::' " % interface
        return tshark_command
    #Parse the packets into ordered dict


    def contSniff(self, save, capture_type, interface):
        if capture_type == "ALL":
            capture_type = ""
        command = self.create_sniff_command(interface)  #"tshark -V  -l -p  -S '::::END OF PACKET::::::' "
        data = ""
        this_frame = {}
        all_frames = []
        p = subprocess.Popen(command, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, shell=True)
        self.packet_id = str(uuid.uuid1())
        for line in iter(p.stdout.readline, ','):
            if ('::::END OF PACKET::::::' not in line):
                if ("Frame Number" in line):
                    all_frames.append(this_frame)
                    self.current_frame = line
                    this_frame[self.current_frame] = ""
                    continue
                elif self.current_frame != "":
                    this_frame[self.current_frame] += line
            else:
                self.packet["ID"] = self.packet_id
                self.packet["Frames"] = all_frames
                self.packet["Metadata"] = data
                self.pktCount += 1
                if save == "YES":
                    self.saveSniffs(capture_type, self.packet)
                self.packet_id = str(uuid.uuid1())
            if "malformed" in line:
                self.malcount += 1
        return

    def saveSniffs(self, capture_type, packet):
        found = False
        for frame in packet["Frames"]:
            for k, v in frame.items():
                if capture_type in k:
                    found = True
                if capture_type in v:
                    found = True
        if found == True:
            json.dump(packet, fp=self.f)

    def closeSniff(self):
        self.f.close()

