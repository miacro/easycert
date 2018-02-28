#!/usr/bin/env python
from easycert import CA

server_pathname = CA.Pathname(
    prefix="./CA", infix="inter", basename="test-server.com")
ca_pathname = CA.Pathname(prefix="./CA", infix="inter", basename="INTER_CA")
ca = CA([], dump_command=True)
ca.run_ocsp_server(server_pathname, ca_pathname)
