from sqlalchemy import Integer, String, MetaData
from sqlalchemy.schema import Table, Column

from Utils.db import engine

metadata = MetaData()

# Create Messages Table

table = Table('users',
              metadata,
              Column('id', Integer, primary_key=True, index=True),
              Column('login', String),
              Column('password', String))

metadata.create_all(engine)
