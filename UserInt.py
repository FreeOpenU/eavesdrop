import npyscreen
from Eavesdrop import Eavesdrop

contentType = ['multipart/form-data','text','video','audio', 'image']


class EavesdropApp(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm("MAIN", EavesdropForm, name="Sniffing Parameters")


class EavesdropForm(npyscreen.ActionForm):
    def afterEditing(self):
        self.parentApp.setNextForm(None)
    def create(self):
        self.captureDevice = self.add(npyscreen.TitleSelectOne,max_height=20, name='Capture Device', values= Eavesdrop().getList(),scroll_exit=True)
        self.Contenttype = self.add(npyscreen.TitleSelectOne, max_height=20, name='Content Type',
                                      values=contentType, scroll_exit=True, default=[0])

        self.SavePacket = self.add(npyscreen.TitleSelectOne,max_height=10,name='Save Packets?',values=['Yes','No']
                                   ,scroll_exit = True)

    def on_ok(self):
        F = EavesdropForm(name="Eavesdrop")
        F.edit()
        dev = F.captureDevice.value
        type = F.Contenttype.value
        if F.SavePacket.value == 'No':
            saveFile = False
        else: saveFile = True
        Sniffoutput = Eavesdrop().contSniff(type=type,save=saveFile)
        return Sniffoutput

class seeOutput(npyscreen.BoxBasic):
    pass



if __name__ == '__main__':
    print(EavesdropApp().run())
