"""

 model-related

    1) GET/models/all_models - all available models 
        - Input: {}
        - Output: {"models": [str]}
        - Use Case: 
        - Who's Doing: Thomas
    
    1) GET/models/model - model details 
        - Input: {"model": str}
        - Output: {"model_info" : dict} <-- can add in datasets used to benchmark
        - Use Case: For latency, accuracy information (pre-stored) <-- overall!
        - Who's Doing: Jason
    
    2) POST/models/initialize - initialize model 
        - Input: {"model": str}
        - Output: {}
        - Use Case: to initialize a model (make sure no pid/model alr running)
        - Who's Doing: Advit
    
    3) POST/models/kill - kill/reset model 
        - Input: {"model": str}
        - Output: {}
        - Use Case: if we want to index model on some other data
        - Who's Doing: Advit

    4) GET/models/summary - get model summary (if summary)
        - Input: {"model": str}
        - Output: {"result": str, "filename": str, "latency": float}
        - Use Case: 
        - Who's Doing: Thomas

    5) GET/models/search - get model answer (if search)
        - Input: {"model": str, "query": str}
        - Output: {"result": str, "latency": float}
        - Use Case: 
        - Who's Doing: Advit 

    6) GET/models/search/file - get model answer (if search)
        - Input: {"model": str, "filename": str, "query": str}
        - Output: {"result": str, "latency": float}
        - Use Case: 
        - Who's Doing: Advit

    7) GET/models/benchmark - model benchmark progress 
        - Input: {"model": str}
        - Output: {"results": Queue}
        - Use Case: model benchmarking or model comparison 
        - Who's Doing: Advit 


"""