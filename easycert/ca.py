from .exception import CAError
import os
import tempfile


class Pathname():
    def __init__(self,
                 prefix="~/.CA",
                 infix="root",
                 basename="ROOT_CA"):
        self.dir_private = "private"
        self.dir_newcerts = "newcerts"
        self.dir_certs = "certs"
        self.dir_crl = "crl"
        self.dir_csr = "csr"
        self.prefix = Utils.abspath(prefix)
        self.infix = infix
        self.basename = basename

    def get_prefix(self, with_infix=False):
        if not with_infix:
            return self.prefix
        return os.path.join(self.prefix, self.infix)

    def get_pathname(self, subdir, postfix, absolute=True):
        pathname = os.path.join(subdir, self.basename + postfix)
        if not absolute:
            return pathname
        return os.path.join(self.get_prefix(with_infix=True), pathname)

    def get_keyfile(self, *args, **kwargs):
        return self.get_pathname(
            "private", ".key.pem", *args, **kwargs)

    def get_crlfile(self, *args, **kwargs):
        return self.get_pathname(
            "crl", ".crl.pem", *args, **kwargs)

    def get_csrfile(self, *args, **kwargs):
        return self.get_pathname(
            "csr", ".csr.pem", *args, **kwargs)

    def get_crtfile(self, *args, **kwargs):
        return self.get_pathname(
            "certs", ".crt.pem", *args, **kwargs)

    def get_cachainfile(self, *args, **kwargs):
        return self.get_pathname(
            "certs", ".cachain.crt.pem", *args, **kwargs)

    def get_indexfile(self, absolute=True):
        pathname = "index.txt"
        if not absolute:
            return pathname
        return os.path.join(self.get_prefix(with_infix=True), pathname)


