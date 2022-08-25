from glob import glob
import os
import os.path as path

from aski.flask_servers.flask_constants import FILES_DIR, MODELS_DIR, DATASETS_DIR 
from aski.params.specifications import Specifications


"""

All files-related methods.

"""

def all_datasets(request, server_config):
	"""
    1) GET/files/all_datasets - all available datasets (datasets)
        - Input: {}
        - Output: {"datasets_summarization": {"name": [str]}, "datasets_search": {"name": [str]}}
        - Use Case: Generate that dropdown for the dash 
        - Who's Doing: Thomas
    """
	specs = Specifications(MODELS_DIR, DATASETS_DIR)
	return {'datasets_summarization' : specs._list_datasets_summarization, 'datasets_search' : specs._list_datasets_search}, 200

def file(request, server_config):
    """
    2) GET/files/file - specific file text (details) 
        - Input: {"file": str}
        - Output: {"file": str, "content": str, "content-length": int}
        - Use Case: Show preview for files
        - Who's Doing: Jason
    """
    json = request.json
    if any(param not in json for param in ['file']):
        return "Malformed request", 400
    
    filepaths = glob(path.join(FILES_DIR, '**', json['file']), recursive=True)
    
    if len(filepaths) > 0:
        filepath = filepaths[0]
        response_data = {}
        with open(filepath, 'r') as f:
            response_data['content'] = f.read()
        response_data['file'] = json['file']
        response_data['content-length'] = len(response_data['content'])
        return response_data, 200
    else:
        return "That file doesn't exist", 404

def load(request, server_config): 
    """
    3) POST/files/load - load datasets 
        - Input: {"datasets": [str]}
        - Output: {}
        - Use Case: if user chooses squad + cnn dailymail in yaml
        - Who's Doing: Advit
    """

    # TODO: cannot implement since all data is currently local 
    # TODO: implement squad, cnn dailymail as huggingface classes
    # TODO: then, files are not local .txt's and must be loaded 
    pass 

def upload(request, server_config):
    """
    4) POST/files/upload - user uploads file 
        - Input: {"file": str, "content": str}
        - Output: {}
        - Use Case: when the user uploads a file
        - Who's Doing: Jason

    5) DELETE/files/upload - user deletes file
        - Input: {"file": str}
        - Output: {}
        - Use Case: when the user deletes a **CUSTOM** file
        - Who's Doing: Jason
    """
    if request.method == 'POST':
        json = request.json
        if any(param not in json for param in ['file', 'content']):
            return "Malformed request", 400
        
        filepath = path.join(FILES_DIR, 'user_files', json['file'])
        with open(filepath, 'w') as f:
            f.write(json['content'])
        return {}, 201
    elif request.method == 'DELETE':
        json = request.json
        if any(param not in json for param in ['file']):
            return "Malformed request", 400

        filepath = path.join(FILES_DIR, 'user_files', json['file'])
        if os.path.exists(filepath):
            os.remove(filepath)
            return {}, 204
        else:
            return {}, 404

    def generate_dash(request, server_config):
        """
        4) POST/files/upload - user uploads file 
        - Input: {"file": str, "content": str}
        - Output: {"dash": str}
        - Use Case: 
        - Who's Doing: Jason
        """
        json = request.json
        if any(param not in json for param in ['file', 'content']):
            return "Malformed request", 400

        return {"dash": "http://localhost:5001"}