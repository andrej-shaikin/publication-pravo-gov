from environ import Env

env = Env()
env.read_env()

DATABASE_DSN = env.str("DATABASE_DSN")
DEBUG = env.bool("DEBUG", default=False)
TIMEZONE = "UTC"
