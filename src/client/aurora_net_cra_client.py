# AURORA-Net IoBT CRA Site Server
# Copyright (C) 2019  Stormfish Scientific Corporation
#
# AURORA-Net IoBT CRA Site Server is free software: you can
# redistribute it and/or modify it under the terms of the GNU General
# Public License as published by the Free Software Foundation, either
# version 3 of the License, or (at your option) any later version.
#
# AURORA-Net IoBT CRA Site Server is distributed in the hope that it
# will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see
# <http://www.gnu.org/licenses/>.

# By: Stormfish Scientific Corporation
# Author: Theron T. Trout
# For: CCDC ARL - US Army Research Laboratory, Battlefield Information
# Processing Branch

import queue
import zmq
import threading
import signal
from pprint import pprint

class AuroraNetCraClient(object):

    def __init__(self, pub_url, sub_url):
        self.pub_url = pub_url
        self.sub_url = sub_url

        self.context = zmq.Context()

        self.pub_socket = self.context.socket(zmq.PUB)

        self.sub_socket = self.context.socket(zmq.SUB)

        self.pub_socket.connect(self.pub_url)

        self.sub_socket.connect(self.sub_url)

        self.recv_queue = queue.Queue()
        self.send_queue = queue.Queue()

        self.recv_worker = None
        self.send_worker = None

        self.keep_running = False

    def subscribe(self, topic):

        self.sub_socket.subscribe(topic)

    def unsubscribe(self, topic):
        self.sub_socket.unsubscribe(topic)

    def publish(self, topic, data):

        self.send_queue.put([topic, data])

    def recv_worker_thread_main(self):

        while self.keep_running:

            res = self.sub_socket.poll(timeout=250)

            if res != 0:
                frames = self.sub_socket.recv_multipart()

                self.recv_queue.put(frames)

    def send_worker_thread_main(self):

        while self.keep_running:

            try:
                frames = self.send_queue.get(timeout=.5)

                self.pub_socket.send_multipart(frames)

            except queue.Empty:
                # Send queue is empty
                pass

    def start(self):

        self.keep_running = True
        self.recv_worker = threading.Thread(
            target=self.recv_worker_thread_main)
        self.send_worker = threading.Thread(
            target=self.send_worker_thread_main)

        self.recv_worker.start()
        self.send_worker.start()

    def stop(self):
        self.keep_running = False

    def get(self, timeout=0):
        return self.recv_queue.get(timeout=timeout)


if __name__ == '__main__':

    # Create an instance of the client.
    # Publish to tcp://localhost:9101
    # Subcribe on tcp://localhost:9102
    cli = AuroraNetCraClient('tcp://localhost:9101',
                             'tcp://localhost:9102')

    cli.start()

    # cli.subscribe(b'data-1')
    cli.subscribe(b'')

    # Set a flag to control when app should quit.
    keep_running = True

    # Loop while keep_running is true.
    while keep_running:
        try:
            # Try to get a message from the receive queue.
            # Wait up to 0.2 seconds before 
            frames = cli.get(.2)

            # If the received message body ends in the number seven
            # ASCII code 55 decimal, publish a message to the 'system'
            # topic reporting that you found something.
            if frames[1][-1] == 55:
                cli.publish(b'system',
                            frames[1] + b' ends in 7!')

            # Print out the frames received.
            # pprint(frames)

        except queue.Empty:
            # Handle the condition when no cli.get() method
            # timed out without finding any messages.
            # You can do other work here.
            # Comment out the next line to have the app
            # stay quite when no data is available.
            print("no data")
            pass

        except KeyboardInterrupt:
            # Handle CTRL-C pressed by user.
            print('Stopping...')
            keep_running = False
            cli.stop()
