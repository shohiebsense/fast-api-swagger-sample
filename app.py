from fastapi import FastAPI, Request
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None

@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    return item

@app.get("/items/{name}", response_model=Item)
async def get_item_by_name(name: str):
    return {"name": name, "description": "Sample description", "price": 10.99, "tax": 1.1}

@app.get("/openapi.json")
async def get_open_api_endpoint():
    return JSONResponse(content=get_openapi(title="FastAPI", version="1.0.0", routes=app.routes))

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "version": "1.0.0"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
