# -*- coding: utf-8 -*-
import re
import sys
from threading import Thread, Timer

import npyscreen

from Eavesdrop import Eavesdrop

contentType = ['multipart/form-data', 'text', 'video', 'audio', 'image', "ALL"]
willyouSave = ['YES', 'NO']
Eavesdrop = Eavesdrop()
deviceList = Eavesdrop.get_list
process_list = Eavesdrop.get_other_processes()

class EavesdropApp(npyscreen.NPSAppManaged):
    keypress_timeout_default = 5
    def onStart(self):
        self.resize()
        npyscreen.setTheme(npyscreen.Themes.ElegantTheme)
        self.addForm("MAIN", WelcomeScreen, name="Hello")
        self.addForm("MAINFORM", EavesdropForm, name="Sniffing Parameters")
        self.addForm('CONFIRMATION', EavesdropConfirmation, name='confirmation Screen')
        self.addForm('SNIFFER', ActivateEavesdrop, name='Sniffing Network')
        self.addForm("INPROGRESS", ManageEavesdrops, name="Manage Eavesdrop")


class WelcomeScreen(npyscreen.ActionFormWithMenus):
    def activate(self):
        self.edit()

    def create(self):
        self.say_hello = self.add(npyscreen.TitleFixedText, value="Welcome To Eavesdrop")
        self.m1 = self.new_menu(name="Main Menu", shortcut="^M")
        self.m1.addItemsFromList([("Create New Sniff ", ""),
                                  ("Manage Eavesdrops: ", self.manage_drops)])

    def on_ok(self):
        self.parentApp.switchForm("MAINFORM")

    def manage_drops(self):
        self.parentApp.switchForm("INPROGRESS")


class ManageEavesdrops(npyscreen.ActionForm):
    def create(self):
        self.inst = self.add(npyscreen.Textfield,
                             value="This is a list of Eavesdrops originating from %s: " % sys.path[0])
        self.processes = self.add(npyscreen.TitleSelectOne, name="Eavesdrops in Process: "
                                  , values=process_list)

    def on_ok(self):
        try:
            job = self.processes.value[0]
            pid = re.search(r"(\d+)(?=\s)", job)
            response = npyscreen.notify_confirm("World you like to view this process? "
                                                "(you may kill the process from the terminal window) ")
        except(IndexError):
            self.parentApp.switchForm("MAINFORM")
            # if response == True:
            #   subprocess.Popen("fg")

    def on_cancel(self):
        self.parentApp.switchForm("MAIN")
class EavesdropForm(npyscreen.ActionForm):
    if len(deviceList) <= 0:
        deviceList = ['No devices Available: Make sure tShark is downloaded']
    def activate(self):
        self.edit()
        self.parentApp.setNextForm('CONFIRMATION')

    def create(self):
        self.device = self.add(npyscreen.TitleMultiSelect, max_height=6, name='Capture Device', value=[0],
                               values=deviceList, scroll_exit=True)
        self.content_type = self.add(npyscreen.TitleSelectOne, max_height=6, name='Content Type',
                                     values=contentType, scroll_exit=True, value=[0])

        self.SavePacket = self.add(npyscreen.TitleSelectOne, max_height=6, value=[0], name='Save Packets?',
                                   values=willyouSave
                                   , scroll_exit=True)
        self.file_address = self.add(npyscreen.TitleFilename, name="Where do you want the text file: ")


    def on_ok(self):
        conf_form = self.parentApp.getForm('CONFIRMATION')
        conf_form.device.value = deviceList[self.device.value[0]]
        conf_form.content_type.value = contentType[self.content_type.value[0]]
        conf_form.willyousave.value = willyouSave[self.SavePacket.value[0]]
        conf_form.file_address.value = self.file_address.value
        self.parentApp.switchForm('CONFIRMATION')
    def on_cancel(self):
        self.parentApp.switchForm("MAIN")

