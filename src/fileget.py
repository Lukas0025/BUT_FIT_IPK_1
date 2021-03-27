# Project: IPK1
## 
# main script implemenation of FSP client with nsp support
# @autor Lukáš Plevač (xpleva07)

from nsp import client as nsp_client
from fsp import client as fsp_client
from urllib.parse import urlparse
from getopt import getopt
import sys
import os

# get params from CLI
opts, _ = getopt(sys.argv[1:], "n:f:")

nsp_host = None
path     = None

for opt, arg in opts:
    if opt in ['-f']:
        path = arg
    elif opt in ['-n']:
        nsp_host = arg

if path == None or nsp_host == None:
    print("need -f -n")
    exit(1)

# parse params

nsp_host = nsp_host.split(":")

if len(nsp_host) != 2:
    print("bad NSP address")
    exit(1)

nsp_host[1] = int(nsp_host[1])

parsed_uri = urlparse(path)

if '{uri.scheme}'.format(uri=parsed_uri) != "fsp":
    print("bad Protocol fsp is only supported")
    exit(1)

# init nsp client and get FSP addr
nsp      = nsp_client(tuple(nsp_host))
fsp_host = nsp.whereis('{uri.netloc}'.format(uri=parsed_uri))

# init FSP client
fsp = fsp_client(
    fsp_host,
    domain='{uri.netloc}'.format(uri=parsed_uri),
    agent='xpleva07'
)

if '{uri.path}'.format(uri=parsed_uri) == '/*':
    #download all
    files = fsp.get_index()
else:
    files = ['{uri.path}'.format(uri=parsed_uri)[1:]]

for file in files:
    if os.path.dirname(file) != '' and not os.path.exists(os.path.dirname(file)):
        os.makedirs(os.path.dirname(file))

    fsp.get(file, target=file)