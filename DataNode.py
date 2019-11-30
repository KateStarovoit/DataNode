from test import *

class DataNode:
    def __init__(self, my_number):
        self.queue_sectors=dict()

    def create_queue(self,queue_name):
            if(not(queue_name in self.queue_sectors)):
                self.queue_sectors[queue_name] = []

    def delete_queue(self, queue_name):
            if(queue_name in self.queue_sectors):
                del self.queue_sectors[queue_name]

    def write_message(self, queue_name, message):
            if(queue_name in self.queue_sectors):
                self.queue_sectors[queue_name].append(message)

    def read_message(self, queue_name):
            if(len(self.queue_sectors[queue_name])>0):
                return self.queue_sectors[queue_name].pop()

if __name__=="__main__":
    unittest.main(exit=False)


