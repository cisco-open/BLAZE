from pydantic import BaseModel

class Error404Message(BaseModel):
    message: str
