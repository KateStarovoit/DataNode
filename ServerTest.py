import requests
import time
import threading
import server
import unittest
import os

process = threading.Thread(target=server.run_Datanode,args=[5001,1])
process.daemon=True
process.start()
time.sleep(1)
process = threading.Thread(target=server.run_Datanode,args=[5002,2])
process.daemon=True
process.start()
time.sleep(1)

class ServerTest(unittest.TestCase):
    def test_create_queue(self):
        r=requests.post("http://localhost:5001/create_queue", json={"qname":"A"})
        self.assertEqual(r.content[:-1], b'{"qname":"A"}')
        r=requests.post("http://localhost:5001/create_queue", json={"qname":"B"})
        self.assertEqual(r.content[:-1], b'{"qname":"B"}')
        r=requests.post("http://localhost:5001/get_queues", json={})
        self.assertEqual(r.content[:-1], b'{"A":[],"B":[]}')

unittest.main()


