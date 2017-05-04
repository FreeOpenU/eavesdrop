# -*- coding: utf-8 -*-
import re
import subprocess


class Eavesdrop(object):
    # print device list
    version = "1.2"

    def __init__(self):  # instance variables
        self.pktCount = 0
        self.malcount = 0
        self.host_count = 0
        self.parsed_packet = {}
        self.current_packet = ""
        self.packets_of_interest = 0

    @property
    def get_list(self):
        """Get list of devices available to tshark"""
        p = subprocess.Popen("tshark -D", stdout=subprocess.PIPE, shell=True)
        devlist = p.communicate()[0]
        self.devList = re.compile("[0-9][.]").split(devlist)
        self.devList.pop(0)
        return self.devList

    @property
    def tshark_info(self):
        """Print information about local tshark"""
        p = subprocess.Popen("tshark -h", stdout=subprocess.PIPE, shell=True)
        result = p.communicate()
        self.tsharkInfo = result[0]
        return self.tsharkInfo

    def create_sniff_command(self, interfaces):
        """Creates a sniff command using user Inut data from the TUI"""
        interface = str(interfaces + 1)
        tshark_command = "tshark -i  %s -V  -l -p -S '::::END OF PACKET::::::' " % interface
        return tshark_command

    def parse_packet(self, pkt):
        """Parses packets into a dictionary"""
        packet = {}
        get = packet.get
        headers_subheaders = re.split(r'(?<=\S)\n(?=\S)', pkt)
        for item in headers_subheaders:
            header = re.findall(r'(^(\S.+))', item, re.MULTILINE)
            remains = item.replace(header[0][0], "")
            packet[header[0][0]] = get(remains, "")
        self.packet = packet
        return self.packet

    def continuous_sniff(self, save, content_type, interface, filename):
        """Starts a sniff in promiscuous mode"""
        data = ""
        if content_type == "ALL":
            content_type = ""
        command = self.create_sniff_command(interface)
        self.tshark_sniff = subprocess.Popen(command, stdout=subprocess.PIPE,
                                             stderr=subprocess.PIPE, shell=True)
        if save == "YES":
            self.f = open(filename, 'a+')
            self.f.write("Tshark PID:  " + str(self.tshark_sniff.pid) + '\r\n\r\n\r\n')
        for line in iter(self.tshark_sniff.stdout.readline, ','):

            if ('::::END OF PACKET::::::' not in line):
                data += line
            else:
                self.current_packet = data
                self.pktCount += 1
                if save == "YES":
                    self.save_packets(content_type, self.current_packet)
                data = ""
            if "malformed" in data:
                self.malcount += 1

        return

    def save_packets(self, capture_type, packet):
        patt = re.compile(r"(?<=Content Type: ).+(?!\d)", re.IGNORECASE)
        results = re.findall(patt, packet)
        find_ip = re.compile(r"(?<=Source: )\d.+")
        try:
            ip_addresses = re.search(find_ip, packet).group(0)
        except:
            ip_addresses = "NOT FOUND"
        print (ip_addresses)
        if capture_type != "" and capture_type in results:
            self.f.write(packet)
            self.packets_of_interest += 1
        elif capture_type == "":
            self.f.write(packet)
            self.packets_of_interest += 1

    def terminate_sniff(self):
        self.tshark_sniff.kill()
        self.f.close()
        print("Goodbye")
        return

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

