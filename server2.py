import flask
import json
import time
import threading
from datetime import datetime
import copy


class DataNode:
    def __init__(self, my_number):
        self.id = my_number
        self.queue_sectors = dict()
        self.statistics = {
            'my_number': my_number,
            'create_queue_duration': 0.0,
            'delete_queue_duration': 0.0,
            'write_message_duration': 0.0,
            'read_message_duration': 0.0
        }
        self.stats_dict = dict()

        now = datetime.now()
        self.stats_dict[now.strftime("%m/%d/%Y, %H:%M:%S")] = self.statistics

        f = open("statistics.json", 'r+')


        data = json.load(f)

        data['node{}'.format(self.id)] = self.statistics
        f.close()
        f = open("statistics.json", 'w')

        json.dump(data, f)
        f.close()



    def duration(func):
        def inner(self, *args, **kwargs):
            start_time = time.time()
            res = func(self, *args, **kwargs)
            duration = time.time() - start_time
            self.statistics[func.__name__ + '_duration'] = duration
            return res

        return inner

    @duration
    def create_queue(self, queue_name):
        if queue_name not in self.queue_sectors:
            self.queue_sectors[queue_name] = []
            self.statistics['msg_num_in_' + queue_name] = 0

    @duration
    def delete_queue(self, queue_name):
        try:
            del self.queue_sectors[queue_name]
            del self.statistics['msg_num_in_' + queue_name]
        except KeyError:
            'No such qname'

    @duration
    def write_message(self, queue_name, message):
        try:
            self.queue_sectors[queue_name].append(message)
            self.statistics['msg_num_in_' + queue_name] += 1
        except KeyError:
            'No such qname'

    @duration
    def read_message(self, queue_name):
        try:
            msg = self.queue_sectors[queue_name].pop()
            self.statistics['msg_num_in_' + queue_name] -= 1
        except KeyError:
            msg = 'No such qname'
        except IndexError:
            msg = 'Queue is empty'
        return msg


def run_Datanode(port, id):
    Node = DataNode(id)

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
        return Node.read_message(content["qname"])

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
        data = Node.stats_dict.copy()
        Node.stats_dict.clear()
        return data

    def save_statistics():
        while True:
            time.sleep(5)
            now = datetime.now()
            Node.stats_dict[now.strftime("%m/%d/%Y, %H:%M:%S")] = Node.statistics

            f = open("statistics.json", 'r+')

            data = json.load(f)

            data['node{}'.format(Node.id)] = Node.statistics
            f = open("statistics.json", 'w')

            json.dump(data, f)
            f.close()
            # print(Node.statistics)


    t = threading.Thread(target=save_statistics)
    # t.daemon = True
    t.start()
    Server.run("localhost", port)
