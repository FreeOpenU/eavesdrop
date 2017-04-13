import npyscreen
from Eavesdrop import Eavesdrop

contentType = ['multipart/form-data','text','video','audio', 'image']
willyouSave = ['Yes','No']
Eavesdrop = Eavesdrop()






class EavesdropApp(npyscreen.NPSAppManaged):
    captureDevice, Contenttype, SavePacket = None,None,None
    def onStart(self):
        npyscreen.setTheme(npyscreen.Themes.ColorfulTheme)
        self.addForm("MAIN", EavesdropForm, name="Sniffing Parameters")
        self.addForm('CONFIRMATION',EavesdropConfirmation,name='confirmation Screen')
        self.addForm('Sniffer',activateEavesdrop,name='Sniffing Network')



class EavesdropForm(npyscreen.ActionForm):
    deviceList = Eavesdrop.getList()
    def activate(self):
        self.edit()
        self.parentApp.setNextForm('CONFIRMATION')

    def create(self):
        self.captureDevice = self.add(npyscreen.TitleSelectOne,max_height=20, name='Capture Device', values= self.deviceList,scroll_exit=True)
        self.Contenttype = self.add(npyscreen.TitleSelectOne, max_height=20, name='Content Type',
                                      values=contentType, scroll_exit=True, default=[0])

        self.SavePacket = self.add(npyscreen.TitleSelectOne,max_height=10,name='Save Packets?',values=willyouSave
                                   ,scroll_exit = True)


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
        self.parentApp.setNextForm('Sniffer')


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
        confirmedParams = self.parentApp.getForm('Sniffer')
        confirmedParams.dev = self.device.value
        self.parentApp.captureDevice = self.device.value
        self.parentApp.switchForm('Sniffer')



class activateEavesdrop(npyscreen.ActionForm):
    def start_Sniff(self):
        F = self.parentApp.getForm('MAIN')
        dev = type(self.parentApp.captureDevice)#F.captureDevice.value
        if F.SavePacket.value == 'No':
            saveFile = False
            packettype = None
        else:
            saveFile = True
            capturetype = F.Contenttype.value
        #Sniffoutput = Eavesdrop.contSniff(deviceList=dev, capture_type='', save=saveFile)
        #print dev
        return dev

    def create(self):
        self.dev = self.add
        self.aldlk = self.add(npyscreen.TitleFixedText, value=self.dev)

    def on_cancel(self):
        self.parentApp.switchForm(None)

if __name__ == '__main__':
    myApp =  EavesdropApp().run()