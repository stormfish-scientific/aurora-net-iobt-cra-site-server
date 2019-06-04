#!/usr/bin/python

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
# Date: 2019-03-27

import basic_proxy
import time
import os
import config
import signal
import uuid
import logging
import zmq
import cra_aurora_net_pb2

from pprint import pprint


def extract_config(conf, section, prefix):
    d = {}

    found_something = False

    if (prefix + 'mode') in conf[section]:
        d['mode'] = conf[section][prefix + 'mode']
        found_something = True

    if (prefix + 'type') in conf[section]:
        d['type'] = conf[section][prefix + 'type']
        found_something = True

    if (prefix + 'url') in conf[section]:
        d['url'] = conf[section][prefix + 'url']
        found_something = True

    if (prefix + 'use_curve') in conf[section]:
        d['use_curve'] = conf[section][prefix + 'use_curve']

    if not found_something:
        return None

    return d


# Extend basic proxy to allow us to manually handle messages.
class DownlinkProxy(basic_proxy.BasicProxy):

    def __init__(self,
                 socket_in_config,
                 socket_out_config,
                 mirror_socket_config=None):

        # Call parent constructor
        super(DownlinkProxy, self).__init__(socket_in_config,
                                            socket_out_config,
                                            mirror_socket_config)

        self.config = config.Config('aurora_local_server.conf')

        if (
                self.config.get('local_site_server', 'site_id') is None
                or
                self.config.get('local_site_server', 'site_id') == ''
        ):
            logging.warning('site_id not set in conig. ')

        if (
                self.config.get('local_site_server', 'site_name',
                                '[UNSPECIFIED]') == '[UNSPECIFIED]'
                or
                self.config.get('local_site_server', 'site_name',
                                '[UNSPECIFIED]') == ''
        ):

            self.config.set('local_site_server', 'site_name', '[UNSPECIFIED]')
            self.config.save()

            raise Exception('site_name not set in [local_site_server] '
                            'config file.')

        if (
                self.config.get('local_site_server', 'site_poc_email',
                                '[UNSPECIFIED]') == '[UNSPECIFIED]'
                or
                self.config.get('local_site_server', 'site_poc_email',
                                '[UNSPECIFIED]') == ''
        ):

            self.config.set('local_site_server', 'site_poc_email',
                            '[UNSPECIFIED]')
            self.config.save()

            raise Exception('site_name not set in [local_site_server] '
                            'config file.')

        self.site_id = self.config.get('local_site_server',
                                       'site_id')

        self.site_name = self.config.get('local_site_server',
                                         'site_name')

        self.site_poc_email = self.config.get('local_site_server',
                                              'site_poc_email')

        logging.info('Site Name: %s' % self.site_name)
        logging.info('Site ID  : %s' % self.site_id)
        logging.info('POC Email: %s' % self.site_poc_email)

    def start(self):
        self.prepare_sockets()

        self.keep_running = True

        if 'mirror' in self.socket:
            self.run_with_mirroring()
        else:
            self.run_without_mirroring()

    def run_with_mirroring(self):

        logging.debug('Starting run_with_mirroring')

        poller = zmq.Poller()

        # Optimize access
        s_in = self.socket['in']
        s_out = self.socket['out']
        s_mirror = self.socket['mirror']

        poller.register(s_in, zmq.POLLIN)
        poller.register(s_out, zmq.POLLIN)
        poller.register(self.socket['mirror'], zmq.POLLIN)

        while self.keep_running:
            try:

                events = poller.poll(1000)

                for s in events:
                    s_id = ''

                    if s[0] == s_in:
                        s_id = 'in'
                    elif s[0] == s_out:
                        s_id = 'out'
                    elif s[0] == self.socket['mirror']:
                        s_id = 'mirror'
                    else:
                        s_id = 'UNKNOWN'

                    frames = s[0].recv_multipart()

                    if s_id == 'out' or s_id == 'mirror':
                        s_in.send_multipart(frames)
                    elif s_id == 'in':

                        msg = cra_aurora_net_pb2.SiteBroadcast()

                        msg.ParseFromString(frames[1])

                        if msg.site_id != self.site_id:

                            s_out.send_multipart(msg.message_frames)
                            s_mirror.send_multipart(msg.message_frames)

            except KeyboardInterrupt:
                logging.info("Stopping...")
                self.keep_running = False
                self.socket['in'].close()
                self.socket['out'].close()
                self.socket['mirror'].close()

            except Exception as ex:
                self.keep_running = False
                logging.error("Exception: " + str(ex))
                # Throw up the stack
                raise ex

    def run_without_mirroring(self):
        logging.debug('Starting run_without_mirroring')

        poller = zmq.Poller()

        # Optimize access
        s_in = self.socket['in']
        s_out = self.socket['out']

        poller.register(s_in, zmq.POLLIN)
        poller.register(s_out, zmq.POLLIN)

        while self.keep_running:
            try:

                events = poller.poll(1000)

                for s in events:
                    s_id = ''

                    if s[0] == s_in:
                        s_id = 'in'
                    elif s[0] == s_out:
                        s_id = 'out'
                    elif s[0] == self.socket['mirror']:
                        s_id = 'mirror'
                    else:
                        s_id = 'UNKNOWN'

                    frames = s[0].recv_multipart()

                    if s_id == 'out':
                        s_in.send_multipart(frames)
                    elif s_id == 'in':
                        msg = cra_aurora_net_pb2.SiteBroadcast()

                        msg.ParseFromString(frames[1])

                        if msg.site_id != self.site_id:

                            s_out.send_multipart(msg.message_frames)

            except KeyboardInterrupt:
                logging.info("Stopping...")
                self.keep_running = False
                self.socket['in'].close()
                self.socket['out'].close()
                self.socket['mirror'].close()

            except Exception as ex:
                self.keep_running = False
                logging.error("Exception: " + str(ex))
                # Throw up the stack
                raise ex


if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG)

    conf = config.Config('aurora_local_server.conf')

    config_section = "cra_downlink"

    socket_in_config = extract_config(conf, config_section,
                                      'socket_in_')

    pprint(socket_in_config)

    socket_out_config = extract_config(conf, config_section,
                                       'socket_out_')

    pprint(socket_out_config)

    mirror_socket_config = extract_config(conf, config_section,
                                          'mirror_socket_')

    pprint(mirror_socket_config)

    # if 'XSUB_URL' in os.environ:
    #     socket_in_config['url'] = os.environ['XSUB_URL']

    # if 'XPUB_URL' in os.environ:
    #     socket_out_config['url'] = os.environ['XPUB_URL']

    # if 'MIRROR_URL' in os.environ:
    #     mirror_socket_config['url'] = os.environ['MIRROR_URL']

    # If url doesn't contain :// then we assume it is the name of an
    # environment variable containing the url to use
    # if '://' not in socket_in_config['url']:
    #     socket_in_config['url'] = os.environ[socket_in_config['url']]

    print('socket_in_url: %s' % socket_in_config['url'])
    print('socket_out_url: %s' % socket_out_config['url'])
    print('socket_mirror_url: %s' %
          mirror_socket_config['url'])

    try:
        # proxy = basic_proxy.BasicProxy(socket_in_config,
        #                                socket_out_config,
        #                                mirror_socket_config)
        proxy = DownlinkProxy(socket_in_config,
                              socket_out_config,
                              mirror_socket_config)

        proxy.configure_curve()

        proxy.start()

    except KeyboardInterrupt:
        print("Stopping...")
        proxy.socket_in.close()
        proxy.socket_out.close()
        # proxy.context.stop()

    proxy.start()
