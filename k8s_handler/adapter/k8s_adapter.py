from miniagent.adapter import Adapter
from kubernetes import client, config
import json

class K8SApiCaller(Adapter):

    def api_client(self, 
                    k8s_api_key:str,
                    k8s_api_key_prefix:str,
                    k8s_host:str,
                    k8s_ssl_ca_cert:str,
                    k8s_verify_ssl:bool,
                ) -> client.CoreV1Api:
        
        config = client.Configuration()

        config.api_key['authorization']        = k8s_api_key
        config.api_key_prefix['authorization'] = k8s_api_key_prefix
        config.host                            = k8s_host
        config.ssl_ca_cert                     = k8s_ssl_ca_cert
        config.verify_ssl                      = k8s_verify_ssl

        return client.CoreV1Api(client.ApiClient(config))

    def get_services(self, api_client:client.CoreV1Api) -> tuple[int, dict]:

        ret = api_client.list_service_for_all_namespaces(watch=False)

        k8s_hosts = []

        for item in ret.items:

            ingress = getattr(item.status.load_balancer, 'ingress')

            if ingress:
                ports = [ str(p.port) \
                            for p in item.spec.ports \
                            if not getattr(p, 'name') or \
                            p.name in ['http','https','http2']]
                ports_str = ','.join(ports)
                ip = ingress[0].ip
                k8s_host = dict(
                            service_name = item.metadata.name,
                            namespace = item.metadata.namespace,
                            external_ip = ip,
                            ports = ports_str
                            )
                k8s_hosts.append(k8s_host)
        """
        TEST Coe
        f = open('test_k8s_services.json')
  
        data = json.load(f)
  
        for item in data['items']:
            if item.get('status').get('loadBalancer').get('ingress'):
                print(item['metadata']['name'], item['metadata']['namespace'])
                ports = [ str(port['port']) \
                         for port in item['spec'].get('ports') \
                            if not port.get('name') or \
                                port.get('name') in ('http','https','http2') ]
                ports_str = ','.join(ports)
                ip = item.get('status').get('loadBalancer').get('ingress')[0]['ip']
                k8s_host = dict(
                            service_name = item['metadata']['name'],
                            namespace = item['metadata']['namespace'],
                            external_ip = ip,
                            ports = ports_str
                            )
                k8s_hosts.append(k8s_host)
        """
        
        status = 1
        result = {"k8s_services":k8s_hosts}

        return status, result
    
    def get_status(self) -> int:
        return 1