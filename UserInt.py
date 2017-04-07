import npyscreen
import curses
from Eavesdrop import Eavesdrop

contentType = ['multipart/form-data','text','video','audio', 'image']


class EavesdropApp(npyscreen.NPSAppManaged):
    def onStart(self):
        npyscreen.setTheme(npyscreen.Themes.ColorfulTheme)
        self.addForm("MAIN", EavesdropForm, name="Sniffing Parameters")


class EavesdropForm(npyscreen.Form):
    def afterEditing(self):
        self.parentApp.setNextForm(None)

    def create(self):
        self.captureDevice = self.add(npyscreen.TitleSelectOne,max_height=20, name='Capture Device', values= Eavesdrop().getList(),scroll_exit=True)
        self.Contenttype = self.add(npyscreen.TitleSelectOne, max_height=20, name='Content Type',
                                      values=contentType, scroll_exit=True, default=[0])

        self.SavePacket = self.add(npyscreen.TitleSelectOne,max_height=10,name='Save Packets?',values=['Yes','No']
                                   ,scroll_exit = True)
        self.SniffButton = self.add(npyscreen.ButtonPress,name='Start Sniff', when_pressed_function = self.start_Sniff)


    def start_Sniff(self):
        F = EavesdropForm(name="Eavesdrop")
        dev = F.captureDevice.value
        if F.SavePacket.value == 'No':
            saveFile = False
            type = None
        else:
            saveFile = True
            type = F.Contenttype.value
        Sniffoutput = Eavesdrop().contSniff(type=type,save=saveFile)
        return Sniffoutput

class seeOutput(npyscreen.BoxBasic):
    pass



if __name__ == '__main__':
    (EavesdropApp().run())
