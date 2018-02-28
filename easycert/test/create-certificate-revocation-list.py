#!/usr/bin/env python
from easycert import CA

client_pathname = CA.Pathname(
    prefix="./CA", infix="inter", basename="test-client.com")
ca_pathname = CA.Pathname(prefix="./CA", infix="inter", basename="INTER_CA")
ca = CA([], dump_command=True)
ca.create_certificate_revocation_list(ca_pathname)
ca.verify_certificate_revocation_list(ca_pathname)

ca.revoke_certificate(client_pathname, ca_pathname)
ca.create_certificate_revocation_list(ca_pathname)
ca.verify_certificate_revocation_list(ca_pathname)
