import copy
import multiprocessing
import zmq
import logging
import json

from backtest.util import *

class TestClient(object):
    
    def __init__(self,feed_address, sync_address):
        self.context = zmq.Context()
        self.logger = logging.getLogger()
        self.feed_address = feed_address
        self.sync_address = sync_address
        
    def run(self):
        self.logger.info("running the client")
        self.data_feed = self.context.socket(zmq.PULL)
        self.data_feed.connect(self.feed_address)
        
        #synchronize with feed
        sync_socket = self.context.socket(zmq.REQ)
        sync_socket.connect(self.sync_address)
        # send a synchronization request to the feed
        sync_socket.send('')
        # wait for synchronization reply from the feed
        sync_socket.recv()
        sync_socket.close()
        
        counter = 0
        prev_dt = None
        while True:
            counter += 1
            msg = self.data_feed.recv()
            event = json.loads(msg)
            if(prev_dt != None):
                assert(event['dt'] >= prev_dt)
            self.logger.info("received {n} messages".format(n=counter))
            