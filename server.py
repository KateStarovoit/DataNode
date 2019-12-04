import flask
import json
import time

class DataNode:
    def __init__(self, my_number):
        self.queue_sectors = dict()
        self.statistics = {
            'create_queue': 0,
            'delete_queue': 0,
            'write_message': 0,
            'read_message': 0}

    def duration(func):
        def inner(self, *args, **kwargs):
            start_time = time.time()
            res = func(self, *args, **kwargs)
            duration = time.time() - start_time
            print('Duration of method {} call is {}'.format(func.__name__, duration))
            return res
        return inner

    @duration
    def create_queue(self, queue_name):
        if queue_name not in self.queue_sectors:
            self.queue_sectors[queue_name] = []
        self.statistics['create_queue'] += 1

    @duration
    def delete_queue(self, queue_name): 
        self.statistics['delete_queue'] += 1
        try:
            del self.queue_sectors[queue_name]
        except KeyError:
            'No such qname'

    @duration
    def write_message(self, queue_name, message):
        self.statistics['write_message'] += 1
        try:
            self.queue_sectors[queue_name].append(message)
        except KeyError:
            'No such qname'

    @duration
    def read_message(self, queue_name):
        self.statistics['read_message'] += 1
        try:
            msg = self.queue_sectors[queue_name].pop()
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
def delete_queue(q_name):
    content = flask.request.json
    Node.delete_queue_queue(content["qname"])
    return "deleted"

@Server.route('/get_statistics/')
def get_statistics():
    return Node.statistics


if __name__ == '__main__':
    Server.run("localhost",2000)
   # Server.run(host="192.168.43.40", port="2000")
