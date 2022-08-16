from importlib import import_module
import yaml

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
      object_var = call_object_class_from_name(object_name, task, object_type)
      
      list_objects.append(object_var)

    return list_objects

def call_object_class_from_name(object_name, task, object_type):

    # Get the class as a variable
    object_class = import_module(
        "aski." + object_type + '.' + task + '.' + object_name).__getattribute__(object_name) 

    # Call the class
    object_var = object_class()
    return object_var

def get_object_from_name(object_name, params, object_type):

    object_active = object_name
    current_object = None 

    for object_iter in params._data_dict['states'][object_type + '_objs']:
        object_name = object_iter._get_class_name()

        if object_name == object_active:
            current_object = object_iter

    return current_object

def dump_yaml(data, path):

    with open(path, mode="wt", encoding="utf-8") as file:
        yaml.dump(data, file)

def get_current_model(params):

    model_active = params._data_dict['states']['model_active'][0]
    current_model = None 

    for model in params._data_dict['states']['model_objs']:
        model_name = model._get_class_name()

        if model_name == model_active:
            current_model = model

    return current_model
