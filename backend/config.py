import os
import os.path as path
basedir = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))


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
    WEBEX_BOT_TOKEN = os.environ.get('WEBEX_BOT_TOKEN', "")
    WEBEX_ACCESS_TOKEN = os.environ.get('WEBEX_ACCESS_TOKEN', "")

    OPENAPI_KEY = os.environ.get('OPENAPI_KEY', "")

    @classmethod
    def public_config(self):
        return {
            "WEBEX_BOT_TOKEN": self.WEBEX_BOT_TOKEN,
            "WEBEX_ACCESS_TOKEN":self.WEBEX_ACCESS_TOKEN,
            "OPENAPI_KEY":self.OPENAPI_KEY
        }

