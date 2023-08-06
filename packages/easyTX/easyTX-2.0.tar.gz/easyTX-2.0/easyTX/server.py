import socket 
import cv2
import imutils
import base64
import easyTX.constants as constants

class Server():
    """Server class of easyTX module. Must be defined if the machine generates a continous stream of data and wants to send it.
    """
    def __init__(self, port):
        self.port = port
        
    def conn(self):
        """Connects with client
        """
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, constants.BUFF_SIZE)
        self.server_socket.settimeout(0.2)
        return self.server_socket
    
    def send_frame(self, source='0', width=400):
        """Sends frames.

        Args:
            source (str): address or path of the corresponding video. Defaults to 0.
            width (int, optional): Width of image. Defaults to 400.
        """
        if source == '0':
            source = int(source)
            
        vid = cv2.VideoCapture(source)
        while vid.isOpened():  
            _, frame = vid.read()
            if _:
                frame = imutils.resize(frame, width = width)
                encoded, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
                message = base64.b64encode(buffer)
                self.server_socket.sendto(message, ('localhost', self.port))
            else:
                vid.set(cv2.CAP_PROP_POS_FRAMES, 0)

    def send_data(self, message):
        """Sends data.

        Args:
            message (Any): Data that want to send.
        """
        message = base64.b64encode(message)
        self.server_socket.sendto(message, ('localhost', self.port))   
