import logging
from fastapi import FastAPI

from src.container import Container
from .adapter.inward.web.send_email import send_email_controller

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()],
)


def create_app() -> FastAPI:
    container = Container()

    app = FastAPI()
    app.container = container  # type: ignore[attr-defined]
    app.include_router(send_email_controller.router)
    return app


app = create_app()
