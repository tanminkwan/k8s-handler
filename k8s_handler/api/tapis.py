from flask import request, make_response
from flask_restful import Resource, reqparse
from flask_api import status
from miniagent import api
from miniagent.executer import ExecuterCaller

def _call_n_return(param: dict) -> tuple[dict, int]:
    
    data = dict(
        initial_param = param,
        executer = 'k8s_handler.executer.k8s.K8SApi',
    )
            
    rtn, rtn_message = ExecuterCaller.instance().execute_command(data)
        
    if rtn:
        status_code = status.HTTP_200_OK            
    else:
        status_code = status.HTTP_404_NOT_FOUND

    return rtn_message, status_code

class Services(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('service', type=dict)

    def get(self, namespace):

        param = dict(
                api = 'get_services' ,
                namespace = namespace,
            )

        return _call_n_return(param)

    def post(self, namespace):

        args = Services.parser.parse_args()

        param = dict(
                api = 'create_service' ,
                namespace = namespace,
                service = args['service'],
            )

        return _call_n_return(param)

class Service(Resource):

    def get(self, namespace, service):

        param = dict(
                api = 'get_service' ,
                namespace = namespace,
                service_name = service,
            )

        return _call_n_return(param)

    def delete(self, namespace, service):

        param = dict(
                api = 'delete_service' ,
                namespace = namespace,
                service_name = service,
            )
        
        return _call_n_return(param)

class Deployments(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('deployment', type=dict)

    def post(self, namespace):

        args = Deployments.parser.parse_args()

        param = dict(
                api = 'create_deployment' ,
                namespace = namespace,
                deployment = args['deployment'],
            )
        
        return _call_n_return(param)

class Scale(Resource):

    def put(self, namespace, deployment, replicas):
        
        param = dict(
                api = 'change_replicas' ,
                namespace   = namespace,
                deployment_name = deployment,
                replicas = replicas
            )
        
        return _call_n_return(param)

class Deployment(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('deployment_object', type=dict)

    def get(self, namespace, deployment):

        param = dict(
                api = 'get_deployment' ,
                namespace = namespace,
                deployment_name = deployment,
            )
        
        return _call_n_return(param)

    def delete(self, namespace, deployment):

        param = dict(
                api = 'delete_deployment' ,
                namespace = namespace,
                deployment_name = deployment,
            )
        
        return _call_n_return(param)

    def put(self, namespace, deployment):

        args = Deployment.parser.parse_args()

        param = dict(
                api = 'patch_deployment' ,
                namespace   = namespace,
                deployment_name = deployment,
                body = args['deployment_object']
            )
        
        return _call_n_return(param)

class CustomObject(Resource):

    parser = reqparse.RequestParser()
#    parser.add_argument('patch_function_name', type=str)
#    parser.add_argument('patch_function_code', type=str)
    parser.add_argument('custom_object', type=dict)

    def get(self, namespace, group, version, plural, custom_object_name):

        param = dict(
                api = 'get_custom_object' ,
                namespace   = namespace,
                object_name = custom_object_name,
                group       = group,
                version     = version,
                plural      = plural,
            )
        
        return _call_n_return(param)

    def put(self, namespace, group, version, plural, custom_object_name):

        args = CustomObject.parser.parse_args()

        param = dict(
                api = 'patch_custom_object' ,
                namespace   = namespace,
                object_name = custom_object_name,
                group       = group,
                version     = version,
                plural      = plural,
#                patch_function_name = args['patch_function_name'],
#                patch_function_code = args['patch_function_code'],
                custom_object = args['custom_object']
            )
        
        return _call_n_return(param)
    
class Job(Resource):

    def delete(self, namespace, job):

        param = dict(
                api = 'delete_job' ,
                namespace = namespace,
                job_name = job,
            )
        
        return _call_n_return(param)

class Jobs(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('job', type=dict)

    def post(self, namespace):

        args = Jobs.parser.parse_args()

        param = dict(
                api = 'create_job' ,
                namespace = namespace,
                job = args['job'],
            )
        
        return _call_n_return(param)

api.add_resource(Services, '/k8s/services/<string:namespace>', endpoint='services')
api.add_resource(Service, '/k8s/service/<string:namespace>/<string:service>', endpoint='service')
api.add_resource(Deployments, '/k8s/deployments/<string:namespace>', endpoint='deployments')
api.add_resource(Deployment, '/k8s/deployment/<string:namespace>/<string:deployment>', endpoint='deployment')
api.add_resource(CustomObject, '/k8s/customobject/<string:namespace>/<string:group>/<string:version>/<string:plural>/<string:custom_object_name>', endpoint='customobject')
api.add_resource(Jobs, '/k8s/jobs/<string:namespace>', endpoint='jobs')
api.add_resource(Job, '/k8s/job/<string:namespace>/<string:job>', endpoint='job')
api.add_resource(Scale, '/k8s/scale/<string:namespace>/<string:deployment>/<int:replicas>', endpoint='scale')
