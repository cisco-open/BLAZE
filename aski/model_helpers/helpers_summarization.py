from importlib import import_module


def get_list_models(list_models_str):
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

    	model = call_model_class_from_name(model_name)

    	list_models_obj.append(model)

    return list_models_obj

def call_model_class_from_name(model_name):

	model_class = import_module("aski_summarization.models." + model_name) \
							.__getattribute__(model_name) 

	model = model_class()

	return model