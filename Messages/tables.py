from sqlalchemy import Integer, String, ARRAY, MetaData
from sqlalchemy.schema import Table, Column, ForeignKey

from Utils import DatabaseEngine
from Users import UserTable

metadata = MetaData()

# Create Messages Table

table = Table( 'messages',
                metadata,
                Column( 'id', Integer, primary_key = True, index = True ),
                Column( 'usr_id', Integer, ForeignKey( UserTable.c.id, onupdate = "CASCADE", ondelete = "CASCADE" ) ),
                Column( 'text', String ),
                Column( 'media', ARRAY( String ) ),
                Column( 'link', String ) )

# Relationship table with users likes

likes = Table( 'messages_likes_users',
               metadata,
               Column( 'msg_id', Integer, ForeignKey( table.c.id, onupdate = "CASCADE", ondelete = "CASCADE" ), primary_key = True ),
               Column( 'usr_id', Integer , ForeignKey( UserTable.c.id, onupdate = "CASCADE", ondelete = "CASCADE" ), primary_key = True ) )

metadata.create_all( DatabaseEngine )