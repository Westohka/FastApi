# RestApi for working with messages

from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from fastapi.responses import FileResponse

from typing import List

import logging

from Utils import LinkPreview, FileManager
from Users import TokenController, UserOutput

from .service import MessageService
from .models import Link, MessageOutput, MessageInput

router = APIRouter()

# Request info link if we can


async def getLinkInfo(url) -> Link:
    link = Link(link=url)

    if url:
        preview = LinkPreview(url)
        await preview.requestPreview()

        link.title = preview.title
        link.description = preview.description
        link.image = preview.image

    return link


@router.get('/msg/{msg_id}', response_model=MessageOutput, tags=["Messages"])
async def message(msg_id: int) -> MessageOutput:
    try:
        result = await MessageService.info(msg_id)
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=404, detail="Message not find")

    return result


@router.get('/msg', response_model=List[int], tags=["Messages"])
async def messages(page: int = 0, page_limit: int = 2) -> List[int]:
    msgs = await MessageService.list(page, page_limit)
    return msgs


@router.post('/msg', response_model=MessageOutput, tags=["Messages"])
async def getMessage(text: str = Form(""),
                     link: str = Form(""),
                     files: List[UploadFile] = File([]),
                     user: UserOutput = Depends(
                         TokenController.get_current_user))\
        -> MessageOutput:
    if len(files) == 0 and link == "" and text == "":
        raise HTTPException(status_code=404, detail="Message can`t be empty")

    media = []

    for file in files:
        if not file.content_type == 'video/mp4'\
                and not file.content_type == 'image/png':
            raise HTTPException(status_code=404,
                                detail="Media data don`t supported")

        media.append(await FileManager.save(file))

    msg = await MessageService.insert(MessageInput(text=text,
                                                   link=link,
                                                   media=media), user)

    return msg


@router.delete('/msg/{blog_id}', response_model=bool, tags=["Messages"])
async def delete(msg_id: int,
                 user: UserOutput = Depends(TokenController.get_current_user))\
        -> bool:
    try:
        msg = await MessageService.delete(msg_id, user)

        for file in msg.media:
            await FileManager.remove(file)
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=403,
                            detail="Not permitted to delete this message")

    return True


@router.get('/msg_like/{blog_id}', response_model=bool, tags=["Messages"])
async def like(msg_id: int,
               user: UserOutput = Depends(TokenController.get_current_user))\
        -> bool:
    try:
        status = await MessageService.like(msg_id, user)
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=404, detail="Message not find")

    return status


@router.get('/media', tags=["Messages"])
async def getMedia(file: str) -> File:
    return FileResponse(FileManager.storagePath() + '/' + file)


@router.get('/link', response_model=Link, tags=["Messages"])
async def linkInfo(link: str) -> Link:
    try:
        info = await getLinkInfo(link)
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=404,
                            detail="Get link info finished with error")

    return info
