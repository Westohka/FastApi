# Service for messages

from typing import List

from sqlalchemy.sql.functions import array_agg

from Utils import Database, DBCheckoutConnection
from Users import UserOutput

from .models import MessageOutputDB, MessageInput
from .tables import table, likes

# Create Message Class

class MessageService:
    # Get a list of message id`s on a page

    @classmethod
    async def list( cls, page: int, page_limit: int ) -> List[int]:
        await DBCheckoutConnection()

        query = table.select().with_only_columns( [table.c.id] ).offset( page_limit * page ).limit( page_limit )
        data = await Database.fetch_all( query )

        msg_list = []

        for msg in data:
            msg_list.append( msg.get( 'id' ) )

        return msg_list

    # Get info about message

    @classmethod
    async def info( cls, msg_id: int ) -> MessageOutputDB:
        await DBCheckoutConnection()

        query = table.select()\
            .with_only_columns( [table.c.id, table.c.usr_id, table.c.media, table.c.text, table.c.link, array_agg( likes.c.usr_id )] )\
            .select_from( table.join( likes, table.c.id == likes.c.msg_id, isouter = True ) )\
            .where( table.c.id == msg_id )\
            .group_by( table.c.id )

        data = await Database.fetch_one( query )

        if not data:
            raise RuntimeError( 'Message not find' )

        return MessageOutputDB( text = data.get( 'text' ),
                                media = data.get( 'media' ),
                                link = data.get( 'link' ),
                                usr_id = data.get( 'usr_id' ),
                                id = data.get( 'id' ),
                                likes = data.get( 'array_agg_1' ) )

    # Insert new message into blog

    @classmethod
    async def insert( cls, data: MessageInput, user: UserOutput ) -> MessageOutputDB:
        await DBCheckoutConnection()

        query = table.insert().values( text = data.text,
                                       media = data.media,
                                       link = data.link,
                                       usr_id = user.id )

        msg_id = await Database.execute( query )

        return MessageOutputDB( text = data.text,
                                media = data.media,
                                link = data.link,
                                usr_id = user.id,
                                id = msg_id,
                                likes = [] )

    # Delete message from blog

    @classmethod
    async def delete( cls, msg_id: int, user: UserOutput ) -> MessageOutputDB:
        await DBCheckoutConnection()

        query = table.select().where( table.c.id == msg_id )
        msg = await Database.fetch_one( query )

        if not msg:
            return msg

        if not msg.get( 'usr_id' ) == user.id:
            raise RuntimeError( 'Not permitted to delete this message' )

        query = table.delete().where( table.c.id == msg_id )
        await Database.execute( query )

        return MessageOutputDB( text = msg.get('text'),
                                media = msg.get( 'media' ),
                                link = msg.get( 'link' ),
                                usr_id = msg.get( 'usr_id' ),
                                id = msg.get( 'id' ),
                                likes = msg.get( 'likes' ) )

    # Like/unlike message. Return like status

    @classmethod
    async def like( cls, msg_id: int, user: UserOutput ) -> bool:
        await DBCheckoutConnection()

        query = table.select().where( table.c.id == msg_id )
        msg = await Database.fetch_one( query )

        if not msg:
            raise RuntimeError( 'Message not find' )

        query = likes.select().where( likes.c.msg_id == msg_id ).where( likes.c.usr_id == user.id )

        is_liked = await Database.fetch_one( query )

        if is_liked:
            query = likes.delete().where( likes.c.msg_id == msg_id ).where( likes.c.usr_id == user.id )
        else:
            query = likes.insert().values( msg_id = msg_id,
                                           usr_id = user.id )

        await Database.execute( query )
        return bool( not is_liked )