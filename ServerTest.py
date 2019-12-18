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

class ServerTest(unittest.TestCase):
    def test_create_queue(self):
        r=requests.post("http://localhost:5001/create_queue", json={"qname":"A"})
        self.assertEqual(r.content[:-1], b'{"qname":"A"}')
        r=requests.post("http://localhost:5001/create_queue", json={"qname":"B"})
        self.assertEqual(r.content[:-1], b'{"qname":"B"}')
        r=requests.post("http://localhost:5001/get_queues", json={})
        self.assertEqual(r.content[:-1], b'{"A":[],"B":[]}')
    
    def test_delete_queue(self):
        requests.post("http://localhost:5001/create_queue", json={"qname":"A"})
        requests.post("http://localhost:5001/create_queue", json={"qname":"B"})
        r=requests.post("http://localhost:5001/delete_queue", json={"qname":"A"})
        self.assertEqual(r.content, b'deleted')
        r=requests.post("http://localhost:5001/get_queues", json={})
        self.assertEqual(r.content[:-1], b'{"B":[]}')

    def test_write_msg(self):
        requests.post("http://localhost:5001/create_queue", json={"qname":"A"})
        requests.post("http://localhost:5001/create_queue", json={"qname":"B"})

        r=requests.post("http://localhost:5001/write_message", json={"qname":"A","message":"A1"})
        self.assertEqual(r.content[:-1], b'{"message":"A1","qname":"A"}')

        r=requests.post("http://localhost:5001/write_message", json={"qname":"A","message":"A2"})
        self.assertEqual(r.content[:-1], b'{"message":"A2","qname":"A"}')

        r=requests.post("http://localhost:5001/get_queues", json={})
        self.assertEqual(r.content[:-1], b'{"A":["A1","A2"],"B":[]}')

        r=requests.post("http://localhost:5001/write_message", json={"qname":"B","message":"B1"})
        self.assertEqual(r.content[:-1], b'{"message":"B1","qname":"B"}')

        r=requests.post("http://localhost:5001/get_queues", json={})
        self.assertEqual(r.content[:-1], b'{"A":["A1","A2"],"B":["B1"]}')

    def test_read_msg(self):
        requests.post("http://localhost:5001/create_queue", json={"qname":"A"})
        requests.post("http://localhost:5001/write_message", json={"qname":"A","message":"A1"})
        requests.post("http://localhost:5001/write_message", json={"qname":"A","message":"A2"})
        
        r=requests.post("http://localhost:5001/read_message", json={"qname":"A"})
        self.assertEqual(r.content, b'A2')

        r=requests.post("http://localhost:5001/read_message", json={"qname":"A"})
        self.assertEqual(r.content, b'A1')

        r=requests.post("http://localhost:5001/get_queues", json={})
        self.assertEqual(r.content[:-1], b'{"A":[]}')

unittest.main()


