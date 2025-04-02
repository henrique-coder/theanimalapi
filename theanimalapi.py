# Standard modules
from datetime import datetime, timezone
from pathlib import Path
from random import choice

# Third-party modules
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from orjson import loads
from pydantic import BaseModel, Field
from uvicorn import run


app = FastAPI(
    title="The Animal API",
    description="A modern API for random animal photos and information",
    version="0.0.1",
    openapi_url=None,
    docs_url=None,
    redoc_url=None,
)

# Configure middleware and static files
app.add_middleware(CORSMiddleware, allow_credentials=True, allow_origins=["*"], allow_methods=["GET"], allow_headers=["*"])
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Load configuration and data
config = loads(Path("config.json").read_bytes())
animal_images = loads(Path("dynamic/animals.json").read_bytes())


class AnimalResponse(BaseModel):
    """Response model for animal data"""

    name: str = Field(..., description="Animal species name")
    url: str = Field(..., description="URL to the animal image")
    timestamp: str = Field(..., description="UTC timestamp of when the response was generated")


@app.get("/", response_class=RedirectResponse)
async def index() -> RedirectResponse:
    """Redirects to the API documentation"""

    return RedirectResponse(url="/docs")


@app.get("/docs", response_class=JSONResponse)
async def docs(request: Request) -> JSONResponse:
    """Custom API documentation page"""

    return templates.TemplateResponse("docs.html", {"request": request})


@app.get(
    "/api/v1/search/animal",
    response_model=AnimalResponse,
    responses={
        200: {"description": "Successfully retrieved animal information"},
        404: {"description": "Animal not found"},
        500: {"description": "Server error"},
    },
)
async def search_animal(name: str | None = None) -> AnimalResponse:
    """
    Get information about an animal with optional filtering.

    - If no name is provided, a random animal will be selected
    """

    # Get list of animals that have at least one image
    valid_animals = [animal for animal, images in animal_images["animals"].items() if images]

    if not valid_animals:
        raise HTTPException(status_code=500, detail="No animals with images found in the database")

    # Handle animal selection
    if name is None:
        name = choice(valid_animals)
    elif name not in animal_images["animals"]:
        raise HTTPException(status_code=404, detail="Animal not found in the database")
    elif not animal_images["animals"][name]:
        raise HTTPException(status_code=404, detail="No images found for this animal")

    # Select a random image and construct URL
    image_filename = choice(animal_images["animals"][name])
    image_url = f"{animal_images['baseUrl']}/{name}/{image_filename}"

    # Generate standard UTC timestamp in ISO 8601 format
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    return AnimalResponse(name=name, url=image_url, timestamp=timestamp)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Handle HTTP exceptions"""

    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle general exceptions"""

    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


if __name__ == "__main__":
    run(app, host=config["fastapi"]["host"], port=config["fastapi"]["port"])
