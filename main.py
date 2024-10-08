from fastapi import FastAPI, HTTPException,status
from fastapi.middleware.cors import CORSMiddleware
from models.custom_response import ResMsg
from utils.exception import ValidateException
from fastapi.responses import JSONResponse
import os
import uvicorn
from pathlib import Path
from utils.logger import LoguruLogger
from starlette.staticfiles import StaticFiles
from dotenv import load_dotenv
# 路由
from routes.home import home_router
from routes.security import security_router
from routes.chat import chat_router
from routes.file import file_router
from routes.resource import resource_router
import warnings
warnings.filterwarnings("ignore")
load_dotenv()

PROJECT_ROOT_PATH = os.path.dirname(os.path.abspath(__name__))
logging_config_path = Path(PROJECT_ROOT_PATH + "/config/logging.json")
logger = LoguruLogger.make_logger(logging_config_path, request_id="yami-api")

origin = ["*"]

app = FastAPI(debug=os.environ.get("DEBUG", False), version="0.0.1")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# 将OpenAI docs代码接管到本地中
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(home_router)
app.include_router(security_router)
app.include_router(chat_router)
app.include_router(file_router)
app.include_router(resource_router)


@app.exception_handler(HTTPException)
async def http_exception_handler(_, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content=ResMsg(success=False, msg=exc.detail, code=exc.status_code).dict()
    )

@app.exception_handler(ValidateException)
async def validate_exception_handler(_, exc):
    return JSONResponse(
        status_code=status.HTTP_422_VALIDATE_FAIL,
        content=ResMsg(success=False, msg=exc.name, code=status.HTTP_422_VALIDATE_FAIL).dict()
    )

if __name__ == '__main__':
    # workers = os.cpu_count()
    workers = 2
    uvicorn.run(
        "main:app",
        host=os.environ.get("HOST", "127.0.0.1"),
        port=int(os.environ.get("PORT", 8443)),
        workers=workers
    )
