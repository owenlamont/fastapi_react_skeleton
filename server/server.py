from fastapi import FastAPI, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

app = FastAPI()


# CORS logic below is for testing when launching the client with npm start
# Taken from: https://testdriven.io/blog/fastapi-react/
origins = [
    "http://localhost:3000",
    "localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Mount the static path for static files queries
app.mount("/static", StaticFiles(directory="../client/build/static"), name="static")

# Set the template directory as the build directory (I don't know if we really need templates
# for a React app - or if HTMLResponse can be given without one)
templates = Jinja2Templates(directory="../client/build/")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """
    Return home page if no file is explicitly requested
    :param request: Request received
    :return: index.html
    """
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/{page_name}", response_class=HTMLResponse)
async def read_page(request: Request, page_name: str, response: Response):
    """
    Return a requested file if it is found otherwise return 404 status
    :param request: Request received
    :param page_name: Name of the file being requested
    :param response: response parameter for setting status manually if needed
    :return: Contents of the file if found or 404 status otherwise
    """
    if Path(f"../client/build/{page_name}").is_file():
        return templates.TemplateResponse(page_name, {"request": request})
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
