# -*- coding: utf-8 -*-
import platform
import re
import subprocess


class Eavesdrop(object):
    # print device list
    __version__ = "1.2"
    __author__ = "Vera Worri"

    def __init__(self):  # instance variables
        self.pktCount = 0
        self.malcount = 0
        self.host_name = ""
        self.parsed_packet = {}
        self.current_packet = ""
        self.packets_of_interest = 0
        self.process_list = self.get_other_processes()

    def get_other_processes(self):
        if "Windows" == platform.system():
            self.process_list = "NOT AVAILABLE FOR WINDOWS"
        else:
            p = subprocess.Popen("ps | grep -v grep| grep %s " % ("UserInt.py "), stdout=subprocess.PIPE, shell=True)
            process_list = p.communicate()[0]
            self.process_list = re.compile(r"(?<=\S)\s(?=\d)").split(process_list)
        return self.process_list


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


    def continuous_sniff(self, save, content_type, interface, filename="tmpfl.txt"):
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
                self.host_name, results = self.parse_packets(self.current_packet)
                if save == "YES":
                    self.save_packets(content_type, self.current_packet, results)
                data = ""
            if "malformed" in data:
                self.malcount += 1

        return

    def parse_packets(self, packet):
        "get information out of packets"
        patt = re.compile(r"(?<=Content Type: ).+(?!=\n)", re.IGNORECASE)
        results = re.findall(patt, packet)
        find_ip = re.compile(r"(?<=Source: )\d.+")
        try:
            self.host_name = re.search(find_ip, packet).group(0)
        except:
            self.host_name = "NOT FOUND"

        return self.host_name, results

    def save_packets(self, capture_type, packet, results):
        if capture_type != "" and capture_type in results:
            self.f.write(packet)
            self.packets_of_interest += 1
        elif capture_type == "":
            self.f.write(packet)
            self.packets_of_interest += 1
        return
