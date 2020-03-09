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
import random
import zmq
import ucla_cellphone_telemetry_pb2

from pprint import pprint, pformat


if "PUB_PREFIX" in os.environ:
    prefix=os.environ['PUB_PREFIX']
else:
    prefix=None


def print_and_pub(publisher, topic, telemetry):
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

    publisher.send_multipart([btopic, telemetry.SerializeToString()])
    # print("[%s] %s" % (topic, str(telemetry)))

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

    min_longitude=-118.4614053
    max_longitude=-118.4418287

    min_latitude=34.0631947
    max_latitude=34.078089

    longitude_delta = (max_longitude-min_longitude) / 100.0
    latitude_delta = (max_latitude-min_latitude) / 100.0

    latitude = (max_latitude + min_latitude) / 2.0
    longitude = (max_longitude + min_longitude) / 2.0

    try:
        
        while True:
            latitude = (
                latitude + (2.0 * random.random() - 1.0) * latitude_delta
            )

            longitude = (
                longitude + (2.0 * random.random() - 1.0) * longitude_delta
            )

            if latitude < min_latitude:
                latitude = min_latitude
            elif latitude > max_latitude:
                latitude = max_latitude

            if longitude < min_longitude:
                longitude = min_longitude
            elif longitude > max_longitude:
                longitude = max_longitude

            telemetry = ucla_cellphone_telemetry_pb2 \
                        .CellPhoneTelemetry()

            telemetry.timestamp = time.time()

            telemetry.device_id = 'android_271'

            telemetry.lat_lon_alt.latitude = latitude
            telemetry.lat_lon_alt.longitude = longitude

            print_and_pub(publisher, b'stormfish:phone-telemetry', telemetry)

            time.sleep(0.5)

            num += 1

    except KeyboardInterrupt:
        print("Stopping...")

    finally:

        # Close the publisher socket
        publisher.close()

        # Terminate the context
        context.term()


if __name__ == "__main__":
    main()
