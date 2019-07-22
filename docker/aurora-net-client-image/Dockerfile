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

FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /pythonlib

COPY ./aurora_net /pythonlib/aurora_net

ENV PYTHONPATH=/pythonlib

#CMD [ "python", "-u", "./your-daemon-or-script.py" ]
CMD [ "/bin/bash" ]
