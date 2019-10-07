#!/bin/bash

protoc --python_out=. intersite_management.proto
cp intersite_management_pb2.py ../client
