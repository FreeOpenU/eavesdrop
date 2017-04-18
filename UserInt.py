import npyscreen

from Eavesdrop import Eavesdrop

contentType = ['multipart/form-data','text','video','audio', 'image']
willyouSave = ['Yes','No']
Eavesdrop = Eavesdrop()




class EavesdropApp(npyscreen.NPSAppManaged):
    def onStart(self):

        npyscreen.setTheme(npyscreen.Themes.ColorfulTheme)
        self.addForm("MAIN", EavesdropForm, name="Sniffing Parameters")
        self.addForm('CONFIRMATION',EavesdropConfirmation,name='confirmation Screen')
        self.addForm('SNIFFER',activateEavesdrop,name='Sniffing Network')



class EavesdropForm(npyscreen.ActionForm):
    deviceList = Eavesdrop.getList()
    if len(deviceList) <= 0:
        deviceList = ['No devices Available: Make sure tShark is downloaded']
    def activate(self):
        self.edit()
        self.parentApp.setNextForm('CONFIRMATION')

    def create(self):
        self.captureDevice = self.add(npyscreen.TitleSelectOne, max_height=6, name='Capture Device', value=[0],
                                      values=self.deviceList, scroll_exit=True)
        self.Contenttype = self.add(npyscreen.TitleSelectOne, max_height=6, name='Content Type',
                                    values=contentType, scroll_exit=True, value=[0])

        self.SavePacket = self.add(npyscreen.TitleSelectOne, max_height=6, value=[0], name='Save Packets?',
                                   values=willyouSave
                                   , scroll_exit = True)


    def on_ok(self):
        confirmForm = self.parentApp.getForm('CONFIRMATION')
        confirmForm.device.value = self.deviceList[self.captureDevice.value[0]]
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
        self.confMessage = self.add(npyscreen.TitleFixedText,value='Check Sniff Parameters. If it is correct, press the'
                                                              'OK button, if it is not, press the Back button, if you'
                                                              ' give up, press the Cancel button')
        self.device =      self.add(npyscreen.TitleFixedText,name='Selected Device: ')
        self.SniffType =   self.add(npyscreen.TitleFixedText,name='Selected Content Type: ')
        self.willyousave = self.add(npyscreen.TitleFixedText, name='Will you Save?')
        self.BackButton =  self.add(npyscreen.ButtonPress, name='Back',when_pressed_function = self.on_back)

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
        dev = self.captureDevice.value
        if self.SavePacket.value == 'Yes':
            saveFile = True
            packetType = ''
        else:
            saveFile = False
            packetType = self.SniffType.value
        if saveFile == True or saveFile == False:
            Sniffoutput = Eavesdrop.contSniff(deviceList=dev, capture_type=packetType, save=saveFile)
        else:
            Sniffoutput = 'Params not here'
        return Sniffoutput

    def create(self):
        self.showOutput = ''
        self.SniffType = self.add(npyscreen.Textfield)
        self.captureDevice = self.add(npyscreen.Textfield)
        self.SavePacket = self.add(npyscreen.Textfield)

    def while_editing(self):
        self.start_Sniff()




    def on_cancel(self):
        self.parentApp.switchForm(None)

if __name__ == '__main__':
   EavesdropApp().run()