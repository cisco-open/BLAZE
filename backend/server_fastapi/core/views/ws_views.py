from fastapi import  WebSocket, APIRouter
from fastapi.responses import HTMLResponse
import backend.server_fastapi.state as state
from backend.models.interfaces.model_search import squad_benchmarkV2
import json
import asyncio
import time

router = APIRouter(
    prefix="/ws",
    tags=["WebSockets"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.websocket("/benchmark")
async def benchmark(websocket: WebSocket):
    await websocket.accept()
    count = 0 
    print(state.state)
    while True:
        data = await websocket.receive_text()
        file = data
        model_obj = state.state.get("server_config")["model_objs"]["search"][0]        
        for res in squad_benchmarkV2(file_name=file,model_obj=model_obj,websocket_response=True):
            # print(res)
            await websocket.send_text(json.dumps(res))
            await asyncio.sleep(0.1)
        
@router.websocket("/benchmark2")
async def benchmark(websocket: WebSocket):
    await websocket.accept()
    count = 0 
    print(state.state)
    while True:
        data = await websocket.receive_text()
        file = data
        model_obj = state.state.get("server_config")["model_objs"]["search"][1]        
        for res in squad_benchmarkV2(file_name=file,model_obj=model_obj,websocket_response=True):
            # print(res)
            await websocket.send_text(json.dumps(res))
            await asyncio.sleep(0.1)
        