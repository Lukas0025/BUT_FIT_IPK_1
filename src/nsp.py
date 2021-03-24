# Project: IPK1
## 
# basic NSP client class implementation
# @autor Lukáš Plevač (xpleva07)

import socket

class client:

    def __init__(self, server, timeout = 2, retry = 5):
        self.server = server
        self.sock = socket.socket(
            family=socket.AF_INET, # Internet
            type=socket.SOCK_DGRAM # UDP
        ) 

        self.sock.settimeout(timeout)
        self.retry = retry
    
    ##
    # Function ask NSP server for IP and Port of service ith name
    # @param name name to resolve
    # @return dict with (ip_addr, port)
    def whereis(self, name):
        self._send("WHEREIS {}".format(name))

        res = self._read()

        if "ERR Not Found" in res:
            raise Exception("NSP :: Not Found")
        elif "ERR Syntax" in res:
            raise Exception("NSP :: Bad Syntax")
        elif not(res.startswith("OK ")):
            raise Exception("NSP :: No OK repose")
        
        #remove ok_ from start
        res = res[3:].split(':')

        if (len(res) != 2):
            raise Exception("NSP :: Bad Syntax in return address")

        # ip, port
        return (res[0], res[1])

    ##
    # Function send string as ASCII to server
    # @param str_to_send string to send
    # @return None
    def _send(self, str_to_send):
        self.sock.sendto(bytes(str_to_send, "ascii"), self.server)

    ##
    # Function read repose string as ASCII from server and do same basic checks (timeout, reposefrom, max_length)
    # @return string from repose (ASCII decoded)
    def _read(self):
        for step in range(self.retry):
            try:
                res =  self.sock.recvfrom(1024)

                if (res[1] != self.server): # repose from another host may by fail connect
                    continue

                if (len(res[0]) > 1000): #message is too big
                    continue

                return res[0].decode('ascii')

            except socket.timeout as e:
                continue
        
        raise Exception("NSP :: timed out") 