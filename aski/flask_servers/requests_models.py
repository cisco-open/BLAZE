from glob import glob

from aski.flask_servers.flask_constants import FILES_DIR, MODELS_DIR, DATASETS_DIR 
from aski.params.specifications import Specifications
from aski.utils.helpers import get_model_object_from_name


"""

All models-related methods.

"""

def all_models(request, server_config):
    """
    1) GET/models/all_models - all available models 
        - Input: {}
        - Output: {"models_summarization": [str], "models_search": [str]}
        - Use Case: 
        - Who's Doing: Thomas
    """

    specs = Specifications(MODELS_DIR, DATASETS_DIR)
    return specs._list_models_summarization, specs._list_models_search

def model(request, server_config): 
    """
    2) GET/models/model - model details 
        - Input: {"model": str}
        - Output: {"model_info" : dict} <-- can add in datasets used to benchmark
        - Use Case: For latency, accuracy information (pre-stored) <-- overall!
        - Who's Doing: Advit
    """

    pass 

def initialize(request, server_config): 
    """
    3) POST/models/initialize - initialize model 
        - Input: {"model": str}
        - Output: {}
        - Use Case: to initialize a model (make sure no pid/model alr running)
        - Who's Doing: Advit

    """

    pass 

def summary(request, server_config):
    """
    4) GET/models/summarization - get model summary 
        - Input: {"model": str, "content": str}
        - Output: {"result": str}
        - Use Case: 
        - Who's Doing: Thomas
    """

    json = request.json
    if any(param not in json for param in ['model', 'content']):
        return "Malformed request", 400

    model_name        = json['model']
    text_to_summarize = json['content']

    model = get_model_object_from_name(model_name, server_config)
    summarized_text = model._summarize_text(text_to_summarize)

    return summarized_text

def search(request, server_config): 
    """
    5) GET/models/search - get model answer (if search)
        - Input: {"model": str, "query": str}
        - Output: {"result": str, "latency": float}
        - Use Case: 
        - Who's Doing: Advit 
    """

def search_file(request, server_config): 
    """
    6) GET/models/search/file - get model answer (if search)
        - Input: {"model": str, "filename": str, "query": str}
        - Output: {"result": str, "latency": float}
        - Use Case: 
        - Who's Doing: Advit    
    """

    pass 

def benchmark(request, server_config): 
    """
    7) GET/models/benchmark - model benchmark progress 
        - Input: {"model": str}
        - Output: {"results": Queue}
        - Use Case: model benchmarking or model comparison 
        - Who's Doing: Advit 
    """

    pass 

def kill(request, server_config): 
    """
    8) POST/models/kill - kill/reset model 
        - Input: {"model": str}
        - Output: {}
        - Use Case: if we want to index model on some other data
        - Who's Doing: Advit
    """

    pass 
