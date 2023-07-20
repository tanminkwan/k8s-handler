import os

#Service Port
PORT = 5000

#DEBUG
DEBUG = os.getenv("DEBUG", 'True').lower() in ('true', '1', 't')

#
COMMAND_RECEIVER_ENABLED = False
MESSAGE_RECEIVER_ENABLED = False

import __main__
AGENT_NAME = os.environ.get('AGENT_NAME') or \
    os.path.basename(__main__.__file__).split('.')[0]

CUSTOM_APIS_PATH = "k8s_handler.api"

#Custom defined valuables
C_K8S_API_KEY = os.environ.get('K8S_API_KEY') 
if not C_K8S_API_KEY:
    try:
        C_K8S_API_KEY = open('/var/run/secrets/kubernetes.io/serviceaccount/token').read()
    except Exception as e:
        pass

C_K8S_API_KEY_PREFIX = os.environ.get('K8S_API_KEY_PREFIX') or 'Bearer'
C_K8S_HOST = os.environ.get('K8S_HOST') or 'https://kubernetes.default'
C_K8S_SSL_CA_CERT = os.environ.get('K8S_SSL_CA_CERT') or '/var/run/secrets/kubernetes.io/serviceaccount/ca.crt'
C_K8S_VERIFY_SSL = os.getenv('K8S_VERIFY_SSL', 'True').lower() in ('true', '1', 't')
