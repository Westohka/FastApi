from fastapi import UploadFile

import aiofiles
import os
import random
import string


class FileManager:
    __storage_path: os.path.dirname(__file__)

    @classmethod
    async def save(cls, file: UploadFile):
        file_type = '.mp4' if file.content_type == 'video/mp4' else '.png'
        filename = ''.join(random.choices(string.ascii_uppercase
                                          + string.digits, k=10)) + file_type
        output_file = cls.__storage_path + '/' + filename

        async with aiofiles.open(output_file, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)

        return filename

    @classmethod
    async def remove(cls, file: str):
        await aiofiles.os.remove(cls.__storage_path + '/' + file)

    @classmethod
    def setStoragePath(cls, path):
        cls.__storage_path = path

    @classmethod
    def storagePath(cls) -> str:
        return cls.__storage_path
