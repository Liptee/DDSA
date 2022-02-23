import socket
import os.path
from math import ceil

class Client(socket.socket):
    def __init__(self):
        super(Client, self).__init__(
            socket.AF_INET,
            socket.SOCK_STREAM)

        self.connect(("localhost", 5001))
        self.nick = input("Intoduce yourself: ")
    
    def send_img(self, filename):
        size = os.path.getsize(f"imgs_for_client\{filename}")
        packages = ceil(size/2048)
        self.send(f"{packages}".encode('utf-8'))
        file = open(f"imgs_for_client\{filename}", mode = 'rb')
        data = file.read(2048)
        count = 0
        while True:
            self.send(data)
            count+=1
            data = file.read(2048)
            if count == packages:
                break
        print(f'Sent {count} packages')
        file.close

    def get_img(self, filename):
        print("Listening user server")
        data = self.recv(2048)
        packages = data.decode('utf-8')
        print(f"Client will accept {packages} packages")
        packages = int(packages)
        file = open(f'imgs_for_client\{self.nick}_{filename}.jpg', mode = 'wb')
        count = 1
        print('Start download image')
        while count<=packages:
            data = self.recv(2048)
            file.write(data)
            count+=1
        file.close()
        print(f"Client received {count} packages")