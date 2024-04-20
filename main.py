from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import uvicorn
from pathlib import Path
from utils.logger import LoguruLogger

# 路由
from routes.home import home_router

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

app.include_router(home_router)

if __name__ == '__main__':
    # workers = os.cpu_count()
    workers = 2
    uvicorn.run(
        "main:app",
        host=os.environ.get("HOST", "127.0.0.1"),
        port=int(os.environ.get("PORT", 8443)),
        workers=workers
    )
