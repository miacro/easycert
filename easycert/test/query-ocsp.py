#!/usr/bin/env python
from easycert import CA

client_pathname = CA.Pathname(
    prefix="./CA", infix="inter", basename="test-client.com")
ca_pathname = CA.Pathname(prefix="./CA", infix="inter", basename="INTER_CA")
ca = CA([], dump_command=True)
ca.query_ocsp(client_pathname, ca_pathname)
