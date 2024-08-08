from fastapi import FastAPI

from src.container import Container
from .adapter.inward.web.send_email import send_email_controller


def create_app() -> FastAPI:
    container = Container()

    app = FastAPI()
    app.container = container
    app.include_router(send_email_controller.router)
    return app


app = create_app()
