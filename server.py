from http import server
import json
from multiprocessing import Process


class Handler(server.BaseHTTPRequestHandler):
    def do_POST(self):
        self.send_response(200)
        self.end_headers()
        body_length = int(self.headers['content-length'])
        request_body_json_string = self.rfile.read(body_length).decode('utf-8')

        print("request_body_json_string")
        # Printing  some info to the server console
        print('Server on port ' + str(self.server.server_port) + ' - request body: ' + request_body_json_string)

        datanode = DataNode()

        json_data_obj = json.loads(request_body_json_string)
        json_data_obj['SEEN_BY_THE_SERVER'] = 'Yes'

        # Sending data to the client
        self.wfile.write(bytes(json.dumps(json_data_obj), 'utf-8'))

class Handler(server.BaseHTTPRequestHandler):
    def do_POST(self):
        self.send_response(200)
        self.end_headers()
        body_length = int(self.headers['content-length'])
        request_body_json_string = self.rfile.read(body_length).decode('utf-8')

        print("request_body_json_string")
        # Printing  some info to the server console
        print('Server on port ' + str(self.server.server_port) + ' - request body: ' + request_body_json_string)

        json_data_obj = json.loads(request_body_json_string)
        json_data_obj['SEEN_BY_THE_SERVER'] = 'Yes'
        print(bytes(json.dumps(json_data_obj), 'utf-8'))

        # Sending data to the client

        self.wfile.write(bytes(json.dumps(json_data_obj), 'utf-8'))


class DataNode:
    def __init__(self, my_number):
        self.queue_sectors=dict({'A':[]})

    def create_queue(self,queue_name):
        self.queue_sectors[queue_name] = []

    def delete_queue(self, queue_name):
        del self.sectors_array[queue_name]

    def write_message(self, queue_name, message):
        self.sectors_array[queue_name].append(message)

    def read_message(self, queue_name):
        return self.queue_sectors[queue_name].pop()




def start_server(server_address):
    my_server = server.ThreadingHTTPServer(server_address, Handler)
    print(str(server_address) + ' Waiting for POST requests...')
    my_server.serve_forever()


def start_local_server_on_port(port):
    p = Process(target=start_server, args=(('127.0.0.1', port),))
    p.start()


if (__name__ == '__main__'):
    start_local_server_on_port(8011)
    start_local_server_on_port(8012)
