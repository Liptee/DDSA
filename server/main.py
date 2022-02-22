from threading import Thread
import socket
from PIL import Image
from PIL import Image, ImageFilter
from math import ceil
import os.path

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 5001))
server.listen(5)
users = []
print("Server is listening")

def processing_img(user_socket):
    print('PROCESSING IMAGE')
    sample = Image.open('server_image.jpg')
    noise = sample.filter(ImageFilter.FIND_EDGES)
    noise = noise.save("noise.jpg")
    send_back(user_socket)

def send_back(user_socket):
    print("Sendig image to user")
    file = open('noise.jpg', mode = "rb")
    print('Файл сервера прочитан')
    data = file.read(2048)
    while data:
        user_socket.send(data)
        data = file.read(2048)
    file.close

def listen_user(user_socket):
    print('Listening user')
    while True:
        data = user_socket.recv(2048)
        size = data.decode('utf-8')
        size = int(size)
        print(size)
        package = ceil(size/2048)+1
        print(package)
        file = open('server_image.jpg', mode = "wb")
        count = 1
        while True:
            data = user_socket.recv(2048)
            file.write(data)
            count+=1
            print(count)
            if count == package:
                break
        file.close()
        processing_img(user_socket)

def start_server():
    while True:
        user_socket, address = server.accept()
        print(f"User <{address[0]} connected>")
        users.append(user_socket)
        listen_acc_user = Thread(
            target=listen_user, 
            args=(user_socket,))
        listen_acc_user.start()

if __name__ == '__main__':
    start_server()
    
    