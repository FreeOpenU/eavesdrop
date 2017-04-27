# FreeOpenU: Eavesdrop:
#    - T.U.I client
import json
import re
import subprocess


class Eavesdrop(object):
    #print device list
    version = "0.1"

    def __init__(self):  # instance variables
        self.pktCount = 0
        self.malcount = 0
        self.host_count = 0
        self.packet = {}
        self.f = open('pacFile.json', 'a')

    def getList(self):
        p = subprocess.Popen("tshark -D", stdout=subprocess.PIPE, shell=True)
        devlist = p.communicate()[0]
        self.devList = re.compile("[0-9][.]").split(devlist)
        self.devList.pop(0)
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
    def parsePacket(self,pkt):
        packet = {}
        get = packet.get
        headers_subheaders = re.split(r'(?<=\S)\n(?=\S)', pkt)
        for item in headers_subheaders:
            header = re.findall(r'(^(\S.+))', item, re.MULTILINE)
            remains = item.replace(header[0][0], "")
            packet[header[0][0]] = get(remains, "")
        self.packet = packet
        return self.packet

    def contSniff(self, save, capture_type, interface):
        if capture_type == "ALL":
            capture_type = ""
        command = self.create_sniff_command(interface)  #"tshark -V  -l -p  -S '::::END OF PACKET::::::' "
        data = ""
        p = subprocess.Popen(command, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, shell=True)
        for line in iter(p.stdout.readline, ','):
            if ('::::END OF PACKET::::::' not in line):
                data += line
            else:
                packet = data
                self.pktCount += 1
                if save == "YES":
                    self.packet = self.parsePacket(packet)
                    self.saveSniffs(capture_type, self.packet)
            if "malformed" in data:
                self.malcount += 1
        return

    def saveSniffs(self, capture_type, packet):
        found = False
        for k, v in packet.items():
            if capture_type in k:
                found = True
            if capture_type in v:
                found = True
        if found == True:
            json.dump(packet, fp=self.f)

    def closeSniff(self):
        self.f.close()
