import sys
import uvicorn
from database import db
from app import app
from config import ADMIN_PORT, API_PORT, LOG_LEVEL, RELOAD
from logger import logger


if __name__ == "__main__":
    if '--init' in sys.argv:    # init database and then exit. because my build command would like me to just init the database with the necessary tables and then exit
        exit()
    logger.info(f"Admin server started on port {ADMIN_PORT}")
    uvicorn.run("app:app" if RELOAD else app, host="0.0.0.0",
                port=API_PORT, log_level=LOG_LEVEL.lower(), reload=RELOAD)
    logger.info(f"Admin server stopped on port {ADMIN_PORT}")
