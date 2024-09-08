from fastapi import UploadFile
import aiofiles

class SingletonMeta(type):
    _instance = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instance:
            cls._instance[cls] = super().__call__(*args, **kwargs)
        return cls._instance[cls]


async def save_file(blob: UploadFile, file_path):
    async with aiofiles.open(file_path, "ab") as buffer:
        while True:
            chunk = await blob.read(1024)
            if not chunk:
                break
            await buffer.write(chunk)