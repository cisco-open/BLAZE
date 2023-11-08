import os
import os.path as path
from tinydb import TinyDB, Query
basedir = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))


class Config(object):
    TESTING = False


class ProductionConfig(Config):
    DATABASE_URI = 'test'


class DevelopmentConfig(Config):
    # ASKI/user
    FILES_DIR = os.path.join(basedir, "user")
    DB_CONFIG_FILE = os.path.join(basedir, "config.json")
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

    ############DB Config###############
    DB_CONFIG_FILE = os.path.join(basedir, "config.json")
    db = TinyDB(DB_CONFIG_FILE)
    DBConfig = Query()
    # /ASKI/aski/models
    MODELS_DIR = os.path.join(basedir, "backend/models/")
    CONFIG_DIR = os.path.join(basedir)

    # /ASKI/aski/datasets 
    DATASETS_DIR = os.path.join(basedir, "backend/datasets/")
    PORT_REST_API = os.environ.get('PORT_REST_API', 3000)
    PREF_REST_API = "http://0.0.0.0:"
    DATABASE_URI = 'test'
    TESTING = True
    WEBEX_BOT_TOKEN = os.environ.get('WEBEX_BOT_TOKEN', "")
    WEBEX_ACCESS_TOKEN = os.environ.get('WEBEX_ACCESS_TOKEN', "")

    OPENAPI_KEY = os.environ.get('OPENAPI_KEY', "")
    all_modules = {"openai":"backend.server.utils.openai_utils"}
    BOT_EMAIL = 'blazetranscriptionbot@webex.bot'

    SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN', "")
    SLACK_APP_TOKEN = os.environ.get('SLACK_APP_TOKEN', "")
    

    @classmethod
    def public_config(self):
        return {
            "WEBEX_BOT_TOKEN": self.WEBEX_BOT_TOKEN,
            "WEBEX_ACCESS_TOKEN":self.WEBEX_ACCESS_TOKEN,
            "OPENAPI_KEY":self.OPENAPI_KEY,
            "SLACK_APP_TOKEN": self.SLACK_APP_TOKEN,
            "SLACK_BOT_TOKEN": self.SLACK_BOT_TOKEN
        }
    
    @classmethod
    def yaml_allowed_moduls(cls,yaml_defined_modules):
        allowed_modules = {}
        for module in yaml_defined_modules:
            allowed_modules[module] = cls.all_modules.get(module)
       
        return allowed_modules
