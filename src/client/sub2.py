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

import queue
import os

import aurora_net

from pprint import pprint


if __name__ == '__main__':

    # Create a client
    acli = aurora_net.AuroraNetCraClient(
        os.environ['AURORA_CRA_LOCAL_PROXY_UPLINK_PORT'],
        os.environ['AURORA_CRA_LOCAL_PROXY_DOWNLINK_PORT'])

    # Start send/receive threads
    acli.start()

    # Subscribe to everything
    acli.subscribe(b'')

    # Flag to keep running
    keep_running = True

    # A heartbeat counter
    counter = 0

    # While keep_running is true...
    while keep_running:

        # Increment counter
        counter += 1

        # When counter hits 5 emmit a heartbeat
        if counter > 5:
            acli.publish(b'heartbeat', b'some-app-id')

            # Reset counter
            counter = 0

        try:
            # Try to get some data frames
            # Wait up to 1.0 seconds for some data to arrive
            frames = acli.get(1.0)

            # If we received some frames...
            if frames:
                # Print them
                pprint(frames)

        except queue.Empty:
            # This exception is thrown when the queue wait for data
            # expires with nothing in the queue

            # print('No data')

            # Nothing to do... move along.
            pass

        except KeyboardInterrupt:
            # Handle CTRL-C pressed by user.
            print('Stopping...')
            keep_running = False
            acli.stop()

    print("Done")
