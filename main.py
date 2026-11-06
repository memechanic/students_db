from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.database import engine, init_db
from app.log import log_requests
from app.routers import admin, auth, pages


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield
    engine.dispose()


app = FastAPI(lifespan=lifespan)

app.middleware("http")(log_requests)


app.include_router(auth.router)
app.include_router(pages.router)
app.include_router(admin.router)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/media", StaticFiles(directory="media"), name="media")


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(
    request: Request,
    exc: StarletteHTTPException,
):
    if exc.status_code == status.HTTP_401_UNAUTHORIZED:
        if request.headers.get("accept", "").startswith("application/json"):
            return JSONResponse(
                {"detail": exc.detail},
                status_code=exc.status_code,
            )
        return RedirectResponse("/login", status_code=status.HTTP_303_SEE_OTHER)

    if exc.status_code == status.HTTP_403_FORBIDDEN or exc.status_code == status.HTTP_404_NOT_FOUND:
        if request.headers.get("accept", "").startswith("application/json"):
            return JSONResponse(
                {"detail": exc.detail},
                status_code=exc.status_code,
            )
        return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)

    return JSONResponse(
        {"detail": exc.detail},
        status_code=exc.status_code,
    )
