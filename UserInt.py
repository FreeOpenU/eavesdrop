import sys
from threading import Thread, Timer

import npyscreen

from Eavesdrop import Eavesdrop

contentType = ['multipart/form-data', 'text', 'video', 'audio', 'image', "ALL"]
willyouSave = ['YES', 'NO']
Eavesdrop = Eavesdrop()
deviceList = Eavesdrop.getList()



class EavesdropApp(npyscreen.NPSAppManaged):
    keypress_timeout_default = 5
    def onStart(self):
        npyscreen.setTheme(npyscreen.Themes.ElegantTheme)
        self.addForm("MAIN", EavesdropForm, name="Sniffing Parameters")
        self.addForm('CONFIRMATION',EavesdropConfirmation,name='confirmation Screen')
        self.addForm('SNIFFER',activateEavesdrop,name='Sniffing Network')



class EavesdropForm(npyscreen.ActionForm):

    if len(deviceList) <= 0:
        deviceList = ['No devices Available: Make sure tShark is downloaded']
    def activate(self):
        self.edit()
        self.parentApp.setNextForm('CONFIRMATION')

    def create(self):
        self.captureDevice = self.add(npyscreen.TitleSelectOne, max_height=6, name='Capture Device', value=[0],
                                      values=deviceList, scroll_exit=True)
        self.Contenttype = self.add(npyscreen.TitleSelectOne, max_height=6, name='Content Type',
                                    values=contentType, scroll_exit=True, value=[0])

        self.SavePacket = self.add(npyscreen.TitleSelectOne, max_height=6, value=[0], name='Save Packets?',
                                   values=willyouSave
                                   , scroll_exit=True)


    def on_ok(self):
        confirmForm = self.parentApp.getForm('CONFIRMATION')
        confirmForm.device.value = deviceList[self.captureDevice.value[0]]
        confirmForm.SniffType.value = contentType[self.Contenttype.value[0]]
        confirmForm.willyousave.value = willyouSave[self.SavePacket.value[0]]
        self.parentApp.switchForm('CONFIRMATION')
    def on_cancel(self):
        self.parentApp.switchForm(None)

class EavesdropConfirmation(npyscreen.ActionForm):
    def activate(self):
        self.edit()
        self.parentApp.setNextForm('SNIFFER')


    def create(self):
        self.confMessage = self.add(npyscreen.TitleFixedText, value='Check Sniff Parameters. If it is correct, press the'
                                                              'OK button, if it is not, press the Back button, if you'
                                                                    ' give up, press the Cancel button', editable=False)
        self.device = self.add(npyscreen.TitleFixedText, name='Selected Device: ', editable=False)
        self.SniffType = self.add(npyscreen.TitleFixedText, name='Selected Content Type: ', editable=False)
        self.willyousave = self.add(npyscreen.TitleFixedText, name='Will you Save?', editable=False)
        self.chooseFile = self.add(npyscreen.TitleFilenameCombo, name="Where do you want the json file: ")

    def on_back(self):
        self.parentApp.switchFormPrevious()

    def on_cancel(self):
        self.parentApp.switchForm(None)

    def on_ok(self):
        sniffer = self.parentApp.getForm('SNIFFER')
        sniffer.captureDevice.value = self.device.value
        sniffer.SniffType.value = self.SniffType.value
        sniffer.SavePacket.value = self.willyousave.value
        self.parentApp.switchForm('SNIFFER')



class activateEavesdrop(npyscreen.ActionForm):
    def start_Sniff(self):
        dev = deviceList.index(self.captureDevice.value)
        packetType = self.SniffType.value
        save_packet = self.SavePacket.value
        Sniffoutput = Eavesdrop.contSniff(capture_type=packetType,
                                          save=save_packet, interface=dev)
        return Sniffoutput

    def create(self):
        self.editing = False
        self.packetCount = self.add(npyscreen.TitleFixedText, editable=False,
                                    value='not updating', name="Total Packets")
        self.showMalformed = self.add(npyscreen.TitleFixedText, editable=False,
                                      value='not updating', name="Malformed Packets")
        self.showHost = self.add(npyscreen.TitleFixedText, editable=False, value='not updating')

        self.SniffType = self.add(npyscreen.TitleFixedText, editable=False, hidden=True)
        self.captureDevice = self.add(npyscreen.TitleFixedText, editable=False, hidden=True)
        self.SavePacket = self.add(npyscreen.Textfield, editable=False, hidden=True)
        self.Packet = self.add(npyscreen.Textfield, editable=False, hidden=True,
                               value=self.SavePacket.value)

    def afterEditing(self):
        t = Thread(target=self.start_Sniff)
        t.start()

    def while_waiting(self):
        Timer(1.0, self.update_count())

    def update_count(self):
        self.packetCount.value = str(Eavesdrop.pktCount)
        self.packetCount.update()
        self.showHost.value = str(Eavesdrop.host_count)
        self.showHost.update()
        self.showMalformed.value = str(Eavesdrop.malcount)
        self.showMalformed.update()
        self.Packet.valut = str(Eavesdrop.current_frame)
        self.Packet.update()

    def on_cancel(self):
        self.parentApp.switchForm(None)
        sys.exit()


if __name__ == '__main__':
    npyscreen.wrapper(EavesdropApp().run())
