import re
import subprocess
import json
from collections import OrderedDict


class Eavesdrop():
    # print device list
    def __init__(self):
        pass

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
        self.devList = result[0]

    # Parse the packets into ordered dict
    def parsePacket(self, pkt):
        patt = re.compile("[^\n]+")
        x = patt.findall(pkt)
        key = ""
        val1 = ""
        val2 = ""
        que = OrderedDict()
        for l in x:
            if "    " not in l and "        " not in l:
                key = l
                que[key] = ''
            if "    " in l and "        " not in l:
                val1 += l
                que[key] = val1
            if "    " not in l and "        " in l:
                val2 += l
                que[key][val1] = val2
        return que

    def contSniff(self,type='multipart/form-data', save=True):
        count = 0
        data = ""
        if save == True:
            self.f = open('pacFile.json', 'w')
        p = subprocess.Popen("tshark -V  -l -p  -S '::::END OF PACKET::::::' ", stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, shell=True)
        for line in iter(p.stdout.readline, '\n\r\n'):
            if ('::::END OF PACKET::::::' not in line):
                data += line
            else:
                packet = data
                data = ""
                pac = (self.parsePacket(packet))
                if save == True:
                    self.saveSniffs(type,pac)
            if "malformed" in data:
                count += 1
        return

    def saveSniffs(self,type,packet):
        found = False
        for k,v in packet.items():
            if type in v:
                found = True
        if found == True:
                (json.dump(packet,fp= self.f))
