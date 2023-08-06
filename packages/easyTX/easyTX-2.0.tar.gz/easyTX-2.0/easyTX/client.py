import cv2
import socket
import numpy as np
import base64
import easyTX.constants as constants

class Client():
    """Client class of easyTX module. Must be defined if the machine wants to recieve a continous stream of data.
    """
    def __init__(self, port):
        self.port = port
        
    def conn(self):
        """Connects with server
        """
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) 
        self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.client_socket.bind(("", self.port))

    def recv_frame(self):
        """Gets frame from server. 
        Run in loop.

        Returns:
            _numpy.ndarray_: Returns single frame.
        """
        packet, _ = self.client_socket.recvfrom(constants.BUFF_SIZE)
        data = base64.b64decode(packet, ' /')
        npdata = np.fromstring(data, dtype = np.uint8)
        frame = cv2.imdecode(npdata, 1)
        return frame

    def recv_data(self):
        """Recives data from the server.
            Runs in loop.

        Returns:
            str: Any String data
        """
        packet, _ = self.client_socket.recvfrom(constants.BUFF_SIZE)
        data = packet.decode('utf-8')
        return data
    