import json
import asyncio
import uvicorn
from fastapi import FastAPI
from fastapi import Request
from fastapi import WebSocket
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class ToDoRequest(BaseModel):
    task: str

marks = ["se", ]
# with open('measurements.json', 'r') as file:
    # measurements = iter(json.loads(file.read()))
@app.post("/set")
def set_values(value:ToDoRequest):
    marks.append(value.task)
    return value


@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        await asyncio.sleep(0.1)
        if len(marks) > 0:
            payload = next(iter(marks))
            print(payload, "aaaaaa")
            await websocket.send_json({"value":payload})
            marks.remove(payload)

def main():
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_level="debug",
        reload=True,
        debug=True,
    )


if __name__ == "__main__":
    main()
