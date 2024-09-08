from typing import Optional
import os
from pathlib import Path
import errno
import yaml
from enum import Enum

# metastore
from sqlalchemy import create_engine, Engine
import pymysql

# langchain
from models.configuration import LLMConfiguration, LLMType
from langchain_openai import ChatOpenAI

pymysql.install_as_MySQLdb()


class MetaStoreType(str, Enum):
    MYSQL = "mysql"
    SQLITE = "sqlite"


class Setting:
    _settings: dict = {}

    metastore: Engine = None
    chat_model = None

    def __init__(self, config_path: Optional[str] = None):
        if config_path:
            self.load(config_path=config_path)

    def _set_metastore(self):
        storage_type = self._settings.get("metastore", {}).get("type", "")
        if storage_type == MetaStoreType.MYSQL:
            self.metastore = create_engine(
                self._settings.get("metastore", {}).get("connection_str"),
                pool_recycle=1500, pool_timeout=3600
            )
        elif storage_type == MetaStoreType.SQLITE:
            self.metastore = create_engine(
                self._settings.get("metastore", {}).get("connection_str"),
                connect_args={"check_same_thread": False}
            )

    def _set_llm(self, llm_type: LLMType = None, llm_param: LLMConfiguration = None, llm_key: str = None):

        _llm = self._settings.get("llm", {})
        llm_type = llm_type if llm_type else _llm.get("type")
        if llm_type == LLMType.MOONSHOT:
            self.chat_model = ChatOpenAI(
                openai_api_base=llm_param.endpoint if llm_param else _llm.get("endpoint"),
                openai_api_key=llm_key if llm_key else _llm.get("key"),
                model_name=llm_param.llm_model_name if llm_param else _llm.get("model_name"),
            )

    def load(self, config_path: Optional[str]):
        config_path = str(config_path)
        if not os.path.exists(config_path):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), config_path)

        _config = None
        with open(config_path, "r") as fp:
            _config = yaml.safe_load(fp)
        self._settings.update(_config)

        # load sub_setting file
        if _config.get("profile", {}).get("active", None) is not None:

            sub_config_path = config_path.replace("application", f"application-{_config['profile']['active']}")
            if not os.path.exists(sub_config_path):
                raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), sub_config_path)
            _sub_config = None
            with open(sub_config_path, "r") as fp:
                _sub_config = yaml.safe_load(fp)
            self._settings.update(_sub_config)

        self._settings = self.parse_env_var(self._settings)
        self._set_metastore()
        self._set_llm()

    def parse_env_var(self, value):
        if isinstance(value, dict):
            return {k: self.parse_env_var(v) for k, v in value.items()}
        elif isinstance(value, str) and value.startswith("${"):
            return os.environ.get(value[2:-1], "")
        elif isinstance(value, list):
            return [self.parse_env_var(c) for c in value]
        else:
            return value

    def get_settings(self):
        return self._settings


if __name__ == '__main__':
    cur_path = os.getcwd()
    configs_path = Path(cur_path + "/config/application.yml")
    setting = Setting(str(configs_path))
    print(setting)
    print(setting.metastore)
