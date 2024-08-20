import logging
from fastapi import FastAPI

from src.container import Container
from .adapter.inward.web.send_email import (
    user_email_request_controller,
    queue_email_request_controller,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()],
)


def create_app() -> FastAPI:
    container = Container()

    app = FastAPI()
    app.container = container  # type: ignore[attr-defined]
    app.include_router(user_email_request_controller.router)
    app.include_router(queue_email_request_controller.router)
    return app


app = create_app()
