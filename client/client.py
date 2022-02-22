import socket
import os.path

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 5001))

def start_client():
    nick = input ("Ваше имя: ")
    while True:
        filename = input("Введите название файла: ")
        size = os.path.getsize(filename)
        client.send(f"{size}".encode('utf-8'))
        file = open(filename, mode = "rb")
        print("Original image is opened")
        data = file.read(2048)
        print("1 package sent")
        count = 1
        while data:
            client.send(data)
            count+=1
            print(f"{count} package sent")
            data= file.read(2048)    
        file.close()
        print('Origin image is closed')
        file = open(f'{nick}_res_image.jpg', mode = "wb")
        print('res_image is created')
        data = client.recv(2048)
        while data:
            file.write(data)
            data = client.recv(2048)
        file.close()
        print('File closed')

if __name__ == '__main__':
    start_client()