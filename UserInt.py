
import npyscreen
from Eavesdrop import eavesdrop
i=0
v = ""


captureDurationTypeDict =[' -c ',
                           ' -a files: ' ,
                           ' -a duration: ',
                          " -a filesize: "]
captureFieldsDict = {
0: ' -e _ws.col.Info ',
    1:' -e http ' ,
    2: ' -e frame.number ',
    3:" -e ip.addr ",

}


class EavesdropForm(npyscreen.Form):
    def create(self):
        self.captureDurationType  = self.add(npyscreen.TitleSelectOne,max_height=6, name='Capture Type', values=['Capture By Packet Count',"Capture By File Size" ,'Capture By Time Limit', "Capture By Number of Files"],scroll_exit=True)
        self.duration = self.add(npyscreen.TitleText, name="Duration Value: ")
        self.fileName = self.add(npyscreen.TitleFilename, name="Filename:" )
        self.capFields = self.add(npyscreen.TitleMultiSelect, max_height=6, name='Tshark Fields', values=['Info Column', 'HTTP', 'frame Number', 'IP Address'], scroll_exit=True)
        self.capProm= self.add(npyscreen.TitleSelectOne, max_height=6, name='!WARNIN! Promiscous Mode',values=['Promiscuous Mode'], scroll_exit=True)
        self.stats = self.add(npyscreen.TitleMultiSelect, max_height=6, name='Capture Statistics',
                                     values=['Conversations', 'http', 'DNS', 'Endpoints','Follow TCP/UDP'], scroll_exit=True)
def convertToComand(type,dur,fields,filename):
    v="tshark -T fields "
    for items in fields:
         v= v + (captureFieldsDict[items])
    v ="\"" + v + captureDurationTypeDict[type[0]] + dur + " -w " + filename + ".pcap" +"\""
    return v


def myFunction(*args):
    F = EavesdropForm(name = "Eavesdrop")
    F.edit()
    t= F.captureDurationType.value
    val= F.duration.value
    fields = F.capFields.value
    name = F.fileName.value
    d = name + ".pcap"
    stats =F.stats.value
    command = convertToComand(t,val,fields,name)
    output = eavesdrop(command,d)
    str(output)
    return output

if __name__ == '__main__':
    print (npyscreen.wrapper_basic(myFunction))