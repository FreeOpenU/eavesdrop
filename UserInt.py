
import npyscreen
from Eavesdrop import Eavesdrop

contentType = ['multipart/form-data','text','video','audio', 'image']
class EavesdropForm(npyscreen.Form):
    def create(self):
        self.captureDevice = self.add(npyscreen.TitleSelectOne,max_height=20, name='Capture Device', values= Eavesdrop().getList(),scroll_exit=True)
        self.Contenttype = self.add(npyscreen.TitleSelectOne, max_height=20, name='Content Type',
                                      values=contentType, scroll_exit=True)


def myFunction(*args):
    F = EavesdropForm(name = "Eavesdrop")
    F.edit()
    dev = F.captureDevice.value
    type = F.Contenttype.value
    return dev, contentType[type]

if __name__ == '__main__':
    print npyscreen.wrapper_basic(myFunction)