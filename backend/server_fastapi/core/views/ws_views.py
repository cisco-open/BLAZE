from fastapi import  WebSocket, APIRouter
from fastapi.responses import HTMLResponse
import backend.server_fastapi.state as state
from backend.models.interfaces.model_search import squad_benchmarkV2
import json
import asyncio

count = 0
router = APIRouter(
    prefix="/ws",
    tags=["WebSockets"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws/benchmark");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""

@router.get("/")
async def get():
    return HTMLResponse(html)

def posCount(websocket):
    count = count+1
    websocket.send_text(f"Message text was: {count}")

import time
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
        