class CA():
    Pathname = Pathname

    def __init__(self,
                 configfiles=[],
                 dump_command=False,
                 dump_config=False,
                 run_command=True):
        self.configfiles = []
        self._dump_command = dump_command
        self._dump_config = dump_config
        self._run_command = run_command
        self.configfiles.append(
            os.path.join(
                os.path.dirname(__file__),
                "config",
                "default.conf"))

    def get_config(self):
        config = None
        for item in self.configfiles:
            config = Utils.read_config(filename=item, config=config)
        return config

    def run_command(self, command):
        if self._dump_command:
            command_string = Utils.run_command(
                command, dump=True, run=False)
            print(command_string)
        return Utils.run_command(
            command, dump=self._dump_command, run=self._run_command)

    def set_pathname_to_config(self, pathname, config):
        config["CA_default"]["dir"] = pathname.get_prefix(with_infix=True)
        config["CA_default"]["private_key"] = pathname.get_keyfile()
        config["CA_default"]["certificate"] = pathname.get_crtfile()
        config["CA_default"]["crl"] = pathname.get_crlfile()
        return config

    def get_root_config(self, pathname):
        config = self.get_config()
        self.set_pathname_to_config(pathname, config)
        config["CA_default"]["policy"] = "policy_match"
        return config

    def get_intermediate_config(self, pathname):
        config = self.get_config()
        self.set_pathname_to_config(pathname, config)
        config["CA_default"]["policy"] = "policy_anything"
        return config

    def run_openssl_with_config_option(self, config, command):
        with tempfile.NamedTemporaryFile(mode="w+t") as temp_file:
            Utils.write_config(config=config, file=temp_file)
            temp_file.flush()
            command += ["-config", temp_file.name]
            self.run_command(command)

    def genrsa(self, filename, cipher="aes256", numbits=4096):
        command = ["openssl", "genrsa"]
        if cipher:
            command += ["-" + cipher]
        command += ["-out", filename,
                    str(numbits)]
        self.run_command(command)
        self.run_command(["chmod", "400", filename])

    def create_root_certificate(
            self, pathname, days=3650, md="sha256", extensions="v3_ca"):
        command = ["openssl", "req",
                   "-key", pathname.get_keyfile(),
                   "-new", "-x509",
                   "-days", str(days),
                   "-" + md,
                   "-out", pathname.get_crtfile()]
        if extensions:
            command += ["-extensions", extensions]
        self.run_openssl_with_config_option(
            self.get_root_config(pathname), command)
        self.run_command(["chmod", "444", pathname.get_crtfile()])

    def verify_root_certificate(self, pathname):
        self.run_command(["openssl", "x509",
                          "-noout", "-text",
                          "-in", pathname.get_crtfile()])

    def create_intermediate_certificate_signing_request(
            self, pathname):
        self.run_command(["bash", "-c", "echo 1000 > crlnumber"])
        command = ["openssl", "req",
                   "-new", "-sha256",
                   "-key", pathname.get_keyfile(),
                   "-out", pathname.get_csrfile()]
        self.run_openssl_with_config_option(
            self.get_intermediate_config(pathname), command)

    def sign_intermediate_certificate(
            self, pathname, root_pathname,
            days=365, md="sha256", extensions="v3_intermediate_ca"):
        command = ["openssl", "ca",
                   "-days", str(days),
                   "-md", md,
                   "-notext",
                   "-in", pathname.get_csrfile(),
                   "-out", pathname.get_crtfile()]
        if extensions:
            command += ["-extensions", extensions]
        self.run_openssl_with_config_option(
            self.get_root_config(root_pathname), command)
        self.run_command(["chmod", "444", pathname.get_crtfile()])

    def verify_intermediate_certificate(self, pathname, root_pathname):
        command = ["openssl", "x509",
                   "-noout",
                   "-text",
                   "-in", pathname.get_crtfile()]
        self.run_command(command)
        command = ["openssl", "verify",
                   "-CAfile", root_pathname.get_crtfile(),
                   pathname.get_crtfile()]
        self.run_command(command)

    def create_cachain(self, pathnames):
        content = ""
        for item in pathnames:
            with open(item.get_crtfile(), "rt") as crtfile:
                content += crtfile.read()
                content += "\n"
        cachainfilename = pathnames[0].get_cachainfile()
        with open(cachainfilename, "w+t") as cachainfile:
            cachainfile.write(content)
        self.run_command(["chmod", "444", cachainfilename])

    def create_certificate_signing_request(
            self, pathname, ca_pathname, md="sha256"):
        command = ["openssl", "req",
                   "-key", pathname.get_keyfile(),
                   "-out", pathname.get_csrfile(),
                   "-new"]
        if md:
            command += ["-" + md]
        self.run_openssl_with_config_option(
            self.get_intermediate_config(ca_pathname), command)

    def sign_server_certificate(
            self, pathname, ca_pathname, days=365, md="sha256"):
        command = ["openssl", "ca",
                   "-extensions", "server_cert",
                   "-days", str(days),
                   "-notext",
                   "-md", md,
                   "-in", pathname.get_csrfile(),
                   "-out", pathname.get_crtfile()]
        self.run_openssl_with_config_option(
            self.get_intermediate_config(ca_pathname), command)
        self.run_command(["chmod", "444", pathname.get_crtfile()])

    def sign_client_certificate(
            self, pathname, ca_pathname, days=365, md="sha256"):
        command = ["openssl", "ca",
                   "-extensions", "usr_cert",
                   "-days", str(days),
                   "-notext",
                   "-md", md,
                   "-in", pathname.get_csrfile(),
                   "-out", pathname.get_crtfile()]
        self.run_openssl_with_config_option(
            self.get_intermediate_config(ca_pathname), command)
        self.run_command(["chmod", "444", pathname.get_crtfile()])

    def verify_certificate(self, pathname, ca_pathname):
        command = ["openssl", "x509",
                   "-noout",
                   "-text",
                   "-in", pathname.get_crtfile()]
        self.run_command(command)
        command = ["openssl", "verify",
                   "-CAfile", ca_pathname.get_cachainfile(),
                   pathname.get_crtfile()]
        self.run_command(command)

    def create_certificate_revocation_list(self, pathname):
        command = ["openssl", "ca",
                   "-gencrl",
                   "-out", pathname.get_crlfile()]
        self.run_openssl_with_config_option(
            self.get_intermediate_config(pathname), command)

    def verify_certificate_revocation_list(self, pathname):
        command = ["openssl", "crl",
                   "-in", pathname.get_crlfile(),
                   "-noout", "-text"]
        self.run_command(command)

    def revoke_certificate(self, pathname, ca_pathname):
        command = ["openssl", "ca",
                   "-revoke", pathname.get_crtfile()]
        self.run_openssl_with_config_option(
            self.get_intermediate_config(ca_pathname), command)

    def run_ocsp_server(
            self, pathname, ca_pathname, port="127.0.0.1:2560",
            nrequest=None, md="sha256"):
        print(ca_pathname.get_indexfile())
        command = ["openssl", "ocsp",
                   "-port", port,
                   "-text", "-" + md,
                   "-index", ca_pathname.get_indexfile(),
                   "-CA", ca_pathname.get_cachainfile(),
                   "-rkey", pathname.get_keyfile(),
                   "-rsigner", pathname.get_crtfile()]
        if nrequest:
            command += ["-" + nrequest, str(nrequest)]
        self.run_command(command)

    def query_ocsp(
            self, pathname,
            ca_pathname,
            url="http://127.0.0.1:2560"):
        command = ["openssl", "ocsp",
                   "-CAfile", ca_pathname.get_cachainfile(),
                   "-url", url,
                   "-resp_text",
                   "-issuer", ca_pathname.get_crtfile(),
                   "-cert", pathname.get_crtfile()]
        self.run_command(command)

    def prepare_directory(self, pathname):
        prefix = pathname.get_prefix(with_infix=True)
        self.run_command(["mkdir", "-p", prefix])
        os.chdir(prefix)
        self.run_command(["mkdir", "-p",
                          pathname.dir_certs,
                          pathname.dir_crl,
                          pathname.dir_private,
                          pathname.dir_csr,
                          pathname.dir_newcerts])
        self.run_command(["chmod", "700", pathname.dir_private])
        self.run_command(["touch", "index.txt"])
        self.run_command(
            ["bash", "-c", "[[ -f serial ]] || echo 1000 > serial"])
