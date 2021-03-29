# Project: IPK1
## 
# basic FSP client class implementation
# @autor Lukáš Plevač (xpleva07)

import socket

class client:
    def __init__(self, server, domain, agent, timeout=10):
        self.server  = server
        self.domain  = domain
        self.agent   = agent
        self.timeout = timeout

    ##
    # Create TCP connection with FSP server
    # @return none
    def connect(self):
        self.sock = socket.socket(
            family=socket.AF_INET,  # Internet
            type=socket.SOCK_STREAM # TCP
        )

        self.sock.settimeout(self.timeout)
        self.sock.connect(self.server)

    ##
    # Genrate FSP client command header
    # @return command string
    def _get_command(self, file):
        return "GET {} FSP/1.0\r\nHostname: {}\r\nAgent: {}\r\n\r\n".format(file, self.domain, self.agent)

    ##
    # get file from server and wite it to file
    # @param file - file path on server
    # @param target - file location to write file
    # @return none
    def get(self, file, target):
        self.connect()
        self.sock.sendall(self._get_command(file).encode())
        self._process_stream(target)
        self.close()

    ##
    # get index from server
    # return index as array
    def get_index(self):
        self.connect()
        self.sock.sendall(self._get_command("index").encode())
        index = self._process_stream_mem().split("\r\n")
        self.close()
        return index[:-1]

    ##
    # process stream from server and return it (thow memory)
    # @return decoded (ASCII) body as string
    def _process_stream_mem(self):
        header = ""

        while not "\r\n\r\n" in header:
            header += self.sock.recv(1).decode("ascii")

        header = self._decode_header(header)

        body = ""
        readed = 0
        while readed < header.body_len:
            buffer = self.sock.recv(1024)
            body += buffer.decode("ascii")
            readed += len(buffer)

        return body

    ##
    # Process stream from server and write body to file
    # @return None
    def _process_stream(self, file):
        header = ""

        while not "\r\n\r\n" in header:
            header += self.sock.recv(1).decode("ascii")

        header = self._decode_header(header)

        with open(file, 'wb') as a_writer:
            readed = 0
            while readed < header.body_len:
                buffer = self.sock.recv(1024)
                a_writer.write(buffer)
                readed += len(buffer)

    ##
    # Decode header from string
    # @return obj header (header_class instac)
    def _decode_header(self, str_header):
        header = _header_class()

        str_header = str_header.split("\r\n")

        if len(str_header) != 4:
            raise Exception("FSP :: Bad header from server")

        str_header[0] = str_header[0].split(" ")

        header.protocol = str_header[0][0].upper()

        if header.protocol != "FSP/1.0":
            raise Exception("FSP :: Unsuported protocol from server {}".format(header.protocol))

        header.status   = str_header[0][1].lower()

        if header.status != "success":
            raise Exception("FSP :: Server return status {}".format(header.status))

        header.body_len = int(str_header[1].lower().replace("length:", ""))

        return header
    
    ##
    # Close opend socket
    # @return None
    def close(self):
        self.sock.close()

##
# class for FSP header
class _header_class:
    def __init__(self):
        self.protocol = None
        self.status   = None
        self.body_len = None