from environ import Env

env = Env()
env.read_env()

DATABASE_DSN = env.str("DATABASE_DSN")
DEBUG = env.bool("DEBUG", default=False)
TIMEZONE = "UTC"

HTTP_PROXY = env.str("HTTP_PROXY", default="")
HTTPS_PROXY = env.str("HTTPS_PROXY", default="")

INSTALLED_APPS = (
  "document_types",
  "signatory_authority",
  "section",
)
