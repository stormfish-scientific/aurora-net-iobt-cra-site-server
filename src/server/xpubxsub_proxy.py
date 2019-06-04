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
import argparse
from pprint import pprint

if __name__ == '__main__':

    parser = argparse.ArgumentParser('xpubxsub_proxy.py')

    parser.add_argument('socket_a_mode', help='Mode of socket A, may be BIND or CONNECT.')
    parser.add_argument('socket_a_type', help='Type of socket A, may be: SUB, XSUB, PUB'
                        'PUB, XPUB, PUSH, PULL')
    parser.add_argument('socket_a_url', help='URL of socket A, e.g. tcp://0.0.0.0.9999.')
    
    parser.add_argument('socket_b_mode', help='Mode of socket B, may be BIND or CONNECT.')
    parser.add_argument('socket_b_type', help='Type of socket B, may be: SUB, XSUB, PUB'
                        'PUB, XPUB, PUSH, PULL')
    parser.add_argument('socket_b_url', help='URL of socket B, e.g. tcp://0.0.0.0.9999.')    

    parser.add_argument('--extra_xsub_a_connect', help='Also connect to url in environment'
                        'variable provided for socket A.')

    parser.add_argument('--extra_xsub_b_connect', help='Also connect to url in environment'
                        'variable provided for socket B.')

    args = parser.parse_args()

    pprint(args)

    proxy = basic_proxy.BasicProxy(args.socket_a_type,
                                   args.socket_a_mode,
                                   args.socket_a_url,
                                   args.socket_b_type,
                                   args.socket_b_mode,
                                   args.socket_b_url,
                                   args.extra_xsub_a_connect,
                                   args.extra_xsub_b_connect)


    proxy.start()
