import os

import environ

env = environ.Env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = environ.Path(__file__) - 2
env.read_env(os.path.join(BASE_DIR, ".env"))
env.read_env(env.str("ENV_PATH", ".env"))
