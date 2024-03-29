import flask
import json
import time
import threading
from datetime import datetime

class DataNode:
    def __init__(self, my_number):
        self.queue_sectors = dict()
        self.statistics = {
            'create_queue_duration': None,
            'delete_queue_duration': None,
            'write_message_duration': None,
            'read_message_duration': None,
            'datetime': (datetime.now()).strftime("%m/%d/%Y, %H:%M:%S")
            }

    def duration(func):
        def inner(self, *args, **kwargs):
            start_time = time.time()
            res = func(self, *args, **kwargs)
            duration = time.time() - start_time
            self.statistics[func.__name__+'_duration'] = duration
            return res
        return inner

    @duration
    def create_queue(self, queue_name):
        if queue_name not in self.queue_sectors:
            self.queue_sectors[queue_name] = []
            self.statistics['msg_num_in_'+queue_name] = 0

    @duration
    def delete_queue(self, queue_name): 
        try:
            del self.queue_sectors[queue_name]
            del self.statistics['msg_num_in_'+queue_name]
        except KeyError:
            'No such qname'

    @duration
    def write_message(self, queue_name, message):
        try:
            self.queue_sectors[queue_name].append(message)
            self.statistics['msg_num_in_'+queue_name] += 1
        except KeyError:
            'No such qname'

    @duration
    def read_message(self, queue_name):
        try:

            msg = self.queue_sectors[queue_name].pop()
            self.statistics['msg_num_in_'+queue_name] -= 1
        except KeyError:
            msg = 'No such qname'
        except IndexError:
            msg = 'Queue is empty'
        return msg


Node = DataNode(1)


Server = flask.Flask(__name__)
@Server.route('/')
def init():
    return "Start"

@Server.route('/write_message/', methods=["POST"])
def write_message():
    content = flask.request.json
    Node.write_message(content["qname"], content["message"])
    return content

@Server.route('/read_message/', methods=["POST"])
def read_message():
    content = flask.request.json
    return  Node.read_message(content["qname"])

@Server.route('/create_queue/', methods=["POST"])
def create_queue():
    content = flask.request.json
    Node.create_queue(content["qname"])
    return content

@Server.route('/delete_queue/', methods=["POST"])
def delete_queue():
    content = flask.request.json
    Node.delete_queue(content["qname"])
    return "deleted"

@Server.route('/get_statistics/', methods=["POST"])
def get_statistics():
    with open('statistics.json', 'r') as f:
        data = json.load(f)
    with open('statistics.json', 'w') as f:
        pass
    return data

def save_statistics():
    while True:
        time.sleep(60)
        now = datetime.now()
        Node.statistics['datetime'] = now.strftime("%m/%d/%Y, %H:%M:%S")
        with open('statistics.json', 'a') as f:
            json.dump(Node.statistics, f)


if __name__ == '__main__':
    t = threading.Thread(target=save_statistics)
    t.start()
    Server.run("localhost",2000)
   # Server.run(host="192.168.43.40", port="2000")

