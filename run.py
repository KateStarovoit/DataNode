import flask
import json
import time
import threading
from datetime import datetime
import ser

process = threading.Thread(target=ser.run_Datanode,args=[5001,1])
process.start()

