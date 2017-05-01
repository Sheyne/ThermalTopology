import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 1238

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

with open("out.hex", "wb") as f:
	try:
		while True:
			data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
			f.write(data)
	except KeyboardInterrupt:
		print("saving")