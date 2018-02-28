#!/usr/bin/env python
from easycert import CA

pathname = CA.Pathname(prefix="./CA", infix="root_ca", basename="root_ca")
ca = CA([], dump_command=True)
# openssl req -config openssl.cnf \
#      -key private/ca.key.pem \
#      -new -x509 -days 7300 -sha256 -extensions v3_ca \
#      -out certs/ca.cert.pem
ca.prepare_directory(pathname)
ca.genrsa(pathname.get_keyfile(), cipher="")
ca.create_root_certificate(pathname)
ca.verify_root_certificate(pathname)
