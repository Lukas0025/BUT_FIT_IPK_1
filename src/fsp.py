# Project: IPK1
## 
# basic FSP client class implementation
# @autor Lukáš Plevač (xpleva07)

import socket

class client:

    def __init__(self, server, timeout = 2, retry = 5):
        self.server = server
        self.retry = retry