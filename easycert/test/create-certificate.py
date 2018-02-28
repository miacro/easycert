#!/usr/bin/env python
from easycert import CA

server_pathname = CA.Pathname(
    prefix="./CA", infix="inter", basename="test-server.com")
client_pathname = CA.Pathname(
    prefix="./CA", infix="inter", basename="test-client.com")
ca_pathname = CA.Pathname(prefix="./CA", infix="inter", basename="INTER_CA")
ca = CA([], dump_command=True)
# openssl req -config openssl.cnf \
#      -key private/ca.key.pem \
#      -new -x509 -days 7300 -sha256 -extensions v3_ca \
#      -out certs/ca.cert.pem
ca.genrsa(server_pathname.get_keyfile(), cipher=False)
ca.create_certificate_signing_request(server_pathname, ca_pathname)
ca.sign_server_certificate(server_pathname, ca_pathname)
ca.verify_certificate(server_pathname, ca_pathname)
ca.genrsa(client_pathname.get_keyfile(), cipher=False)
ca.create_certificate_signing_request(client_pathname, ca_pathname)
ca.sign_client_certificate(client_pathname, ca_pathname)
ca.verify_certificate(client_pathname, ca_pathname)
