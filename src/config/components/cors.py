from corsheaders.defaults import default_headers

from config.env import env

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = default_headers + ("cache-control", "cookies")
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS", default=[])
