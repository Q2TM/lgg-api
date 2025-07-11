from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import router_v1
from repositories.lakeshore import LakeshoreRepository as ls
from mocks.model240 import MockModel240


app = FastAPI(
    title="Lakeshore Model240 API",
    description="API for Lakeshore Model240 temperature controller",
    version="1.0.0",
    lifespan=ls.lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router_v1)

ls.device = MockModel240()

if __name__ == "__main__":
    import uvicorn
    # uvicorn.run("main:app", host="0.0.0.0", port=8000, workers=4)
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)