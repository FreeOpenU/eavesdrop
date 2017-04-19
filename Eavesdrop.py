import json
import re
import subprocess

class Eavesdrop():
    #print device list
    def __init__(self):
        self.pktCount = 0
        self.malcount = 0
        self.host_count = 0
        self.f = open('pacFile.json', 'a')
        self.packet = ''

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
    # create T-shar sniff command
    def create_sniff_command(self,dev):
        tshark_command = ''
        #for i in dev:
        #    tshark_command += ' -i ' + str(dev)
        return tshark_command
    #Parse the packets into ordered dict
    def parsePacket(self,pkt):
        patt = re.compile("[^\n]+")
        x = patt.findall(pkt)
        key = ""
        val1 = ""
        val2 = ""
        que = {}
        for l in x:
            if "    " not in l and "        " not in l:
                key = l
                que[key] = ''
            elif "    " in l and "        " not in l:
                l = l.replace("    ", "")
                val1 += l
                que[key] = val1
            elif "    " not in l and "        " in l:
                l = l.replace("        ", "")
                val2 += l
                que[key][val1] = val2
        return que

    def contSniff(self, capture_type, deviceList=None, save=True):
        data = ""

        p = subprocess.Popen("tshark -V  -l -p  -S '::::END OF PACKET::::::' ", stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, shell=True)
        for line in iter(p.stdout.readline, ','):
            if ('::::END OF PACKET::::::' not in line):
                data += line
            else:
                self.packet = data
                print(self.packet)
                data = ""
                pac = (self.parsePacket(self.packet))
                self.pktCount += 1
                if save == True:
                    self.saveSniffs(capture_type, pac, save=True)
                else:
                    self.f.close()
            if "malformed" in data:
                self.malcount += 1
        return
    def saveSniffs(self,capture_type,packet,save):
        if save == True:
            found = False
            for k,v in packet.items():
                if capture_type in k:
                    found = True
            if found == True:
                json.dump(packet, fp=self.f)


e = Eavesdrop()
e.contSniff(capture_type="")
