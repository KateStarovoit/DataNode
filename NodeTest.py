import unittest
from DataNode import *

n1 = DataNode(1)
class QueueTest(unittest.TestCase):
    def test_create(self):
        n1.create_queue("first") #just create some q
        n1.create_queue("sec")
        a = dict()
        a["first"] = []
        a["sec"] = []
        self.assertEqual(n1.queue_sectors,a)
        n1.queue_sectors.clear()

    def test_write(self):
        n1.create_queue("1")
        n1.create_queue("2") #create 2 queues

        n1.write_message("1","a") #add some msg
        n1.write_message("1","aa")
        n1.write_message("2","b")
        n1.write_message("2","bb")
        n1.write_message("3","?") #add to non existed key
        a = dict()
        a["1"] = ["a",'aa']
        a["2"] = ['b','bb']
        self.assertEqual(n1.queue_sectors,a)
        n1.create_queue("1") #is it rewrite our queue ?
        n1.create_queue("2")
        self.assertEqual(n1.queue_sectors,a)
        n1.queue_sectors.clear()

    def test_delete(self):
        n1.create_queue("1")
        n1.create_queue("2") #create 2 queues
        n1.delete_queue("1") #delete existed 
        a = dict()
        a["2"] = []
        self.assertEqual(n1.queue_sectors, a)
        n1.delete_queue("1") #delete unexisted
        n1.delete_queue("none") #delete unexisted
        self.assertEqual(n1.queue_sectors, a)
        n1.queue_sectors.clear()

    def test_read(self):
        answ=['aa','bb','a','b']
        n1.create_queue('1')
        n1.create_queue('2')
        n1.write_message('1','a')
        n1.write_message('1','aa')
        n1.write_message('2','b')
        n1.write_message('2','bb')
        current=[]
        current.append(n1.read_message('1'))
        current.append(n1.read_message('2'))
        current.append(n1.read_message('1'))
        current.append(n1.read_message('2'))
        self.assertEqual(answ,current)


