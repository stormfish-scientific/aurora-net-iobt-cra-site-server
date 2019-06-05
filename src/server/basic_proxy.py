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
# Author: Theron T. Tout
# For: CCDC ARL - US Army Research Laboratory, Battlefield Information
# Processing Branch
# Date: 2019-01-03

import os
#import ipaddress
#import socket
import signal
#import time
import zmq
import zmq.auth
import logging
import uuid
from pprint import pprint

class BasicProxy(object):

    def __init__(self,
                 socket_in_config,
                 socket_out_config,
                 mirror_socket_config=None):

        self.node_uuid = uuid.uuid4()

        self.context = zmq.Context()

        self.keep_running = False

        self.socket_config = {}

        self.socket_config['in'] = socket_in_config
        self.socket_config['out'] = socket_out_config

        # pprint({'socket_config': self.socket_config})

        if mirror_socket_config is not None:
            self.socket_config['mirror'] = mirror_socket_config

        self.socket = {}

        for key in self.socket_config.keys():
            self.configure_socket(key)

    def configure_curve(self):
        self.base_dir = os.path.dirname(__file__)
        self.public_keys_dir = os.path.join(self.base_dir, 'public_keys')
        self.secret_keys_dir = os.path.join(self.base_dir, 'private_keys')

        self.server_public_file = os.path.join(
            self.public_keys_dir, "aurora-server.key"
        )

        self.server_key = zmq.auth.load_certificate(
            self.server_public_file
        )

        # We need two certificates, one for the client and one for
        # the server. The client must know the server's public key
        # to make a CURVE connection.
        self.client_secret_file = os.path.join(
            self.secret_keys_dir, "client.key_secret"
        )
        self.client_public, self.client_secret = zmq.auth.load_certificate(
            self.client_secret_file
        )

        print('CurveZMQ Configured.')

    def configure_socket(self, socket_key):
        # pprint({'socket_key': socket_key,
        #         'socket_config["key"]': self.socket_config[socket_key]
        #         })

        self.socket[socket_key] = self.context.socket(
            self.identify_socket_type(
                self.socket_config[socket_key]['type']
            )
        )

    def configure_socket_for_curvezmq(self, key):

        if 'use_curve' in self.socket_config[key]:
            if self.socket_config[key][
                    'use_curve'
            ].lower() == 'true':

                self.socket[key].curve_secretkey = (
                    self.client_secret
                )
                self.socket[key].curve_publickey = (
                    self.client_public
                )
                self.socket[key].curve_serverkey = (
                    self.server_key[0]
                )
                print(
                    'Socket %s configured to '
                    'use CurveZQM.' %
                    (
                        key
                    )
                )

            else:
                pprint({'use_curve here?': self.socket_config})
        else:
            print('Not using CurveZMQ on socket %s' %
                  key)
            pprint(self.socket_config)

    def prepare_sockets(self):

        for key in self.socket_config.keys():
            if self.socket_config[key]['mode'].upper() == 'BIND':
                print('Binding socket %s to %s' % (
                    key,
                    self.socket_config[key]['url']
                ))
                self.socket[key].bind(self.socket_config[key]['url'])

            elif self.socket_config[key]['mode'].upper() == 'CONNECT':

                if (
                    type(self.socket_config[key]['url']) is list or
                    type(self.socket_config[key]['url']) is tuple
                ):

                    for i in range(len(self.socket_config[key]['url'])):
                        url = self.socket_config[key]['url'][i]

                        # If :// not in url, treat it as an environment
                        # variable to load
                        if "://" not in url:
                            url = os.environ[url]

                        print('Connecting socket %s to %s' % (
                            key,
                            url
                        ))

                        self.configure_socket_for_curvezmq(key)

                        self.socket[key].connect(url)

                else:

                    url = self.socket_config[key]['url']

                    # If :// not in url, treat it as an environment
                    # variable to load
                    if "://" not in url:
                        print('Looking up environment variable %s.' % url)
                        url = os.environ[url]

                    print('Connecting socket %s to %s' % (
                        key,
                        url
                    ))

                    self.configure_socket_for_curvezmq(key)

                    self.socket[key].connect(url)

            else:
                raise Exception('Invalid mode of socket %s: %s' % (
                    url,
                    str(self.socket['in']['mode'].upper())
                ))

    def identify_socket_type(self, type_name):

        type_name = type_name.upper()

        if type_name == 'SUB':
            return zmq.SUB
        if type_name == 'XSUB':
            return zmq.XSUB
        if type_name == 'PUB':
            return zmq.PUB
        if type_name == 'XPUB':
            return zmq.XPUB
        if type_name == 'PUSH':
            return zmq.PUSH
        if type_name == 'PULL':
            return zmq.PULL

        raise Exception('Unknown socket type: %s' % type_name)

    def get_context(self):
        return self.context

    def get_node_uuid(self):
        return self.node_uuid

    def is_running(self):
        return self.keep_running

    def start(self):
        self.prepare_sockets()

        self.keep_running = True

        try:
            if 'mirror' in self.socket:
                zmq.proxy(self.socket['in'], self.socket['out'],
                          self.socket['mirror'])
            else:
                zmq.proxy(self.socket['in'], self.socket['out'])

        except KeyboardInterrupt:
            logging.info("Stopping...")
            self.keep_running = False
            self.socket['in'].close()
            self.socket['out'].close()

    def stop(self):
        self.keep_running = False

        if self.socket['in'] is not None:
            self.socket['in'].close()

        if self.socket['out'] is not None:
            self.socket['out'].close()
