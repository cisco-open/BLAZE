from glob import glob
from flask_restful import Resource, request
from flask import current_app


class Panoptica_prompt_with_functions(Resource):
    
    def post(self):
        pass