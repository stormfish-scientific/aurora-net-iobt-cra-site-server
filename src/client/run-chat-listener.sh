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
# Author: Theron T. Trout
# For: CCDC ARL - US Army Research Laboratory, Battlefield Information
# Processing Branch

if [ "$1" = "cli" ]; then
    
    shift

    if [ $# -eq 0 ]; then

	docker run -ti --rm \
	       -v ${PWD}:/usr/src/app \
	       --network host \
	       -e AURORA_CRA_LOCAL_PROXY_DOWNLINK_PORT=tcp://localhost:9102 \
	       aurora-net /bin/bash

    else

	docker run -ti --rm \
	       -v ${PWD}:/usr/src/app \
	       -v ${PWD}/sub.py:/usr/src/app/sub.py \
	       --network host \
	       -e AURORA_CRA_LOCAL_PROXY_DOWNLINK_PORT=tcp://localhost:9102 \
	       aurora-net "$@"

    fi
    
else

    # docker run -ti --rm \
    # 	   -v ${PWD}/sub.py:/usr/src/app/sub.py \
    # 	   -e AURORA_CRA_LOCAL_PROXY_DOWNLINK_PORT=tcp://10.1.27.150:9102 \
    # 	   aurora-net python -u sub.py "$@"
    
    docker run -ti --rm \
    	   -v ${PWD}:/usr/src/app \
	   --network host \
	   -e AURORA_CRA_LOCAL_PROXY_DOWNLINK_PORT=tcp://localhost:9102 \
    	   aurora-net python -u chat_listener.py "$@"
fi




