import json
from glob import glob
import os
import os.path as path
import requests
from backend.server.utils.helpers import get_object_from_name
from fastapi import APIRouter, Depends, HTTPException, Response, status, Body
from typing import Any, Dict, AnyStr, List, Union, Annotated
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import backend.server_fastapi.state as state
from backend.params.specifications import Specifications
from backend.server_fastapi.core.schemas.dataset_schema import DatasetFileList, UploadedFile, File
from backend.server_fastapi.core.schemas.general_schema import Error404Message
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix="/datasets",
    tags=["Dataset"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get('/')
def datasets():
    """
     List all datasets
    """
    specs = Specifications()
    return {'datasets_summarization': specs._list_datasets_summarization, 'datasets_search': specs._list_datasets_search}


@router.get('/files',
            response_model=DatasetFileList,
            responses={
                404: {"model": Error404Message, "description": "Files not found for dataset"},
                200: {
                    "description": "Dataset files requested by Datasetname",
                    "content": {
                        "application/json": {
                            "files": ["Beyonce", "The Nightangle"]
                        }
                    },
                },
            },)
def dataset_files_list(dataset: str):
    """
     List the files from given dataset name
    """
    dataset_name = str(dataset)
    dataset_obj = get_object_from_name(
        dataset_name, state.state.get("server_config"), 'dataset')
    if not dataset_obj:
        return JSONResponse(status_code=404, content={"message": "Files not found"})

    titles = dataset_obj._get_topic_titles()
    return {"files": titles}


@router.post('/files', response_model=UploadedFile,
             responses={
                 404: {"model": Error404Message, "description": "Files not found for dataset"},
                 200: {
                     "description": "Returns uploaded if uploaded successful",
                     "content": {
                         "application/json": {
                             "message": "Uploaded"
                         }
                     },
                 },
             },)
def dataset_file_Upload(file: UploadedFile):
    """
     Create file using the filename and content
    """

    if not any(file.fileName.endswith(ext) for ext in ['.txt', '.pdf']):
        return JSONResponse(status_code=404, content={"message": "Please use either .txt or .pdf filename"})

    print(state.state)
    filepath = path.join(state.state.get("FILES_DIR"), file.fileName)
    isBytes = "" if file.fileName.endswith('.txt') else 'b'
    with open(filepath, f'w{isBytes}') as f:
        f.write(file.content)

    for dataset_obj in state.state.get("server_config")['dataset_objs']:
        if dataset_obj._dataset_name == "User":
            dataset_obj._update_file(file.fileName)
            break

    return {"message": "Uploaded"}, 200


@router.post('/datasets/files/detail',
             response_model=File,
             responses={
                 404: {"model": Error404Message, "description": "File not found"},
                 200: {
                     "description": "Details of files",
                     "content": {
                         "application/json": {
                             "content": "test",
                             "size": "1"
                         }
                     },
                 },
             },)
def dataset_file_details(fileName: Annotated[str, Body()], fileClass: Annotated[str, Body()]) -> Union[Dict[str, str], None]:
    if fileClass == 'User' or fileName == "WebEx":
        filepaths = glob(
            path.join(state.state.get("FILES_DIR"), '**', fileName), recursive=True)

        if len(filepaths) > 0:
            filepath = filepaths[0]

            with open(filepath, 'r') as f:
                if filepath.endswith(".json"):
                    content = json.loads(f.read())
                else:
                    content = f.read()
                size = os.path.getsize(filepath) / 1000
        else:
            return JSONResponse(status_code=404, content={"message": "File does not exist"})
    else:

        dataset_obj = get_object_from_name(
            fileClass, state.state.get("server_config"), 'dataset')
        print(dataset_obj)
        if 'search' in dataset_obj.functions_supported:
            content = dataset_obj._get_title_story(fileName)
            content = ' '.join(sentence for sentence in content)
            size = "N/A"
        elif ("summarization" in dataset_obj.functions_supported) and ("search" not in dataset_obj):
            content = None
            size = None
        else:
            return JSONResponse(status_code=404, content={"message": "File does not exist"})

    response_data = {}
    response_data['content'] = content
    response_data['size'] = size

    return response_data


@router.post('/list_webex_meeting_transcripts',
             response_model=File,
             responses={
                 404: {"model": Error404Message, "description": "File not found"},
                 200: {
                     "description": "List meeting transcripts",
                     "content": {
                         "application/json": {
                             "response": "[]",
                             "recordings": "[]"
                         }
                     },
                 },
             },)
def list_meeting_transcripts():
    dataset_obj = get_object_from_name(
        "WebEx", state.state.get("server_config"), 'dataset')
    if not dataset_obj:
        return JSONResponse(status_code=404, content={"message": "That dataset doesn't exist"})
   
    return {"response": dataset_obj.list_meetings(), "recordings": dataset_obj.recordings}
