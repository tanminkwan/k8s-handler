from kubernetes import client
from miniagent import configure, db
from miniagent.executer import ExecuterInterface
from ..adapter.k8s_adapter import K8SApiCaller

class K8SApi(ExecuterInterface):

    def execute_command(self, 
                            initial_param: dict, 
                            k8s: K8SApiCaller,
                        ) -> tuple[int, dict]:
        
        api = initial_param.get('api')

        config = client.Configuration()

        config.api_key['authorization']        = configure.get('C_K8S_API_KEY')
        config.api_key_prefix['authorization'] = configure.get('C_K8S_API_KEY_PREFIX')
        config.host                            = configure.get('C_K8S_HOST')
        config.ssl_ca_cert                     = configure.get('C_K8S_SSL_CA_CERT')
        config.verify_ssl                      = configure.get('C_K8S_VERIFY_SSL')

        k8s.init_caller(config)
        
        method = getattr(k8s, api)

        return method(initial_param)