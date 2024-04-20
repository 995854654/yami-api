import logging
from pathlib import Path
import json
from loguru import logger
from utils.common import SingletonMeta
import sys

class InterceptHandler(logging.Handler):
    def __init__(self,request_id):
        super().__init__()
        self.request_id = request_id

    def emit(self, record: logging.LogRecord) -> None:
        try:
            level = logger.level(record.levelname).name
        except AttributeError:
            level = str(record.levelno)

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1
        log = logger.bind(request_id=self.request_id)
        log.opt(
            depth=depth,
            exception=record.exc_info
        ).log(level, record.getMessage())

class LoguruLogger(metaclass=SingletonMeta):
    _logger = None

    @classmethod
    def make_logger(cls, config_path: Path, request_id: str = "unknown-service"):
        config = cls.load_logging_config(config_path)
        if config is None:
            return None
        log_config: dict = config.get("logger", {})
        log_path = log_config.get("path", "")
        file_path = log_path + "/" + log_config.get("filename", "")
        logger_object = cls.get_logger(
            file_path,
            level=log_config.get("level"),
            retention=log_config.get("retention"),
            rotation=log_config.get("rotation"),
            formats=log_config.get("format"),
            request_id=request_id
        )
        if cls._logger is None:
            cls._logger = logger_object
        return logger_object

    @classmethod
    def get_logger(cls, filepath: Path, level: str, retention: str, rotation: str, formats: str,
                   request_id: str = "unknown-service"):
        """
        :param filepath: 日志输出路径
        :param level: 日志等级
        :param retention: 日志保留时间
        :param rotation: 日志分割，比如 1 days, 每天分割一个日志，不会堆积在一个日志文件中
        :param formats: 日志输出格式
        :param request_id: 项目id
        :return: Logger
        """
        logger.remove()
        # enqueue 加入消息队列，保证日志的完整性
        # backtrace 回溯
        logger.add(sys.stdout, enqueue=True, backtrace=True, level=level.upper(), format=formats)
        logger.add(str(filepath), encoding="utf-8", rotation=rotation, retention=retention, enqueue=True,
                   backtrace=True, level=level.upper(), format=formats)
        # 将fastAPI的日志添加到loguru中
        LOGGER_NAMES = ["uvicorn", "uvicorn.error", "fastapi", "uvicorn.asgi", "uvicorn.access"]
        logging.getLogger().handlers = [InterceptHandler(request_id=request_id)]
        for log_name in LOGGER_NAMES:
            __logger = logging.getLogger(log_name)
            __logger.handlers = [InterceptHandler(request_id=request_id)]

        return logger.bind(request_id=request_id)

    @classmethod
    def load_logging_config(cls, config_path: Path):
        config = None
        try:
            with open(config_path) as fp:
                config = json.load(fp)
        except Exception as error:
            logger.error("load logging config error!!")
        finally:
            return config
