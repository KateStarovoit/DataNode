import requests
import json
from flask import request


res = requests.post("http://localhost:2000/create_queue", json={"qname":"A"})


requests.post("http://localhost:2000/write_message", json={"qname":"A","message":"hello"})

#test_data = {
#    'create_queue': 'A',
#}

r = requests.post("http://127.0.0.1:2000/read_message", json={"qname":"A"})
print(r.content)
