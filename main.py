import threading

import uvicorn

from app import app
from config import ADMIN_PORT, API_PORT, LOG_LEVEL, RELOAD
from logger import logger
from server import serve_admin

server_thread = threading.Thread(target=serve_admin, daemon=True)

if __name__ == "__main__":
    server_thread.start()
    logger.info(f"Admin server started on port {ADMIN_PORT}")
    uvicorn.run("app:app" if RELOAD else app, host="0.0.0.0", port=API_PORT,
                log_level=LOG_LEVEL.lower(), reload=RELOAD)
    logger.info(f"Admin server stopped on port {ADMIN_PORT}")
