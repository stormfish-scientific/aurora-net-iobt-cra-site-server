# AURORA-Net IoBT CRA Site Server

By Stormfish Scientific Corporation
Copyright (C) 2019 Stormfish Scientific Corporation
https://www.stormfish.io

Version: 1.0.0-alpha
Date: 2019-June-04

## Origin

Developed under sub-contract to the US Combat Capabilities Development
Command Army Search Lab (CCDC-ARL), Battlefield Information Processing
Branch (BIPB).

The code has undergone Operational Security (OPSEC) Review by
CCDC US Army Research Laboratory and has been approved for public
release with unlimited  distribution.  The OPSEC Receipt is included in
this distribution as AURORA-NET CRA Server Form 1 Receipt.pdf.

## Distribution

AURORA-Net IoBT CRA Site Server is free software: you can redistribute
it and/or modify it under the terms of the GNU General Public License
as published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

AURORA-Net IoBT CRA Site Server is distributed in the hope that it
will be useful, but WITHOUT ANY WARRANTY; without even the implied
warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See
the GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

Use of this software is constitutes acceptance of the terms of the
license.  See LICENSE for details.

## Purpose:

Provides a local server that includes a subset of the capabilities
of the Accelerated User Reasoning: Operations, Research, Analysis™
Network (AURORA-Net™) to support Internet of Battlefield Things (IoBT)
Collaborative Research Alliance (CRA) activities and to inter-connect
CRA sites via a central server.

By default, traffic between local IoT nodes and the site server is
un-encrypted.  All traffic between the local site server and a central
server is encrypted using Elliptic Curve Cryptography and
public/private key pairs.

From a client system's perspective it is meant to act as a "vanilla"
ZeroMQ pub/sub server.  Inter-site message distribution and encryption/
decryption is transparent to the user.

##  How to Use:

### Requirements

 * docker - Developed and tested on Docker version 18.09.6
 * docker-compose - Developed and tested on docker-compose version 1.23.1

### 1) Build the Docker Image

$ cd ./docker
$ ./build.sh

### 2) Configure Server

$ cd ./src/server/

Edit aurora_local_server.conf as desired.

Provide an appropriate value for site_name and site_poc_email.  A value
for site_id will be a uuid.  If you don't supply one, one will be
generated and the config file updated on the first run.

local_server_xsub configures the server port to which local nodes may
connect and publish messages.  The default port is 9101/tcp.

local_server_xpub configures the server port which publishes all
messages received on the local xsub port as well as traffic from remote
sites.  The default port is 9102/tcp.

cra_uplink and cra_downlink provide connectivity to a central server
to provide inter-site communication.  If you are a IoBT CRA member
and wish to connect to partner CRA sites, please contact your CRA
coordinator.

#### 2.a) Generate Certificates

You will need the public key of the server and to have your public key
installed on the server before you will be able to connect.  To
generate your public/private key pair, do the following:

$ cd ./src/server
$ ./run-generate_certificates.sh

Make a copy of the file client.key in the ./src/server/public_keys
folder and name it something representative of your site.  Send a
copy of this file to the central CRA server administrator.

You will need a copy of the CRA server's public key in order to
establish a trust relationship with the central server.  Contact
the CRA server adminstrator to request this file.


### 3) Launch Server

cd ./src/server

$ docker-compose up -d

To check output for errors enter:

$ docker-compose logs -f

### 4) Testing

The ./src/client folder contains various test scripts which may be used
to test that the server is running and also as a starting point for
writing new scripts.

### 5) Usage

Once the server is running, connect and publish to tcp://<your-server-ip>:9101
using a ZeroMQ client API.  Connect and subscribe to topics of interest on
tcp://<your-server-ip>:9102.
