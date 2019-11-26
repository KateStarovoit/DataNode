import flask
import json

class DataNode:
    def __init__(self, my_number):
        self.queue_sectors=dict()

    def create_queue(self,queue_name):
            self.queue_sectors[queue_name] = []

    def delete_queue(self, queue_name):
            del self.queue_sectors[queue_name]

    def write_message(self, queue_name, message):
            self.queue_sectors[queue_name].append(message)

    def read_message(self, queue_name):
            return self.queue_sectors[queue_name].pop()


Node = DataNode(1)

Server = flask.Flask(__name__)
@Server.route('/')
def init():
    return "Start"

@Server.route('/write_message/')
def write_message():
    content =json.loads(flask.request.json)
    Node.write_message(content["qname"], content["message"])
    return content

@Server.route('/read_message/')
def read_message():
    json.loads(flask.request.json)
    return  Node.read_message(content["qname"])

@Server.route('/create_queue/')
def create_queue():
    content = json.loads(flask.request.json)
    Node.create_queue(content["qname"])
    return content

@Server.route('/delete_queue/')
def delete_queue(q_name):
    content = json.loads(flask.request.json)
    Node.delete_queue_queue(content["qname"])
    return "deleted"

if __name__ == '__main__':
   # Server.run("localhost",2000)
    Server.run(host="192.168.43.40", port="2000")

