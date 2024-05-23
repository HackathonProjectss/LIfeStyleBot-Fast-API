from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

from core.config import init_db, settings
from core.logger import logger
from fastapi import Request
from api.router import router
from core.middlewares import AuthMiddleware

allowed_origins = [
    "http://localhost:3000",  # Assuming your frontend runs on localhost:3000
]

app = FastAPI(
    title="Life Style API",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=None,
)


@app.on_event("startup")
async def app_startup():
    try:
        await init_db()
    except Exception as e:
        logger.error(f"An error occurred while connecting to database: {e}")


@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": "An internal server error occurred"},
    )


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


app.include_router(router)
# Add CORSMiddleware to the application
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # List of allowed origins
    allow_credentials=True,  # Allow cookies to be included in cross-origin requests
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)
app.add_middleware(AuthMiddleware, allow_routes=["/", "/users", "/api/docs", "/api/openapi.json", "/robots.txt"])
