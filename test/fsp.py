import sys
sys.path.insert(0, '../src')
import fsp
import nsp

# resorve name
nsp_cl = nsp.client(("127.0.0.1", 3333))
server = nsp_cl.whereis("test.one")

print("connecting to {}\n".format(server))

# connect to server
fsp_cl = fsp.client(server, domain="test.one", agent="xpleva07")
fsp_cl.get("index", "index")
print(fsp_cl.get_index())
fsp_cl.close()