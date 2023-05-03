
# Copyright 2022 Cisco Systems, Inc. and its affiliates
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0


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
