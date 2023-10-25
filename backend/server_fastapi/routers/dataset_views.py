import json
from glob import glob
import os
import os.path as path
import requests
from backend.params.specifications import Specifications
from backend.server.utils.helpers import get_object_from_name
from fastapi import APIRouter, Depends, HTTPException,Response, status, Body
from typing import Any, Dict, AnyStr, List, Union
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import backend.server_fastapi.state as state

router = APIRouter(
    prefix="/datasets",
    tags=["Dataset"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.get('/')
def datasetsList():
    specs = Specifications(state.state.get("MODELS_DIR"), state.state.get("DATASETS_DIR"))
    return {'datasets_summarization': specs._list_datasets_summarization, 'datasets_search': specs._list_datasets_search}

@router.get('/files')
def datasetFilesList(dataset: str):
    dataset_name = str(dataset)
    dataset_obj = get_object_from_name(dataset_name, state.state.get("server_config"), 'dataset')
    if not dataset_obj:
        return "That dataset doesn't exist", 404

    titles = dataset_obj._get_topic_titles()
    return {"files": titles}

