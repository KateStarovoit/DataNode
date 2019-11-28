import requests
import json
from flask import request


requests.post("http://localhost:5000/create_queue", json={"qname":"A"})


requests.post("http://localhost:5000/write_message", json={"qname":"A","message":"hello"})

test_data = {
    'create_queue': 'A',
}

r = requests.post("http://127.0.0.1:5000/read_message", json={"qname":"A"})
print(r.content)
