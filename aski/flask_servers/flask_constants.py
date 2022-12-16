
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



import os.path as path

# ASKI/user
FILES_DIR    = path.realpath(path.join(path.dirname(path.realpath(__file__)), '..', '..', 'user'))

# /ASKI/aski/models
MODELS_DIR   = path.realpath(path.join(path.dirname(path.realpath(__file__)), '..', 'models/'))

# /ASKI/aski/datasets
DATASETS_DIR = path.realpath(path.join(path.dirname(path.realpath(__file__)), '..', 'datasets/'))

PORT_REST_API = 3000
PREF_REST_API = "http://0.0.0.0:"