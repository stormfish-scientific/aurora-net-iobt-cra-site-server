#!/bin/bash

protoc --python_out=. intersite_management.proto
cp intersite_management_pb2.py ../client

protoc --python_out=. ucla_cellphone_telemetry.proto
cp ucla_cellphone_telemetry_pb2.py ../client

protoc --java_out=. ucla_cellphone_telemetry.proto
