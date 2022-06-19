import json
import asyncio
import uvicorn
from fastapi import FastAPI
from fastapi import Request
from fastapi import WebSocket
from fastapi.templating import Jinja2Templates


app = FastAPI()
templates = Jinja2Templates(directory="templates")


marks = ["se", ]
# with open('measurements.json', 'r') as file:
    # measurements = iter(json.loads(file.read()))
@app.get("/set")
def set_values(value: str):
    marks.append(value)
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
            payload = next(marks)
            await websocket.send_json(payload)

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
