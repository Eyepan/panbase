import sys


LOG_LEVEL = "DEBUG" if '--debug' in sys.argv else "CRITICAL"
API_PORT = 8000
ADMIN_PORT = 9000
RELOAD = True if '--reload' in sys.argv else False
