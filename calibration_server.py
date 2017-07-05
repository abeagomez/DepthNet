import socket
import sys
import select
import struct
import random
import depth_net
import numpy as np
import cv2
from time import sleep

def create_socket(host, port):
    try :
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print 'Socket created'
    except socket.error, msg :
        print 'Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()
    try:
        s.bind((host, port))
    except socket.error , msg:
        print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()
    print 'Socket bind complete'
    return s

def establish_connection(s):
    while 1:
        # receive data from client (data, addr)
        d = s.recvfrom(1024)
        data = d[0]
        addr = d[1]

        data = struct.unpack('i',data[0:4])
        print "receiving " + str(data[0])

        if data[0] != 0:
            continue
        print "Start signal received"
        break
    while 1:
        print "sending 0"
        msg = struct.pack('i', 0)
        s.sendto(msg , addr)

        rlist, wlist, xlist = select.select([s],[],[],1.0)

        if rlist == []:
            continue
        d = s.recvfrom(1024)
        data = d[0]
        addr = d[1]

        identifier = struct.unpack('<i',data[0:4])[0]

        if identifier != 1:
            continue
        return addr



def receive_points(s, addr, points_number):
    virtual_coordinates = []
    #get_interaction()
    real_coordinates = []
    i = 0
    print "Se van a recibir los puntos"
    while i < points_number:

        rlist, wlist, xlist = select.select([s],[],[],1.0)
        if rlist == []:
            continue

        d = s.recvfrom(1024)
        data = d[0]
        addr = d[1]

        #Voy a leer los primeros 4 bytes para tener el identificador
        identifier = struct.unpack('<i',data[0:4])[0]
        print "el identificador recibido es " + str(identifier)

        if identifier == 2:
            print "Se termino el proceso de calibracion"
            break

        if identifier != 1:
            continue

        data = struct.unpack('<iifff',data)

        if data[1] != i:
            continue

        virtual_coordinates.append((data[2],data[3],data[4]))
        real_coordinates.append(get_world_coordinates())
        send_point_confirmation(i, addr, s)
        i += 1
    return depth_net.compute_matrix(real_coordinates, virtual_coordinates)

def send_point_confirmation(i, addr, s):
    while 1:
        print 'enviando confirmacion del punto' + str(i)
        msg = struct.pack('ii',1, i)
        s.sendto(msg, addr)

        rlist, wlist, xlist = select.select([s],[],[],1.0)
        if rlist == []:
            continue

        d = s.recvfrom(1024)
        data = d[0]
        addr = d[1]

        #Voy a leer los primeros 4 bytes para tener el identificador
        #y el punto que me estan mandando
        identifier = struct.unpack('<i',data[0:4])
        if identifier[0] == 2:
            break
        if identifier[0] == 1:
            point = struct.unpack('<ii',data[0:8])[1]
            print "punto " + str(point) + " recibido"
            if point == i+1:
                break

def get_world_coordinates():
    while True:
        frame = depth_net.get_video_frame()
        depth = depth_net.get_depth_map()
        print "obtuve el frame y la profundidad sin problemas"
        point = depth_net.get_centroid(frame, depth)

        #depth_net.show_scene(frame,depth,point)
        if point != (-1,-1,-1):
            print "El punto detectado fue " + str(point)
            return point

        #k = cv2.waitKey(10)
        #if k == 27:
        #    break

def get_interaction_virtual_coordinates(m, c):
    while True:
        frame = depth_net.get_video_frame()
        depth = depth_net.get_depth_map()
        point = depth_net.get_centroid(frame, depth)


        #depth_net.show_scene(frame,depth,point)

        if point != (-1,-1,-1):
            print "Coordenadas detectadas"
            print "point"
            return np.dot(np.array(point), m) + c

        k = cv2.waitKey(10)
        if k == 27:
            break

def send_points(s, addr, m, c):
    while 1:
        print addr
        point = get_interaction_virtual_coordinates(m, c)
        print point
        msg = struct.pack('ifff',3,point[0],point[1],point[2])
        print "before send to"
        s.sendto(msg,addr)

def fake_sending(s,addr):
    while 1:
        x = random.uniform(-0.5,0.5)
        y = random.uniform(-0.01,1.0)
        z = random.uniform(-0.3,0.3)
        msg = struct.pack('fff',x,y,z)
        print x,y,z
        s.sendto(msg, addr)

def calibrate_system(host, port, points_number):
    print "Hola mundo"
    s = create_socket(host, port)
    addr = establish_connection(s)
    m, c = receive_points(s, addr, points_number)
    #fake_sending(s,addr)
    print "Se van a comenzar a enviar los puntos en coordenadas de mundo"
    send_points(s, addr, m, c)



calibrate_system('', 9050, 10)
