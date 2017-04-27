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
        self.parsed_packet = {}
        self.current_packet = ""

    @property
    def get_list(self):
        p = subprocess.Popen("tshark -D", stdout=subprocess.PIPE, shell=True)
        devlist = p.communicate()[0]
        self.devList = re.compile("[0-9][.]").split(devlist)
        self.devList.pop(0)
        return self.devList

    # use to print tshark versions and options then exits
    @property
    def info(self):
        p = subprocess.Popen("tshark -h", stdout=subprocess.PIPE, shell=True)
        result = p.communicate()
        self.tsharkInfo = result[0]
        return self.tsharkInfo

    # create T-shark sniff command
    def create_sniff_command(self, interfaces):
        interface = str(interfaces + 1)
        tshark_command = "tshark -i  %s -V  -l -p -S '::::END OF PACKET::::::' " % interface
        return tshark_command
    #Parse the packets into ordered dict
    def parse_packet(self, pkt):
        packet = {}
        get = packet.get
        headers_subheaders = re.split(r'(?<=\S)\n(?=\S)', pkt)
        for item in headers_subheaders:
            header = re.findall(r'(^(\S.+))', item, re.MULTILINE)
            remains = item.replace(header[0][0], "")
            packet[header[0][0]] = get(remains, "")
        self.packet = packet
        return self.packet

    def continuous_sniff(self, save, content_type, interface):
        data = ""
        if content_type == "ALL":
            content_type = ""
        if save == "YES":
            self.f = open('pacFile.json', 'a')
        command = self.create_sniff_command(interface)
        self.tshark_sniff = subprocess.Popen(command, stdout=subprocess.PIPE,
                                             stderr=subprocess.PIPE, shell=True)

        for line in iter(self.tshark_sniff.stdout.readline, ','):

            if ('::::END OF PACKET::::::' not in line):
                data += line
            else:
                self.current_packet = data
                self.pktCount += 1
                if save == "YES":
                    self.f.write(str(self.tshark_sniff.pid) + '\r\n\r\n\r\n')
                    self.save_packets(content_type, self.current_packet)
            if "malformed" in data:
                self.malcount += 1
            data = ""
        return

    def save_packets(self, capture_type, packet):
        patt = re.compile(r"(?<=content-type:\s).+(?!\d)", re.IGNORECASE)
        results = re.findall(patt, packet)
        for k in results:
            if capture_type in k:
                self.parsed_packet = self.parse_packet(packet)
                json.dump(self.packet, fp=self.f)

    def terminate_sniff(self):
        self.tshark_sniff.kill()
        self.f.close()
        print("Goodbye")
        return

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
