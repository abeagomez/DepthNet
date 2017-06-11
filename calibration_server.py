import socket
import sys
import select
import struct
import random
import depth_net


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
    
		data = struct.unpack('i',data)
		print "receiving " + str(data[0])

		if data[0] != 0:
			continue
		break
	while 1:
		print "sending 0" 
		msg = struct.pack('i', 0)
		s.sendto(msg , addr)

		rlist, wlist, xlist = select.select([s],[],[],1.0)    

		if rlist == []:
			print "No llega nada"
			continue
		d = s.recvfrom(1024)
		data = d[0]
		addr = d[1]
		#try :
		data = struct.unpack_from('<ifff',data)
		#except:
		#	print "el unpack dio error"
		#	continue

		print "receiving " + str(data[0])
		if data[0] != 1:
			continue
		return data, addr

def receive_points(s, point_1, points_number):
	print "Se van a recibir los puntos"
	virtual_coordinates = [(point_1[0][1], point_1[0][2], point_1[0][3])]
	#get_interaction()
	real_coordinates = []
	addr = point_1[1]
	i = 2
	while i <= points_number:
		print 'sending confirmation'
		msg = struct.pack('i',1)
		s.sendto(msg, addr)

		rlist, wlist, xlist = select.select([s],[],[],1.0)
		if rlist == []:
			continue 

		d = s.recvfrom(1024)
		data = d[0]
		addr = d[1]
		try :
			data = struct.unpack('<ifff',data)
		except:
			continue

		if data[0] == i:
			i += 1
			virtual_coordinates.append((data[1],data[2],data[3]))
			real_coordinates.append(get_world_coordinates())
			print virtual_coordinates[-1]
			#get interaction append to real_coordinates
	return depth_net.compute_matrix(real_coordinates, virtual_coordinates)

def get_world_coordinates(m, c):
	while True:
		frame = depth_net.get_video_frame()
		depth = get_depth_map()
		point = get_centroid(frame, depth)
		if point != (-1,-1,-1):
			return np.dot(np.arry(point), m) + c

def send_points(s, addr, m, c):
	while 1:
		point = get_world_coordinates(m, c)
		print point
		msg = struct.pack('ifff',3,point[0],point[1],point[2])
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
	s = create_socket(host, port)
	point_1 = establish_connection(s)
	m, c = receive_points(s, point_1, points_number)
	#fake_sending(s,point_1[1])
	fake_sending(s, point_1[1], m, c)



calibrate_system('', 9050, 3)