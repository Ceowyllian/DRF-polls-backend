from config.env import env

DATABASES = {"default": env.db(var="DB_URL")}
