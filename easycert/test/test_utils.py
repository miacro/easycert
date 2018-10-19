from easycert import utils
import unittest
import os
import tempfile
import configparser


class UtilsTest(unittest.TestCase):
    def test_readconfig(self):
        testfile = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "files", "A.conf")
        config = utils.readconfig(filename=testfile)
        self.assertEqual(config["DEFAULT"]["ServerAliveInterval"], '45')
        self.assertEqual(config["DEFAULT"]["Compression"], 'yes')
        self.assertEqual(config["DEFAULT"]["CompressionLevel"], '9')
        self.assertEqual(config["DEFAULT"]["ForwardX11"], 'yes')
        self.assertEqual(config["bitbucket.org"]["User"], 'hg')
        self.assertEqual(config["topsecret.server.com"]["Port"], '50022')
        self.assertEqual(config["topsecret.server.com"]["ForwardX11"], 'no')

        with open(testfile, "rt") as stream:
            content = stream.read()
        config = utils.readconfig(content)
        self.assertEqual(config["DEFAULT"]["ServerAliveInterval"], '45')
        self.assertEqual(config["DEFAULT"]["Compression"], 'yes')
        self.assertEqual(config["DEFAULT"]["CompressionLevel"], '9')
        self.assertEqual(config["DEFAULT"]["ForwardX11"], 'yes')
        self.assertEqual(config["bitbucket.org"]["User"], 'hg')
        self.assertEqual(config["topsecret.server.com"]["Port"], '50022')
        self.assertEqual(config["topsecret.server.com"]["ForwardX11"], 'no')

    def test_dumpconfig(self):
        config = configparser.ConfigParser()
        config["a"] = {"a": 123, "b": "456"}
        with tempfile.NamedTemporaryFile(mode="w+t") as stream:
            utils.dumpconfig(config, stream)
            stream.flush()
            config2 = utils.readconfig(filename=stream.name)
            self.assertEqual(config2["a"]["a"], "123")
            self.assertEqual(config2["a"]["b"], "456")
