from models.settings import Setting
from pathlib import Path
from abc import abstractmethod
import os


class BaseStorage:
    @abstractmethod
    def get_path(self) -> str:
        pass


class LocalStorageService(BaseStorage):
    def __init__(self, settings: Setting):
        self.settings = settings

    def get_path(self) -> str:
        _setting = self.settings.get_settings()
        filepath = _setting.get("storage", {}).get("addr")
        if not filepath:
            raise FileNotFoundError("配置文件缺少storage.addr")
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        return filepath
