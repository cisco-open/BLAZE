
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


from importlib import import_module
import yaml
import os
import json
import time

def profile(func):
    def wrap(*args, **kwargs):
        if "ASKI_PROFILING" in os.environ:
            shouldRunProfile = json.loads(
                os.environ.get('ASKI_PROFILING').lower())
        if not shouldRunProfile:
            result = func(*args, **kwargs)
            return result
        started_at = time.time()
        result = func(*args, **kwargs)
        print(str(func.__name__)+": Time taken to execute -> " +
              str(time.time() - started_at) + ":For Args -> "+str(args)+str(kwargs))
        return result

    return wrap


@profile
def get_list_objects(list_objects_str, task, object_type):
    """ 
    Function that takes as input a list of strings of the models we want to use
    for the dashboard and that returns a list of the different models as 
    objects.
    Parameters
    ----------
    list_models_str : list of Strings
      List of the models we want to use for the dashboard as Strings
    Returns
    -------
    list_models_obj : list of Model objects
        List of the models we want to use for the dashboard as Objects
    """

    list_objects = []
   
    for object_name in list_objects_str:
        print(object_name)
        object_var = call_object_class_from_name(
            object_name, task, object_type)

        list_objects.append(object_var)

    return list_objects


@profile
def call_object_class_from_name(object_name, task, object_type):
    print("calling_object_class_from_name")
    # Get the class as a variable
    object_class = import_module(
        "backend." + object_type + '.' + task + '.' + object_name).__getattribute__(object_name)

    # Call the class
    object_var = object_class()
    return object_var


@profile
def get_object_from_name(object_name, params, object_type):

    try:
        list_objs = params._data_dict['states'][object_type + '_objs']
    except:
        list_objs = params[object_type + '_objs']

    object_active = object_name
    current_object = None

    for object_iter in list_objs:
        object_name = object_iter._get_class_name()

        if object_name == object_active:
            current_object = object_iter

    return current_object


def dump_yaml(data, path):

    with open(path, mode="wt", encoding="utf-8") as file:
        yaml.dump(data, file)


@profile
def get_current_model(params):

    model_active = params._data_dict['states']['model_active'][0]
    current_model = None

    for model in params._data_dict['states']['model_objs']:
        model_name = model._get_class_name()

        if model_name == model_active:
            current_model = model

    return current_model


@profile
def get_model_object_from_name(model_name, task, data_dict):

    try:
        list_objs = data_dict['states']['model_dict'][task]
    except:
        list_objs = data_dict['model_objs'][task]

    model_active = model_name
    current_model = None

    for model in list_objs:
        model_name = model._get_class_name()

        if model_name == model_active:
            current_model = model

    return current_model


