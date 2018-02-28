#!/usr/bin/env python
from easycert import CA

pathname = CA.Pathname(prefix="./CA", infix="inter", basename="INTER_CA")
root_pathname = CA.Pathname(prefix="./CA", infix="root_ca", basename="root_ca")
ca = CA([], dump_command=True)
ca.prepare_directory(pathname)
ca.genrsa(pathname.get_keyfile(), cipher=False)
ca.create_intermediate_certificate_signing_request(
    pathname)
ca.sign_intermediate_certificate(pathname, root_pathname)
ca.verify_intermediate_certificate(pathname, root_pathname)
ca.create_cachain([pathname, root_pathname])
