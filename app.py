from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware  # middleware helper

from conf import settings

app = FastAPI(debug=settings.DEBUG)

app.add_middleware(DBSessionMiddleware, db_url=settings.DATABASE_DSN)
