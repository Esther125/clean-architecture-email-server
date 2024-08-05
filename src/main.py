from fastapi import FastAPI
from .adapter.inward.web.send_email import send_email_controller

app = FastAPI()

app.include_router(send_email_controller.router)
