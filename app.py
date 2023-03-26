from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from config import ADMIN_PORT, API_PORT
from logger import logger
from routes.admin import router as admin_router
from routes.collections import router as collections_router
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:9000",
                   "http://localhost:5173",
                   "http://localhost:4173"],
    # for deployment and vite testing
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(admin_router)
app.include_router(collections_router)


@app.on_event("startup")
async def startup_event():
    logger.info("Server started")
    print("\t\033[94mPANBASE\033[0m")
    print(f"\tREST API: http://localhost:{API_PORT}/api")
    print(f"\tADMIN DASHBOARD: http://localhost:{ADMIN_PORT}/")
