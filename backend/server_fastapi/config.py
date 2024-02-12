import os
import os.path as path
from werkzeug.utils import import_string

#fastapi
basedir = os.path.normpath(os.path.join(os.path.dirname(__file__), "../.."))

#flask
# basedir = os.path.normpath(os.path.join(os.path.dirname(__file__), "../.."))


class Config(object):
    TESTING = False

    

    
class ProductionConfig(Config):
    DATABASE_URI = 'test'


class DevelopmentConfig(Config):
    # ASKI/user
    FILES_DIR = os.path.join(basedir, "user")

    # /ASKI/aski/models
    MODELS_DIR = os.path.join(basedir, "backend/models/")

    # /ASKI/aski/datasets 
    DATASETS_DIR = os.path.join(basedir, "backend/datasets/")

    PORT_REST_API = 3000
    PREF_REST_API = "http://0.0.0.0:"
    DATABASE_URI = 'test'
    TESTING = True


class TestingConfig(Config):
    # ASKI/user
    # ASKI/user
    FILES_DIR = os.path.join(basedir, "user")

    # /ASKI/aski/models
    MODELS_DIR = os.path.join(basedir, "backend/models/")

    # /ASKI/aski/datasets 
    DATASETS_DIR = os.path.join(basedir, "backend/datasets/")
    PORT_REST_API = os.environ.get('PORT_REST_API', 3000)
    PREF_REST_API = "http://0.0.0.0:"
    DATABASE_URI = 'test'
    TESTING = True
    WEBEX_BOT_TOKEN = os.environ.get('WEBEX_BOT_TOKEN', "NGM5N2U2MDgtMzc4YS00NjY1LWFjN2MtMjBhNTM4MTgzNzAyOWNkMmI3YTYtYjJk_PF84_1eb65fdf-9643-417f-9974-ad72cae0e10f")
    WEBEX_ACCESS_TOKEN = os.environ.get('WEBEX_ACCESS_TOKEN', "YTAzMGJmYmQtY2I1Ni00MGRmLWJlNWYtNDJjNjY1NmFjZjljM2RjODhmY2QtY2M4_PF84_1eb65fdf-9643-417f-9974-ad72cae0e10f")

    OPENAPI_KEY = os.environ.get('OPENAPI_KEY', "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")
    all_modules = {"openai":"backend.server.utils.openai_utils"}
    BOT_EMAIL = 'blazetranscriptionbot@webex.bot'
    

    @classmethod
    def public_config(self):
        return {
            "WEBEX_BOT_TOKEN": self.WEBEX_BOT_TOKEN,
            "WEBEX_ACCESS_TOKEN":self.WEBEX_ACCESS_TOKEN,
            "OPENAPI_KEY":self.OPENAPI_KEY
        }
    @classmethod
    def yaml_allowed_moduls(cls,yaml_defined_modules):
        allowed_modules = {}
        for module in yaml_defined_modules:
            allowed_modules[module] = cls.all_modules.get(module)
       
        return allowed_modules
