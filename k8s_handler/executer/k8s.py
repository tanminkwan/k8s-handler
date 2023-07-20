from miniagent import configure, db
from miniagent.executer import ExecuterInterface
from ..adapter.k8s_adapter import K8SApiCaller

class K8SApi(ExecuterInterface):

    def execute_command(self, 
                            initial_param: dict, 
                            k8s: K8SApiCaller,
                        ) -> tuple[int, dict]:
        
        api = initial_param.get('api')
        api_client = k8s.api_client(
                    k8s_api_key        = configure.get('C_K8S_API_KEY'),
                    k8s_api_key_prefix = configure.get('C_K8S_API_KEY_PREFIX'),
                    k8s_host           = configure.get('C_K8S_HOST'),
                    k8s_ssl_ca_cert    = configure.get('C_K8S_SSL_CA_CERT'),
                    k8s_verify_ssl     = configure.get('C_K8S_VERIFY_SSL'),
                )
        
        method = getattr(k8s, api)

        return method(api_client)