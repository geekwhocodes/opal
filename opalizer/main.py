import logging
from typing import Any
from fastapi import Depends, FastAPI, Request, Response
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from opalizer.config import Settings, get_settings
from opalizer.core.logging import setup_logging
from opalizer.core.rate_limiter import limiter



log = logging.getLogger(__name__)
setup_logging()


def create_app() -> FastAPI:
    
    app = FastAPI(title="Opal")
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    return app

app = create_app()


@app.get("/ping")
@limiter.limit("1/second")
def get_ping(request:Request, response: Response) -> Any:
    return 1 

@app.on_event("startup")
async def startup_event():
    logging.info("Starting up...")


@app.on_event("shutdown")
async def shutdown_event():
    logging.info("Shutting down...")


#FastAPIInstrumentor.instrument_app(app=app)