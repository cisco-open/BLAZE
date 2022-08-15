from importlib import import_module
import yaml

def get_list_models(list_models_str, task):
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

    list_models_obj = []

    for model_name in list_models_str:
      model = call_model_class_from_name(model_name, task)
      
      list_models_obj.append(model)

    return list_models_obj

def call_model_class_from_name(model_name, task):

    model_class = import_module("aski.models." + task + '.' + model_name) \
                            .__getattribute__(model_name) 

    model = model_class()

    return model

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

def get_model_object_from_name(model_name, params):

    model_active = model_name
    current_model = None 

    for model in params._data_dict['states']['model_objs']:
        model_name = model._get_class_name()

        if model_name == model_active:
            current_model = model

    return current_model
