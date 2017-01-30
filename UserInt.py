
import npyscreen
from Eavesdrop import eavesdrop
i=0
v = ""


captureDurationTypeDict =[' -c ',
                           ' -a files: ' ,
                           ' -a duration: ',
                          " -a filesize: ",
                          ""]
captureFieldsDict = {
0: ' -e _ws.col.Info ',
    1:' -e http ' ,
    2: ' -e frame.number ',
    3:" -e ip.addr ",
    4: ''

}

outputType = {
0: 'text',
1:'forms' ,
2: 'image',
3:" audio",
4: ''
}


class EavesdropForm(npyscreen.Form):
    def create(self):
        self.captureDurationType  = self.add(npyscreen.TitleSelectOne,max_height=6, name='Capture Type', values=['Capture By Packet Count',"Capture By File Size" ,'Capture By Time Limit', "Capture By Number of Files", 'none'],scroll_exit=True)
        self.duration = self.add(npyscreen.TitleText, name="Duration Value: ")
        self.fileName = self.add(npyscreen.TitleFilename, name="Filename:" )
        self.capFields = self.add(npyscreen.TitleMultiSelect, max_height=6, name='Tshark Fields', values=['Info Column', 'HTTP', 'frame Number', 'IP Address', 'none'], scroll_exit=True)
        self.capProm = self.add(npyscreen.TitleSelectOne, max_height=6, name='!WARNING! Promiscous Mode',values=['Promiscuous Mode', 'none'], scroll_exit=True)




contSniffer ='tshark  -p  -T pdml -b duration:10 -b files:30 -w 0000.pcap'

def convertToComand(type,dur,fields,filename,prom):
    v="tshark"
    if prom == [0]:
        v += ' -p'
    if fields != []:
        v += " -T fields "
        for items in fields:
            v += " " + (captureFieldsDict[items])
    if type != []:
        v = v + captureDurationTypeDict[type[0]] + dur
    if filename !=' ':
        v + " -w " + filename + ".pcap"


    return v


def myFunction(*args):
    F = EavesdropForm(name = "Eavesdrop")
    F.edit()
    t= F.captureDurationType.value
    promisc = F.capProm.value
    wantedOutputIndex = F.outputType.value
    val= F.duration.value
    fields = F.capFields.value
    name = F.fileName.value
    d = name
    command = convertToComand(t,val,fields,name, promisc)
    output = eavesdrop(contSniffer,d)
    return

if __name__ == '__main__':
    npyscreen.wrapper_basic(myFunction)