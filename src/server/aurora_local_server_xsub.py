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
# Date: 2019-03-27

import basic_proxy
#import argparse
import os
import config
import signal

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

    if not found_something:
        return None
    
    return d

if __name__ == '__main__':

    conf = config.Config('aurora_local_server.conf')

    socket_in_config = extract_config(conf, 'local_server_xsub',
                                      'socket_in_')

    socket_out_config = extract_config(conf, 'local_server_xsub',
                                       'socket_out_')

    mirror_socket_config = extract_config(conf, 'local_server_xsub',
                                          'mirror_socket_')

    if 'XSUB_URL' in os.environ:
        socket_in_config['url'] = os.environ['XSUB_URL']

    if 'XPUB_URL' in os.environ:
        socket_out_config['url'] = os.environ['XPUB_URL']

    if 'MIRROR_URL' in os.environ:
        mirror_socket_config['url'] = os.environ['MIRROR_URL']

    # If url doesn't contain :// then we assume it is the name of an
    # environment variable containing the url to use
    if '://' not in socket_in_config['url']:
        socket_in_config['url'] = os.environ[socket_in_config['url']]

    if '://' not in socket_out_config['url']:
        socket_out_config['url'] = os.environ[socket_out_config['url']]

    if '://' not in mirror_socket_config['url']:
        mirror_socket_config['url'] = os.environ[mirror_socket_config['url']]

    try:
        proxy = basic_proxy.BasicProxy(socket_in_config,
                                       socket_out_config,
                                       mirror_socket_config)

    except KeyboardInterrupt:
        print("Stopping...")
        proxy.socket_in.close()
        proxy.socket_out.close()
        proxy.context.stop()

    proxy.start()
