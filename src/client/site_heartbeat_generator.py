import os
import queue
import time

import aurora_net_cra_client as aurora_net
import intersite_management_pb2

from pprint import pprint


def decode_and_print_heartbeat(data):

    if data is None:
        print("No Data")
        return

    broadcast = intersite_management_pb2.IntersiteStatusBroadcast()

    broadcast.ParseFromString(data)

    pprint({"Decoded msg": broadcast})
    return


if __name__ == '__main__':

    # Create a new instance of the AURORA CLI using the
    # connection info provided via environment variables
    aurora_cli = aurora_net.AuroraNetCraClient(
            os.environ['AURORA_CRA_LOCAL_PROXY_UPLINK_PORT'],
            os.environ['AURORA_CRA_LOCAL_PROXY_DOWNLINK_PORT'])

    # Store topic for easy access
    intersite_mgmt_topic = b'global:intersite_management'

    # Subscribe to the main topic
    aurora_cli.subscribe(intersite_mgmt_topic)

    # Start the client threads
    aurora_cli.start()

    keep_running = True

    # Prepare the site id message
    site_id = intersite_management_pb2.SiteIdentifier()

    # Look for site UUID in environment variables
    site_id.site_uuid = os.environ['SITE_UUID']

    # Look for site name in environment variables
    site_id.site_name = os.environ['SITE_NAME']

    # Include organization name if provided
    if 'ORG_NAME' in os.environ:
        site_id.organization_name = os.environ['ORG_NAME']

    # Create counter to control heartbeat broadcast interval
    counter = 4

    while keep_running:

        counter += 1

        # When counter hits 5 emmit a heartbeat
        if counter > 5:
            # Prepare a broadcast message
            broadcast = intersite_management_pb2.IntersiteStatusBroadcast()

            # Merge in the site_id message we created earlier
            broadcast.site_id.MergeFrom(site_id)

            # Arbitrarily report the status as yellow
            broadcast.system_heartbeat.system_status_color_code = (
                intersite_management_pb2.StatusColorCodes.YELLOW
            )


            broadcast.system_heartbeat.system_instance.name = "A test system"
            broadcast.system_heartbeat.short_status_message = (
                "System is initializiing..."
            )

            # Reset counter
            counter = 0

            data = broadcast.SerializeToString()

            pprint({'to publish': data})

            aurora_cli.publish(intersite_mgmt_topic, data)

        try:
            # Try to get some data frames
            # Wait up to 1.0 seconds for some data to arrive
            frames = aurora_cli.get(1.0)

            # If we received some frames...
            if frames:
                # Print them
                #pprint(frames)
                decode_and_print_heartbeat(frames[1])

        except queue.Empty:
            # This exception is thrown when the queue wait for data
            # expires with nothing in the queue
            # Nothing to do... move along.

            print('Queue empty')

            pass

        except KeyboardInterrupt:
            # Handle CTRL-C pressed by user.
            print('Stopping...')
            keep_running = False
            aurora_cli.stop()

    print ("Done")
