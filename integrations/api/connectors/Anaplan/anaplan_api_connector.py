import base64

import requests
from OpenSSL import crypto

from integrations.api.connectors.abstract.connector_push_task import ConnectorPushTask


class AnaplanApiConnector(ConnectorPushTask):
    def __init__(self, cert_name: str, ):
        self.cert_format = "/certs/{}"
        self.cert_name = cert_name

    def connect_push(self, orchestrator_data=None):
        print("Pushing data...", str(orchestrator_data))
        connect_string = self.anaplan_cert_connect()
        return orchestrator_data

    def cert_connect_string(self):
        cert_file = self.cert_format.format(self.cert_name)
        # Convert cer file to PEM
        # cmd="openssl x509 -inform der -in "+cert_file+" -out cert.pem"
        # os.popen(cmd)
        # Use of the pem file
        with open(cert_file, "r") as my_cert_file:
            my_cert_text = my_cert_file.read()
        cert = crypto.load_certificate(crypto.FILETYPE_PEM, my_cert_text)
        subject = cert.get_subject()
        issued_to = subject.CN  # the Common Name field
        issuer = cert.get_issuer()
        issued_by = issuer.CN
        # return my_cert_text
        return issued_to, my_cert_text

    def anaplan_cert_connect(self):
        # return authentication_txt
        username, cert = self.cert_connect_string()
        encoded_auth = '{}:{}'.format(username, cert).encode('utf-8')
        cert_str = str(base64.b64encode(encoded_auth).decode('utf-8'))
        anaplan_cert_header = 'AnaplanCertificate %s' % cert_str
        headers = {'Authorization': anaplan_cert_header}
        url = "https://api.anaplan.com/1/3/workspaces/"
        r = requests.get(url, headers=headers)
        return r.text
