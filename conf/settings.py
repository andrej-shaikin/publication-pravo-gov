import databases
import sqlalchemy
from environ import Env

env = Env()
env.read_env()

SYSTEM_CODENAME = env.str("SYSTEM_CODENAME", default="publication_pravo_gov")
DATABASE_DSN = env.str("DATABASE_DSN")
DEBUG = env.bool("DEBUG", default=False)
TIMEZONE = "UTC"

HTTP_PROXY = env.str("HTTP_PROXY", default="")
HTTPS_PROXY = env.str("HTTPS_PROXY", default="")

db = databases.Database(DATABASE_DSN)
db_meta = sqlalchemy.MetaData()

INSTALLED_APPS = (
    "document_types",
    "signatory_authority",
    "section",
)
