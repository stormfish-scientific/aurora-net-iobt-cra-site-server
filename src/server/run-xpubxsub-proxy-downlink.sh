#!/bin/bash

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

if [ "$1" = "cli" ]; then
    
    shift

    if [ $# -eq 0 ]; then

	docker run -ti --rm \
	       --name aurora-cra-local-proxy-downlink \
	       -v ${PWD}/:/usr/src/app/ \
	       --link aurora-cra-local-proxy-uplink \
	       --expose 9001 \
	       -p "9001:9001" \
	       aurora-net /bin/bash

    else

	docker run -ti --rm \
	       --name aurora-cra-local-proxy-downlink \
	       --link aurora-cra-local-proxy-uplink \
	       -v ${PWD}/:/usr/src/app/ \
	       --expose 9001 \
	       -p "9001:9001" \
	       aurora-net "$@"

    fi
    
else

    docker run -ti --rm \
	   --name aurora-cra-local-proxy-downlink \
	   --link aurora-cra-local-proxy-uplink \
	   -v ${PWD}/:/usr/src/app/ \
	   --expose 9001 \
	   -p "9001:9001" \
	   aurora-net python -u xpubxsub_proxy.py \
	   CONNECT XSUB tcp://10.1.27.150:9001 \
	   BIND XPUB tcp://0.0.0.0:9001
#	   aurora-net python -u server.py "$@"
#	   aurora-net python -u curve_server.py "$@"
#	   --extra_xsub_a_connect AURORA_CRA_LOCAL_PROXY_UPLINK_PORT \    
fi




