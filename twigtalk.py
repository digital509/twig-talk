import re
import serial
import requests
import time


class TwigController():

    def __init__(self,port):

        # Port used by Raspberry Pi
        # GPIO Uart pins /dev/ttyAMA0

        self.port = port
        self.controller = re.search("=(.*?);", self.send_command('hubid')).group(1)
        self.twigs = self.get_twigs()


    def send_command(self, command):

        try:
            # Create a command string from arg and append line end
            command_string = "{}\n".format(command).encode('utf-8')
            # Initialize serial port settings
            serialPort = serial.Serial(self.port, 115200, timeout = 4)
            # Reset serial IO buffers
            serialPort.reset_output_buffer()
            serialPort.reset_input_buffer()
            # Write the command to serial
            serialPort.write(command_string)
            # Read the bytes response from the Twig Controller and return as utf-8 string
            rx = serialPort.readline()
            serialPort.close()
            return rx.decode('utf-8')
        except:
            return "Sending Command Failed"


    def get_twigs(self):

        # Try to get the next connected Twig ID and push it to twig_list. 
        # While loop terminates if controller returns FFFFFFFF for none or stop after
        # 10 tries.
        try:
            twig_list = []
            nextID = "0"
            timeout = 0
            while str(nextID) != "FFFFFFFF" or timeout == 10:
                command_string = "nextID {}".format(nextID)
                twigID = self.get_id(command_string)
                if str(twigID) != "FFFFFFFF":
                    twig_list.append(twigID)
                nextID = twigID
                timeout = timeout + 1
            return twig_list
        except Exception as e:
            print(e)


    def get_id(self,itemID):

        try:
            controllerID = re.search("=(.*?);", self.send_command(itemID)).group(1)
            return controllerID
        except Exception as e:
            print(e)
            pass


    def twig_status(self, twig):

        twigid = twigstatus = valveMessage = ''
        battVoltage = twigRssi = 0
        twigValve0 = twigValve1 = twigValve2 = twigValve3 = 0
        twigValve0message = twigValve1message = twigValve2message = twigValve3message = ''
        command = "twig {}".format(twig)
        twig_details = self.send_command(command)
        details = twig_details.split(',')

        for detail in details:
            if "id=" in detail:
                twigid = re.sub('id=', '', detail)
            if "batt=" in detail:
                hexvoltage = re.sub('batt=', '', detail)
                battVoltage = int(hexvoltage, 16) / 10
            if "stat=" in detail:
                twigstatus = re.sub('stat=', '', detail)
            if "v0=" in detail:
                twigValve0 = re.sub('v0=', '', detail)
                twigValve0 = "{0:08b}".format(int(twigValve0))
                twigValve0message, twigValve0 = self.decode_valve_status(twigValve0)
            if "v1=" in detail:
                twigValve1 = re.sub('v1=', '', detail)
                twigValve1 = "{0:08b}".format(int(twigValve1))
                twigValve1message, twigValve1 = self.decode_valve_status(twigValve1)
            if "v2=" in detail:
                twigValve2 = re.sub('v2=', '', detail)
                twigValve2 = "{0:08b}".format(int(twigValve2))
                twigValve2message, twigValve2 = self.decode_valve_status(twigValve2)
            if "v3=" in detail:
                twigValve3 = re.sub('v3=', '', detail)
                twigValve3 = twigValve3.split(";", 1)[0]
                twigValve3 = "{0:08b}".format(int(twigValve3))
                twigValve3message, twigValve3 = self.decode_valve_status(twigValve3)
            if "rssi=" in detail:
                twigRssi = re.sub('rssi=', '', detail)
                twigRssi = int(twigRssi, 16)
        payload = {
            'id': twigid,
            'voltage': battVoltage, 
            'rssi': twigRssi,
            'status': twigstatus,
            'valve1_state': twigValve0,
            'valve1_message': twigValve0message,
            'valve2_state': twigValve1,
            'valve2_message': twigValve1message,
            'valve3_state': twigValve2,
            'valve3_message': twigValve2message,
            'valve4_state': twigValve3,
            'valve4_message': twigValve3message,
            }
        return payload


    def decode_valve_status(self, valvestring):
        #   00001000
        valvestate = 0
        message = 'Valve Closed - No Errors'
        errval = valvestring.find('1')
        if int(errval) == 7:
            message = 'Valve Open'
            valvestate = 1
        if int(errval) == 5:
            message = 'Open Circuit Detected'
        if int(errval) == 4:
            message = 'Short Circuit Detected'
        if int(errval) == 2:
            message = 'Solenoid Voltage Too Low'
        return message, valvestate


    def set_valve(self, valve, state):
        command = "valveset {} {}".format(valve, state)
        self.send_command(command)
