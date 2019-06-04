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

import uuid
import signal
import time
import zmq
import os

import chat_service_pb2

from pprint import pprint

def print_and_pub(publisher, topic, body):

    if type(topic) is str:
        btopic = topic.encode('utf-8')
    else:
        btopic = topic
        topic = topic.decode('utf-8')

    if type(body) is str:
        bbody = body.encode('utf-8')
    else:
        bbody = body
        body = body.decode('utf-8')
        
    publisher.send_multipart([btopic, bbody])
    print("[%s] %s" % (topic, body))
            

def main():
    """ main method """
    
    #time.sleep(3)

    sender_id = str(uuid.uuid4())

    print('Chatting with listener id: %s')

    # Create a 0MQ Context
    context = zmq.Context()

    # Create a publisher socket
    publisher = context.socket(zmq.PUB)

    # print ("Connecting to: tcp://10.1.27.150:9000")
    # Connect
    # publisher.connect("tcp://10.1.27.150:9000")
    pub_url = os.environ['AURORA_CRA_LOCAL_PROXY_UPLINK_PORT']
    print ("Connecting to: %s" % pub_url)
    # Connect
    publisher.connect(pub_url)

    try:

        topic = b'chat'

        # Send a first welcome message.. 
        print_and_pub(publisher, topic, 'HELLO from %s' %
                      sender_id)
            
        time.sleep(.2)

        msg = chat_service_pb2.ChatMessage()
        msg.sender_id = sender_id
        msg.timestamp = time.time()

        msg.sender_name = ''

        while msg.sender_name.strip() == '':
            print('Please enter your name')
            msg.sender_name = input(': ')

        keep_running = True

        while keep_running:

            print('Enter message or Q to quit.')

            if msg.body == 'Q' or msg.body == 'q':
                keep_running = False
            else:
                msg.body = input(': ')

                publisher.send_multipart([
                    topic,
                    msg.SerializeToString()])

        print_and_pub(publisher, 'system', 'Finished publishing messages')

    except KeyboardInterrupt:
        print("Caught interrupt")

    finally:
        print("Stopping...")
        # Close the publisher socket
        publisher.close()

        # Terminate the context
        context.term()


if __name__ == "__main__":
    main()
