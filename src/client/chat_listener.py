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

import argparse
import signal
import time
import zmq
import os

import chat_service_pb2

from pprint import pprint

def main():
    """ main method """
    
    # Create a 0MQ Context
    context = zmq.Context()

    # Create a subscriber socket
    subscriber = context.socket(zmq.SUB)

    # Utilize environment variables provided by docker via --expose and --link
    # switches to figure out the URI sublisher port

    # sub_uri = 'tcp://10.1.27.150:9001'

    sub_uri = os.environ['AURORA_CRA_LOCAL_PROXY_DOWNLINK_PORT']

    # Connect using environment variable
    print('Connecting to: %s' % sub_uri)

    subscriber.connect(sub_uri)
    # Or we can specify uri manually
    # subscriber.connect("tcp://aurora-part2.1-sub:14701")

    # We'll use argparse to allow the user to specify topics of interest
    # on the command line
    parser = argparse.ArgumentParser('sub')
    # -t or --topic will be used to specify a topic.  It
    # can be used multiple times
    # thanks to the "append" action.
    parser.add_argument('sender_id')

    # Arg definitions are complete, so let's run the parser and
    # store the results in args
    args = parser.parse_args()

    # Setup default topics to use if none specified on command line
    default_topics = [b'chat']

    # If args.topic is None then no topics specified on command line
    topics = default_topics

    # Subscribe to each topic in the topics list
    for topic in topics:

        # Python 3 treats strings and byte arrays differently
        # We are using ZMQ calls which expect byte arrays, not
        # strings so we need to convert
        if type(topic) is str:
            topic = topic.encode('utf-8')

        # Perform the subscribe
        subscriber.setsockopt(zmq.SUBSCRIBE, topic)

        # Print a message telling the user we have subscribed...
        # don't forget to convert back to a str
        print('Subscribed to topic "%s"' % (topic.decode('utf-8')))

    try:

        print("Waiting for messages...")

        while True:

            message = subscriber.recv_multipart()

            chat_message = chat_service_pb2.ChatMessage()
            chat_message.ParseFromString(message[1])

            # if chat_message.sender_id != args.sender_id:
            print('[%s] %s' % (chat_message.sender_name,
                               chat_message.body))

    except KeyboardInterrupt:
        print("Stopping...")

    finally:

        # Close the subscriber socket
        subscriber.close()

        # Terminate the context
        context.term()


if __name__ == "__main__":
    main()
