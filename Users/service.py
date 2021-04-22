from Utils import Database, DBCheckoutConnection

from .tables import table
from .models import UserOutput, UserInput

# Create User Class


class UserService:
    # Get info about user

    @classmethod
    async def infoByLogin(cls, usr_login: str) -> UserOutput:
        await DBCheckoutConnection()

        query = table.select().where(table.c.login == usr_login)
        user = await Database.fetch_one(query)

        return UserOutput(id=user.get('id'),
                          login=user.get('login'),
                          password=user.get('password'))

    # Insert new message into blog

    @classmethod
    async def insert(cls, data: UserInput) -> UserOutput:
        await DBCheckoutConnection()

        query = table.insert().values(login=data.login, password=data.password)
        usr_id = await Database.execute(query)

        return UserOutput(login=data.login,
                          password=data.password,
                          id=usr_id)
