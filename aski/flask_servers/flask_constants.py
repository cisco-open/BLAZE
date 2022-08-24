import os.path as path

# ASKI/data
FILES_DIR    = path.realpath(path.join(path.dirname(path.realpath(__file__)), '..', '..', 'data'))

# /ASKI/aski/models
MODELS_DIR   = path.realpath(path.join(path.dirname(path.realpath(__file__)), '..', 'models/'))

# /ASKI/aski/datasets
DATASETS_DIR = path.realpath(path.join(path.dirname(path.realpath(__file__)), '..', 'datasets/'))
