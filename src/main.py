from fastapi import FastAPI

# from .adapter.inward.web import home
# from .adapter.inward.web.health import health
# from .adapter.inward.web.requisition import gws, plps

app = FastAPI()
# app.include_router(health.router)
# app.include_router(home.router)
# app.include_router(gws.router)
# app.include_router(plps.router)