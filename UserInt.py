
import npyscreen
from Eavesdrop import Eavesdrop

contentType = ['multipart/form-data','text','video','audio', 'image']


class EavesdropApp(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm("MAIN", EavesdropForm, name="Sniffing Parameters")







class EavesdropForm(npyscreen.ActionFormV2):
    def afterEditing(self):
        self.parentApp.setNextForm(None)
    def create(self):
        self.captureDevice = self.add(npyscreen.TitleSelectOne,max_height=20, name='Capture Device', values= Eavesdrop().getList(),scroll_exit=True)
        self.Contenttype = self.add(npyscreen.TitleSelectOne, max_height=20, name='Content Type',
                                      values=contentType, scroll_exit=True)

    def on_ok(self):
        #npyscreen.notify_confirm("Starting Sniff:     ")
        F = EavesdropForm(name="Eavesdrop")
        F.edit()
        dev = F.captureDevice.value
        type = F.Contenttype.value
        Sniffoutput = Eavesdrop().contSniff()
        return Sniffoutput





if __name__ == '__main__':
    EavesdropApp().run()
