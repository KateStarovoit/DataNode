import flask
import json
import time
import threading
from datetime import datetime
import server2

process = threading.Thread(target=server2.run_Datanode,args=[5001,1])
process.start()
time.sleep(1)
process = threading.Thread(target=server2.run_Datanode,args=[5002,2])
process.start()
time.sleep(1)
process = threading.Thread(target=server2.run_Datanode,args=[5003,3])
process.start()
