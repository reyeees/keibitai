from socket import gethostbyname_ex, getfqdn
from random import choice as random
from json import dumps as json
from base64 import b64decode

from fastapi import FastAPI, Response, Request
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

# <----------------------- Data

class Data:
    def __init__(self) -> None:
        self.available_ports = gethostbyname_ex(getfqdn())[2]
        self.assets_file, self.port = self.parse_info()
        self.out_file: str = "saved_images.txt"
        self.data: list[dict] = self.parse()

    def deconcatenate(self, string: str) -> dict:
        first, second, third = string.split(" | ")
        return {
            "message": "SUCCESS",
            "percents": eval(first.split(" - ")[0]),
            "first_hash": second.split(" ")[0],
            "second_hash": second.split(" ")[1],
            "first_filename": third.split(" || ")[0],
            "second_filename": third.split(" || ")[1]
        }
    
    def parse_info(self) -> list[str]:
        with open("assets/info.txt", "r", encoding = "utf-8") as _file:
            return _file.read().split("\n")

    def parse(self) -> list:
        _file = open(self.assets_file, "r", encoding = "utf-8").read().strip().split("\n")
        return [self.deconcatenate(line.strip()) for line in _file]

# <------------------- server

data = Data()
app = FastAPI()
templates = Jinja2Templates(directory = "template")
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_methods = ["*"],
    allow_headers = ["*"],
    allow_credentials = True
)

@app.get("/file")
async def file(f: str) -> Response:
    f = b64decode(f.encode()).decode()
    return Response(content = open(f, "rb").read(), media_type = "image/jpeg")

@app.get("/index")
async def get_index(index: int = 0) -> Response:
    if index > len(data.data) - 1 or index < 0:
        return Response(content = json({"message": "Invalid request: Index out of bounds."}), media_type = "application/json")
    return Response(content = json(data.data[index]), media_type = "application/json")

@app.get("/save")
async def save(index: int) -> Response:
    if index > len(data.data) - 1:
        return Response(content = json({"message": "Failed: Index out of bounds."}), media_type = "application/json")
    with open(data.out_file, "a+", encoding = "utf-8") as file_:
        file_.write(json(data.data[index]))
        file_.write("\n")
        file_.flush()
        file_.close()
    return Response(content = json({"message": "SUCCESS"}), media_type = "application/json")

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "address": random(data.available_ports), "port": data.port})

# <------------------ bushes

print(f"http://{random(data.available_ports)}:8000") # <- Printing accessiable address