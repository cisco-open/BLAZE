# -*- coding: utf-8 -*-
"""This module contains a template MindMeld app configuration"""

# The namespace of the application. Used to prevent collisions in supporting services across
# applications. If not set here, the app's enclosing directory name is used.
# APP_NAMESPACE = 'app-name'

# Dictionaries for the various NLP classifier configurations

# An example decision tree model for intent classification

INTENT_CLASSIFIER_CONFIG = {
    'model_type': 'text',
    'model_settings': {
        'classifier_type': 'embedder'
    },
    'params': {
        'embedder_type': 'bert'
    }
}


"""
# Fill in the other model configurations if necessary
# DOMAIN_CLASSIFIER_CONFIG = {}
# ENTITY_RECOGNIZER_CONFIG = {}
# ROLE_CLASSIFIER_CONFIG = {}
"""

# A example configuration for the parser
"""
# *** Note: these are place holder entity types ***
PARSER_CONFIG = {
    'grandparent': {
        'parent': {},
        'child': {'max_instances': 1}
    },
    'parent': {
        'child': {'max_instances': 1}
    }
}
"""

AUGMENTATION_CONFIG = {
    "augmentor_class": "EnglishParaphraser",
    "batch_size": 8,
    "retain_entities": False,
    "paths": [
        {
            "domains": "query.*",
            "intents": "ask_question.*",
            "files": ".*",
        },
        {
            "domains": "query.*",
            "intents": "get_summary.*",
            "files": ".*",
        }
    ],
    "path_suffix": "-augmented.txt"
}

NLP_CONFIG = {"system_entity_recognizer": {}}