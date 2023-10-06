from miniagent.adapter import Adapter
from kubernetes import client, config
from kubernetes.client.rest import ApiException
import json

class K8SApiCaller(Adapter):

    def _datetime2str(self, o:dict) -> dict:
        return json.loads(json.dumps(o, default=str))

    def init_caller(self, 
                    config: config
                ) :
        
        self.batchv1api_client = client.BatchV1Api(client.ApiClient(config))
        self.corev1api_client = client.CoreV1Api(client.ApiClient(config))
        self.apisv1api_client = client.AppsV1Api(client.ApiClient(config))
        self.customapi_client = client.CustomObjectsApi(client.ApiClient(config))

    def get_all_external_services(self, param:dict) -> tuple[int, dict]:

        ret = self.corev1api_client.list_service_for_all_namespaces(watch=False)

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
        return 1, {"results":k8s_hosts}

    def get_service(self, param:dict) -> tuple[int, dict]:

        namespace = param['namespace']
        service_name = param['service_name']

        api_response = self.corev1api_client.read_namespaced_service(service_name, namespace)

        result = self._datetime2str(api_response.to_dict())
        return 1, {"result":result}

    def get_services(self, param:dict) -> tuple[int, dict]:

        namespace = param['namespace']

        api_response = self.corev1api_client.list_namespaced_service(namespace)

        results = self._datetime2str(api_response.to_dict())
        return 1, {"results":results}

    def create_service(self, param:dict) -> tuple[int, dict]:

        namespace = param['namespace']
        body = param['service']

        api_response = self.corev1api_client.create_namespaced_service(namespace, body)

        return 1, {"result":"OK"}

    def delete_service(self, param:dict) -> tuple[int, dict]:

        namespace = param['namespace']
        service_name = param['service_name']

        api_response = self.corev1api_client.delete_namespaced_service(service_name, namespace)

        return 1, {"result":"OK"}

    def get_deployment(self, param:dict) -> tuple[int, dict]:

        namespace = param['namespace']
        deployment_name = param['deployment_name']

        api_response = self.apisv1api_client.read_namespaced_deployment(deployment_name, namespace)

        result = self._datetime2str(api_response.to_dict())
        return 1, {"result":result}

    def create_deployment(self, param:dict) -> tuple[int, dict]:

        namespace = param['namespace']
        body = param['deployment']

        #try:
        #    api_response = self.apisv1api_client.create_namespaced_deployment(namespace, body)
        #except ApiException as e:
        #    pass
        api_response = self.apisv1api_client.create_namespaced_deployment(namespace, body)

        return 1, {"result":"OK"}

    def patch_deployment(self, param:dict) -> tuple[int, dict]:

        namespace   = param['namespace']
        deployment_name = param['deployment_name']
        body        = param['body']
        
        patched_deployment = self.apisv1api_client.patch_namespaced_deployment(
            namespace=namespace,
            name=deployment_name,
            body=body,
        )

        return 1, {"result":patched_deployment}

    def change_replicas(self, param:dict) -> tuple[int, dict]:

        namespace = param['namespace']
        deployment_name = param['deployment_name']
        replicas = param['replicas']
        
        target_object = self.apisv1api_client.read_namespaced_deployment(deployment_name, namespace)
        target_object.spec.replicas = replicas

        patched_deployment = self.apisv1api_client.patch_namespaced_deployment(
            namespace=namespace,
            name=deployment_name,
            body=target_object,
        )

        return 1, {"result":"OK"}
    
    def delete_deployment(self, param:dict) -> tuple[int, dict]:

        namespace = param['namespace']
        deployment_name = param['deployment_name']

        api_response = self.apisv1api_client.delete_namespaced_deployment(deployment_name, namespace)

        return 1, {"result":"OK"}

    def create_job(self, param:dict) -> tuple[int, dict]:

        namespace = param['namespace']
        body = param['job']

        api_response = self.batchv1api_client.create_namespaced_job(namespace, body)

        return 1, {"result":"OK"}
    
    def delete_job(self, param:dict) -> tuple[int, dict]:

        namespace = param['namespace']
        job_name = param['job_name']

        api_response = self.batchv1api_client.delete_namespaced_job(job_name, namespace)

        return 1, {"result":"OK"}

    def get_custom_object(self, param:dict) -> tuple[int, dict]:

        namespace   = param['namespace']
        object_name = param['object_name']
        group       = param['group']
        version     = param['version']
        plural      = param['plural']

        target_object = self.customapi_client.get_namespaced_custom_object(
            group=group, # networking.istio.io
            version=version, # v1alpha3
            namespace=namespace, # wta
            plural=plural, # virtualservices
            name=object_name # wta-external
        )

        return 1, {"result":target_object}

    def patch_custom_object(self, param:dict) -> tuple[int, dict]:

        namespace   = param['namespace']
        object_name = param['object_name']
        group       = param['group']
        version     = param['version']
        plural      = param['plural']
        body        = param['custom_object']
        
        patched_object = self.customapi_client.patch_namespaced_custom_object(
            group=group,
            version=version,
            namespace=namespace,
            plural=plural,
            name=object_name,
            body=body,
        )

        return 1, {"result":patched_object}

    """
    def patch_custom_object(self, param:dict) -> tuple[int, dict]:

        namespace   = param['namespace']
        object_name = param['object_name']
        group       = param['group']
        version     = param['version']
        plural      = param['plural']
        patch_function_name   = param['patch_function_name']
        patch_function_code   = param['patch_function_code']

        target_object = self.customapi_client.get_namespaced_custom_object(
            group=group,
            version=version,
            namespace=namespace,
            plural=plural,
            name=object_name
        )
        
        local_vars = {}
        exec(patch_function_code, local_vars)
        f = local_vars[patch_function_name]
        f(target_object)

        patched_object = self.customapi_client.patch_namespaced_custom_object(
            group=group,
            version=version,
            namespace=namespace,
            plural=plural,
            name=object_name,
            body=target_object
        )

        return 1, {"result":"OK"}
    """
    def get_status(self) -> int:
        return 1