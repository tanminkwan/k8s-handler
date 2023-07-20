from flask import request, make_response
from flask_restful import Resource, reqparse
from flask_api import status
from miniagent import api
from miniagent.executer import ExecuterCaller

class Service(Resource):

    def get(self):

        data = dict(
            initial_param = dict(
                api = 'get_services' ,
            ),
            executer = 'k8s_handler.executer.k8s.K8SApi',
        )

        rtn, rtn_message = ExecuterCaller.instance().execute_command(data)
        
        if rtn:
            status_code = status.HTTP_200_OK            
        else:
            status_code = status.HTTP_404_NOT_FOUND

        return rtn_message, status_code
    
api.add_resource(Service, '/k8s/services', endpoint='services')