class EavesdropConfirmation(npyscreen.ActionForm):
    def activate(self):
        self.edit()
        self.parentApp.setNextForm('SNIFFER')


    def create(self):
        self.confMessage = self.add(npyscreen.TitleFixedText, value=
        'Check Sniff Parameters. If it is correct, press the'
        ' OK button, if it is not, press the Cancel button to go mack to the main form!', editable=False)
        self.device = self.add(npyscreen.TitleFixedText, name='Selected Device: ', editable=False)
        self.content_type = self.add(npyscreen.TitleFixedText, name='Selected Content Type: ', editable=False)
        self.willyousave = self.add(npyscreen.TitleFixedText, name='Will you Save?', editable=False)
        self.file_address = self.add(npyscreen.TitleFixedText, name=
        "What would you like to name the text file: ", editable=False)



    def on_cancel(self):
        self.parentApp.switchForm("MAINFORM")
    def on_ok(self):
        sniffer = self.parentApp.getForm('SNIFFER')
        sniffer.captureDevice.value = self.device.value
        sniffer.content_type.value = self.content_type.value
        sniffer.SavePacket.value = self.willyousave.value
        sniffer.file_address.value = self.file_address.value
        self.parentApp.switchForm('SNIFFER')


class ActivateEavesdrop(npyscreen.ActionForm):

    def start_sniffing(self):
        dev = deviceList.index(self.captureDevice.value)
        desired_content_type = self.content_type.value
        save_packet = self.SavePacket.value
        filename = self.file_address.value
        dropped_eaves = Eavesdrop.continuous_sniff(content_type=desired_content_type,
                                                   save=save_packet, interface=dev, filename=filename)
        return dropped_eaves

    def create(self):
        self.packetCount = self.add(npyscreen.TitleFixedText, editable=False,
                                    value='not updating', name="Total Packets")
        self.malformed_packets = self.add(npyscreen.TitleFixedText, editable=False,
                                          value='not updating', name="Malformed Packets")
        self.showHost = self.add(npyscreen.TitleFixedText, editable=False, value='not updating',
                                 name="Glimpse of packet:")
        self.content_type = self.add(npyscreen.TitleFixedText, editable=False, hidden=True)
        self.captureDevice = self.add(npyscreen.TitleFixedText, editable=False, hidden=True)
        self.SavePacket = self.add(npyscreen.TitleFixedText, editable=False, hidden=True)
        self.incoming_packets = self.add(npyscreen.TitleFixedText, editable=False,
                                         name="Incoming Packets: ", value="Not Updating")
        self.packets_of_interest = self.add(npyscreen.TitleFixedText, editable=False,
                                            name="Packets of chosen type: ", value="Not Updating")
        self.filename = self.add(npyscreen.TitleFixedText, editable=False, hidden=True,
                                 name="What do you want to call your file name?")
        self.file_address = self.add(npyscreen.TitleFixedText, editable=False, hidden=True,
                                     name="Where do you want the json file: ")
        self.kill_sniff = self.add(npyscreen.ButtonPress, name="KILL SNIFF",
                                   when_pressed_function=self.kill_button)

    def afterEditing(self):
        t = Thread(target=self.start_sniffing)
        t.setDaemon(True)
        t.start()

    def while_waiting(self):
        Timer(1.0, self.update_count())

    def update_count(self):
        self.packetCount.value = str(Eavesdrop.pktCount)
        self.packetCount.update()
        self.showHost.value = str(Eavesdrop.host_name)
        self.showHost.update()
        self.malformed_packets.value = str(Eavesdrop.malcount)
        self.malformed_packets.update()
        self.incoming_packets.value = Eavesdrop.current_packet
        self.incoming_packets.update()
        self.packets_of_interest.value = Eavesdrop.packets_of_interest
        self.incoming_packets.update()

    def kill_button(self):
        result = npyscreen.notify_yes_no("Are you sure you want to KILL the sniff? ")
        if result == True:
            sys.exit(0)

    def on_cancel(self):
        self.parentApp.switchForm(None)
        self.editing = False
        sys.exit(0)

if __name__ == '__main__':
    npyscreen.wrapper(EavesdropApp().run())
