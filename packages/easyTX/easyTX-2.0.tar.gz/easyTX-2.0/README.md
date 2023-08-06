# easyTX 2.0 

- "easyTX" 2.0 is the ultimate module to exchange data in any form (video or string) from one PC to another.
- It works on the basis of udp broadcasting.
- The Server has the data that is continuously shared on the LAN.
- Any number of Clients can access the data from the Server.

Installation
============

```shell
pip install easyTX
```


The following convention is used here: 
* the server is transmitting data
* the client is receiving data

Usage
============

##### server.py 

	from easyTX import Server
	socket = Server(5000)
	socket.conn()
	socket.send_frame()

##### client.py

	from easyTX import Client
	import cv2
	socket = Client(5000)
	socket.conn()
	while True:
		frame = socket.recv_frame()
		cv2.imshow('frame', frame)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			print('Disconnecting..')
			break
