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
    PORT_REST_API = 3000
    PREF_REST_API = "http://0.0.0.0:"
    DATABASE_URI = 'test'
    TESTING = True
