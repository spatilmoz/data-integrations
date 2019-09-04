import unittest

from integrations.connectors.Anaplan.anaplan_api_connector import AnaplanApiConnector


class TestAnaplanApiConnector(unittest.TestCase):
    def test_should_connect(self):
        # cert_format = "~/certs/{}"
        # cert_name = "anaplan.cer"
        cert_name = "cert.pem"
        anaplan_api_connector = AnaplanApiConnector(cert_name)
        anaplan_api_connector.connect_push()



if __name__ == '__main__':
    unittest.main()
