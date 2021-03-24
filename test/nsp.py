import sys
sys.path.insert(0, '../src')
import nsp

nsp_cl = nsp.client(("127.0.0.1", 3333))
print(nsp_cl.whereis("test.one"))