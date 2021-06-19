import socket
import struct
import time
import timeit
import random

TCP_IP = '127.0.0.1'
TCP_PORT = 8008

buffer_u16 = "H"
buffer_u8 = "b"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
time.sleep(.1)

def send_and_receive():
    message = 50
    data = random.randint(1, 128)
    buffer_type = buffer_u8+buffer_u16
    buffer = struct.pack('<'+buffer_type,*[message,data])

    s.send(buffer)
    #time.sleep(.1)
    data = s.recv(1024)
    #print('Received', repr(data)[50:])

def test_timing():
    time_val = timeit.timeit("send_and_receive()", "from __main__ import send_and_receive; import random", number=1000)
    print("Time: " + str(time_val) + " seconds")

s.close()