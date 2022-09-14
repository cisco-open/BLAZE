import os.path as path

# ASKI/user
FILES_DIR    = path.realpath(path.join(path.dirname(path.realpath(__file__)), '..', '..', 'user'))

# /ASKI/aski/models
MODELS_DIR   = path.realpath(path.join(path.dirname(path.realpath(__file__)), '..', 'models/'))

# /ASKI/aski/datasets
DATASETS_DIR = path.realpath(path.join(path.dirname(path.realpath(__file__)), '..', 'datasets/'))

PORT_REST_API = 3000
PREF_REST_API = "http://0.0.0.0:"