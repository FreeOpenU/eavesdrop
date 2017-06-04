class CostumCommand(object):
    def create_sniff_command(self, interfaces):
        """Creates a sniff command using user Inut data from the TUI"""
        interface = str(interfaces + 1)
        tshark_command = "tshark -i  %s -V  -l -p -S '::::END OF PACKET::::::' " % interface
        return tshark_command
