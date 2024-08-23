import logging
from typing import Optional
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


class CustomFastAPI(FastAPI):
    container: Optional[Container] = None


def create_app() -> CustomFastAPI:
    container = Container()

    app = CustomFastAPI()
    app.container = container
    app.include_router(user_email_request_controller.router)
    app.include_router(queue_email_request_controller.router)
    return app


app = create_app()
