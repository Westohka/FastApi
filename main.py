from fastapi import FastAPI
import os

from Utils import Database, FileManager, DBCheckoutConnection

from Messages import MessagesRouter
from Users import UsersRouter

app = FastAPI()
app.include_router( MessagesRouter )
app.include_router( UsersRouter )

# Create storage path

application_path = os.path.dirname( os.path.abspath( __file__ ) )

if not os.path.exists( application_path + '/media' ):
    os.makedirs( application_path + '/media' )

FileManager.setStoragePath( application_path + '/media' )

# Application events for connecting to database

@app.on_event( "startup" )
async def startup():
    await DBCheckoutConnection()

@app.on_event( "shutdown" )
async def shutdown():
    await Database.disconnect()