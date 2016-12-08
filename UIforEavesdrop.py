import npyscreen
#from Eavesdrop import pysharkSniffer
import curses
class UIforSniffer(npyscreen.NPSAppManaged):
    def onStart(self):
        self.registerForm("MAIN", MainForm())

# This form class defines the display that will be presented to the user.

class MainForm(npyscreen.ActionForm):
    def create(self):
        F = npyscreen.Form(name= "Pyshark Sniffer")
        F.add(npyscreen.Textfield, name= "Sniffer Output Saved to Eavesdrop_Data.txt")
        F.add(npyscreen.TextfieldUnicode, value= " ")




if __name__ == '_main__':
    UIforSniffer().run()
