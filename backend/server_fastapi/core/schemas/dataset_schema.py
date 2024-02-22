from pydantic import BaseModel
from typing import Union

class DatasetFilesUpload(BaseModel):
    file: str
    content: Union[str, None] = None


class DatasetFileList(BaseModel):
    files: list[str]

class UploadedFile(BaseModel):
    fileName:str
    content:str

class File(BaseModel):
    filename:str
    fileClass:str