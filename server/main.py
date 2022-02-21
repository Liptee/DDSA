import socket
from PIL import Image
from PIL import Image, ImageFilter
from math import ceil

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 5001))
server.listen(5)
print("Server is listening")

user_socket, address = server.accept()

print(f"User {address} connected!")

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
    if count == package:
        break
file.close()

sample = Image.open('server_image.jpg')
noise = sample.filter(ImageFilter.FIND_EDGES)
noise = noise.save("noise.jpg")

file = open('noise.jpg', mode = "rb")
print('Файл сервера прочитан')
data = file.read(2048)
while data:
    user_socket.send(data)
    data = file.read(2048)
file.close
    
    