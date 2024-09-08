from fastapi import APIRouter, UploadFile, WebSocket
from services.common import get_storage_service
from models.custom_response import ResMsg
from pathlib import Path
from utils.common import save_file
from utils.logger import LoguruLogger
from starlette.websockets import WebSocketDisconnect

file_router = APIRouter(
    tags=["upload"]
)


@file_router.post("/upload_file")
async def upload_file(blob: UploadFile):
    service = get_storage_service()
    file_save_path = str(Path(str(service.get_path()) + "/" + blob.filename))
    await save_file(blob, file_save_path)
    return ResMsg(msg="上传成功！！")


@file_router.post("/download_file")
async def download_file():
    pass


@file_router.websocket("/download_file_ws")
async def download_file_ws(websocket: WebSocket):
    logger = LoguruLogger.get_logger()
    await websocket.accept()
    logger.info("websocket连接成功！！")
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        logger.info("websocket断开连接")
