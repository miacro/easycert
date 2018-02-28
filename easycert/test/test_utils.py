from easycert import Utils
import unittest, tempfile


class UtilsTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_read_config(self):
        content = "[DEFAULT]\n \
                   ServerAliveInterval = 45\n \
                   Compression = yes\n \
                   CompressionLevel = 9\n \
                   ForwardX11 = yes\n \
                   [bitbucket.org]\n \
                   User = hg\n \
                   [topsecret.server.com]\n \
                   Port = 50022\n \
                   ForwardX11 = no"
        config = Utils.read_config(content=content)
        self.assertEqual(config["DEFAULT"]["ServerAliveInterval"], '45')
        self.assertEqual(config["DEFAULT"]["Compression"], 'yes')
        self.assertEqual(config["DEFAULT"]["CompressionLevel"], '9')
        self.assertEqual(config["DEFAULT"]["ForwardX11"], 'yes')
        self.assertEqual(config["bitbucket.org"]["User"], 'hg')
        self.assertEqual(config["topsecret.server.com"]["Port"], '50022')
        self.assertEqual(config["topsecret.server.com"]["ForwardX11"], 'no')

        with tempfile.NamedTemporaryFile(mode="w+t") as temp_file:
            temp_file.write(content)
            temp_file.flush()
            config = Utils.read_config(filename=temp_file.name)
            self.assertEqual(config["DEFAULT"]["ServerAliveInterval"], '45')
            self.assertEqual(config["DEFAULT"]["Compression"], 'yes')
            self.assertEqual(config["DEFAULT"]["CompressionLevel"], '9')
            self.assertEqual(config["DEFAULT"]["ForwardX11"], 'yes')
            self.assertEqual(config["bitbucket.org"]["User"], 'hg')
            self.assertEqual(config["topsecret.server.com"]["Port"], '50022')
            self.assertEqual(config["topsecret.server.com"]["ForwardX11"], 'no')

        config2 = Utils.read_config(config=config)
        self.assertIs(config, config2)
