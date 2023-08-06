from socket import create_connection
import ssl
import os
from websocket import create_connection
import json

class QlikEngine():
    def __init__(self,host,cert_path,user_directory,user_id):
        self.host = host
        self.cert_path = cert_path
        self.user_directory = user_directory
        self.user_id = user_id

        

    def createSocket(self):
        socketUrl = f"wss://{self.host}:4747/app/"
        cert = {
                "cert_reqs":ssl.CERT_NONE,
                'ca_certs': os.path.join(self.cert_path,'root.pem'),
                'certfile': os.path.join(self.cert_path,'client.pem'),
                'keyfile': os.path.join(self.cert_path,'client_key.pem')
        }

        requestHeader = {
                'X-Qlik-User':f'UserDirectory={self.user_directory};'
                              f'UserId={self.user_id}'
        }

        self.ws = create_connection(socketUrl, sslopt = cert, header = requestHeader)

        result = self.ws.recv()
        print(json.dumps(result))

        
    def __del__(self):
        self.ws.close()

    
