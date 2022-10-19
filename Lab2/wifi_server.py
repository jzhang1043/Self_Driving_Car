import socket
import picar_4wd as fc
from picamera import PiCamera
import base64

HOST = "192.168.10.62" # IP address of your Raspberry PI
PORT = 65432          # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    try:
        while 1:
            client, clientInfo = s.accept()
            print("server recv from: ", clientInfo)
            data = client.recv(1024)      # receive 1024 Bytes of message in binary format
            if data != b"":
                print(data)

                if data == b"87\r\n":
                    fc.forward(30)
                    client.sendall(data) # Echo back to client
                elif data == b"83\r\n":
                    fc.backward(30)
                    client.sendall(data) # Echo back to client
                elif data == b"65\r\n":
                    fc.turn_left(30)
                    client.sendall(data) # Echo back to client
                elif data == b"68\r\n":
                    fc.turn_right(30)
                    client.sendall(data) # Echo back to client
                elif data == b"0\r\n":
                    fc.stop()
                    client.sendall(data) # Echo back to client
                elif data == b"20\r\n":
                    camera = PiCamera()
                    camera.capture('picture.jpg')
                    camera.close()
                    encoded_string = ""
                    with open("picture.jpg", "rb") as image_file:
                        encoded_string = base64.b64encode(image_file.read())    
                        client.sendall(encoded_string)                        
                elif data == b"50\r\n":
                    cpu_temp = str(fc.cpu_temperature())
                    client.sendall(bytes(cpu_temp,'utf-8'))
                elif data == b"100\r\n":
                    battery = str(fc.power_read())
                    client.sendall(bytes(battery,'utf-8'))
    except: 
        print("Closing socket")
        client.close()
        s.close()