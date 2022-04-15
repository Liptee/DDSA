from PIL import Image, ImageFilter
from threading import Thread
import socket
import os.path
from math import ceil
from skimage.io import imread, imsave
import cv2

class Server(socket.socket):
    def __init__(self):
        super(Server, self).__init__(
            socket.AF_INET,
            socket.SOCK_STREAM)

        self.bind(("localhost",5001))
        self.listen(5)
        print("Server is listening now")
    
    def get_img(self, user_socket):
        print(f"Listening user {user_socket}")
        while True:
            data = user_socket.recv(2048)
            packages = data.decode('utf-8')
            print(f"Server will accept {packages} packages")
            packages = int(packages)
            file = open('imgs_for_server\original.jpg', mode = 'wb')
            count = 1
            print('Start download image')
            while count<=packages:
                data = user_socket.recv(2048)
                file.write(data)
                count+=1
                
            file.close()
            print(f"Server received {count} packages")
            self.processing_img(user_socket)

    def accepted_users(self):
        while True:
            user_socket, address = self.accept()
            print(f"User <{address[0]}> connected")
            listen_acc_user = Thread(
                target=self.get_img,
                args=(user_socket,)
            )
            listen_acc_user.start()
    
    def processing_img(self, user_socket):
            print("PROCESSING IMAGE")
            img = imread("imgs_for_server\original.jpg") 
            clear = cv2.medianBlur(img, 3)
            imsave('imgs_for_server\oise.jpg', clear)
            self.send_img(user_socket)

    def send_img(self, user_socket):
        size = os.path.getsize("imgs_for_server\oise.jpg")
        packages = ceil(size/2048)
        user_socket.send(f"{packages}".encode('utf-8'))
        file = open("imgs_for_server\oise.jpg", mode = 'rb')
        data = file.read(2048)
        count = 0
        while True:
            user_socket.send(data)
            count+=1
            data = file.read(2048)
            if count == packages:
                break
        print(f'Sent {count} packages')
        file.close()

    