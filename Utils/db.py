# Connecting to database

from sqlalchemy import create_engine
import os

import databases

USER = 'postgres'
PASSWORD = 'password'
HOST = 'localhost' if os.environ.get( 'TEST_FLAG' ) else 'db'
PORT = '5432'
DB_NAME = 'database'

DATABASE_URL = f'postgresql://{ USER }:{ PASSWORD }@{ HOST }:{ PORT }/{ DB_NAME }'

database = databases.Database( DATABASE_URL )
engine = create_engine( DATABASE_URL )

async def checkoutConnection():
    if not database.is_connected:
        try:
            await database.connect()
        except:
            pass