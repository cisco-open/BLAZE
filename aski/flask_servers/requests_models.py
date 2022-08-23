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
    return {'models_summarization' : specs._list_models_summarization, 'models_search' : specs._list_models_search}

def model(request, server_config): 
    """
    2) GET/models/model - model details 
        - Input: {"model": str}
        - Output: {"model_info" : dict} <-- can add in datasets used to benchmark
        - Use Case: For latency, accuracy information (pre-stored) <-- overall!
        - Who's Doing: Advit
    """

    json = request.json

    if any(param not in json for param in ['model']):
        return "Malformed request", 400

    model_name = str(json['model']) 
    for model in server_config['model_objs']: 
        if model._info['class_name'] == model_name: 
            return {'model_info' : model._info}, 200 

    return "That model doesn't exist", 404 

def initialize(request, server_config): 
    """
    3) POST/models/initialize - initialize model 
        - Input: {"model": str}
        - Output: {}
        - Use Case: to initialize a model (make sure no pid/model alr running)
        - Who's Doing: Advit

    TODO: Figure out whether this should look at processes, or at model_objs
    TODO: Figure out concrete functionality for this method... unsure 

    TODO: This will be for initializing search (indexing on a file!)

    """

    json = request.json
    if any(param not in json for param in ['model']):
        return "Malformed request", 400
    
    model_name = str(json['model']) 

    for model in server_config['model_objs']: 
        if model._info['class_name'] == model_name: 
            return 200 

    return "That model doesn't exist", 404 

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

    return {'result' : summarized_text}, 200

def search(request, server_config): 
    """
    5) GET/models/search - get model answer (if search)
        - Input: {"model": str, "query": str}
        - Output: {"result": str, "latency": float}
        - Use Case: 
        - Who's Doing: Advit 
    """

    json = request.json
    if any(param not in json for param in ['model', 'query']):
        return "Malformed request", 400

    model_name = json['model']
    query = json['query']

    model = get_model_object_from_name(model_name, server_config)
    res, latency = model.file_search(query)

    return {'result' : res, 'latency' : latency}, 200 

def search_file(request, server_config): 
    """
    6) GET/models/search/file - get model answer (if search)
        - Input: {"model": str, "filename": str, "query": str}
        - Output: {"result": str, "latency": float}
        - Use Case: 
        - Who's Doing: Advit    
    """

    json = request.json
    if any(param not in json for param in ['model', 'filename', 'query']):
        return "Malformed request", 400

    model_name = json['model']
    file_name = json['filename']
    query = json['query']

    # TODO: Figure out file content <-- will given attribute be file name? 
    # TODO: What structure will it take? Pass in content directly? TBD

    file_content = None 

    model = get_model_object_from_name(model_name, server_config)

    model.load_model(file_name, file_content)
    res, latency = model.file_search(query)

    return {'result' : res, 'latency' : latency}, 200

def benchmark(request, server_config): 
    """
    7) GET/models/benchmark - model benchmark progress 
        - Input: {"model": str}
        - Output: {"results": Queue}
        - Use Case: model benchmarking or model comparison 
        - Who's Doing: Advit 
    """

    json = request.json
    if any(param not in json for param in ['model']):
        return "Malformed request", 400
    
    model_name = str(json['model']) 

    for process in server_config['processes']: 
        if process == model_name: 
            # There is a process already running with this model 

            # TODO: Reimplement queue, replace with FIFO/Value/List 
            # TODO: No need to store ALL results (most are empty)
            # TODO: Just need the last results, which will be returned 

            res = server_config['processes'][process][1].pop()
            server_config['processes'][process][2] = res

            return {'results': res}, 200 


    return "That model isn't running in a separate process", 404 

def kill(request, server_config): 
    """
    8) POST/models/kill - kill/reset model 
        - Input: {"model": str}
        - Output: {}
        - Use Case: if we want to index model on some other data
        - Who's Doing: Advit
    """

    json = request.json
    if any(param not in json for param in ['model']):
        return "Malformed request", 400
    
    model_name = str(json['model']) 

    for process in server_config['processes']: 
        if process == model_name: 
            # There is a process already running with this model 
            server_config['processes'][process][0].kill()
            server_config['processes'][process][1].empty()
            server_config['processes'][process][2] = None 

            server_config['processes'].pop(process)
            return 200 

    return "That model isn't running in a separate process", 404 
