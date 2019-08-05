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

import signal
import time
import zmq
import os

from pprint import pprint

if "PUB_PREFIX" in os.environ:
    prefix=os.environ['PUB_PREFIX']
else:
    prefix=None

def print_and_pub(publisher, topic, body):
    global prefix

    if type(topic) is str:
        btopic = topic.encode('utf-8')
    else:
        btopic = topic
        topic = topic.decode('utf-8')

    if type(prefix) is str:
        bprefix = prefix.encode('utf-8')
    else:
        bprefix = prefix

        if prefix is not None:
            prefix = prefix.decode('utf-8')

    if type(body) is str:
        bbody = body.encode('utf-8')
    else:
        bbody = body
        body = body.decode('utf-8')

    if bprefix is not None:
        bbody = bprefix + bbody
        body = prefix + body

    publisher.send_multipart([btopic, bbody])
    print("[%s] %s" % (topic, body))
            

def main():
    """ main method """
    
    #time.sleep(3)

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

    # Setup control vars
    counter = 0
    msg_count = 0
    num_messages = 10

    num = 0

    try:
        
        while True:
            counter = num_messages

            # publisher.send_multipart([b'system', b'Preparing to publish...'])
            # print("[%s] %s" % ('system', 'Preparing to publish...'))
            print_and_pub(publisher, 'system', 'Preparing to publish...')
            
            #Sleep 3 seconds
            time.sleep(3.0)

            # publisher.send_multipart([b'system', b'Publishing messages'])
            #print("[%s] %s" % ('system', 'Publishing messages'))
            print_and_pub(publisher, 'system', 'Publishing messages')

            while counter > 0:

                # Use modules to alternate topic 
                if num % 2 == 0:
                    topic = 'data-1'
                else:
                    topic = 'data-2'
                    
                payload = 'Message number %s' % (num)

                print_and_pub(publisher, topic, payload)

                time.sleep(0.5)

                num += 1
                
                counter -= 1

            print_and_pub(publisher, 'system', 'Finished publishing messages')

    except KeyboardInterrupt:
        print("Stopping...")

    finally:

        # Close the publisher socket
        publisher.close()

        # Terminate the context
        context.term()
        
if __name__ == "__main__":
    main()
        
