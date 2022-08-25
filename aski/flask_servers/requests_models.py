from glob import glob
from multiprocessing import Process, Manager 
import string 

from aski.flask_servers.flask_constants import FILES_DIR, MODELS_DIR, DATASETS_DIR 
from aski.params.specifications import Specifications
from aski.utils.helpers import get_model_object_from_name, get_dataset_object_from_name

"""

All models-related methods.

"""

manager = Manager() 

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
        - Input: {"model": str, "filename": str, "filecontent": str} <-- last two are optional!
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
        print(f"currently examining {model}")
        if model._info['class_name'] == model_name: 

            model = get_model_object_from_name(model_name, server_config)
            if callable(getattr(model, "load_model", None)): 

                if any(param not in json for param in ['filename', 'filecontent']):
                    return "Malformed request", 400

                model.load_model(str(json['filename']), str(json['filecontent']))

            return {"response" : "success"}, 200 

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

    query = query.translate(string.punctuation)

    model = get_model_object_from_name(model_name, server_config)
    res, latency = model.file_search(query)

    return {'result' : res, 'latency' : latency}, 200 

def search_file(request, server_config): 
    """
    6) GET/models/search/file - get model answer (if search)
        - Input: {"model": str, "filename": str, "filecontent": str, "query": str}
        - Output: {"result": str, "latency": float}
        - Use Case: 
        - Who's Doing: Advit    
    """

    json = request.json
    if any(param not in json for param in ['model', 'filename', 'filecontent', 'query']):
        return "Malformed request", 400

    model_name = json['model']
    file_name = json['filename']
    file_content = json['filecontent']
    query = json['query']

    model = get_model_object_from_name(model_name, server_config)

    model.load_model(file_name, file_content)
    res, latency = model.file_search(query)

    return {'result' : res, 'latency' : latency}, 200

def benchmark(request, server_config): 
    """
    7) GET/models/benchmark - model benchmark progress 
        - Input: {"model": str, "filename": str, "dataset": str, "task": str} <-- task can be either "start", "read"
        - Output: {"results": dict}
        - Use Case: model benchmarking or model comparison 
        - Who's Doing: Advit 
    """

    json = request.json
    if any(param not in json for param in ['model', 'dataset', 'task', 'filename']):
        return "Malformed request", 400
    
    model_name = str(json['model']) 
    dataset_name = str(json['dataset'])
    file_name = str(json['filename'])
    task = str(json['task'])

    process_name = f"{model_name}-{dataset_name}"

    # If there is a process already running with this model: 
    if process_name in server_config['processes']: 
        if task == 'stop': 
            server_config['processes'][process_name][0].kill()
            server_config['processes'][process_name][1] = manager.dict() 
            server_config['processes'].pop(process_name)

            return {"response" : "Stopped succesfully"}, 200 

        elif task == 'read': 
            res = server_config['processes'][process_name][1] 

            print(res) 

            d = dict() 
            d = res.copy() 

            return {"res": d}, 200 

        else: 
            return "Malformed request", 400 
    
    else: 
        if task == 'start':

            dataset_obj = get_dataset_object_from_name(dataset_name, server_config)

            results = dict() 
            print("tryna start it")
            server_config['processes'][process_name] = [None, manager.dict()]
            server_config['processes'][process_name][0] = Process(target=dataset_obj._benchmark, args=(model_name, file_name,
                                                                    server_config['processes'][process_name][1])
                                                                  )
            server_config['processes'][process_name][0].start() 
            #server_config['processes'][process_name][0].join() 
            return {"response" : "Started succesfully"}, 200 

        else: 
            return "Malformed request", 400 




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
            server_config['processes'][process][1] = {} 

            server_config['processes'].pop(process)
            return {"response" : "Killed successfully."}, 200 

    return "That model isn't running in a separate process", 404 
