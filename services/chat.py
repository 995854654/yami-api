from models.settings import Setting
from utils.logger import LoguruLogger
from sse_starlette import ServerSentEvent


class ChatService:
    def __init__(self, setting: Setting = None):
        self.setting = setting
        self.logger = LoguruLogger.get_logger()

    async def chat_simple_qa(self, context):
        self.logger.info("开始聊天")

        async for stream in self.setting.chat_model.astream_events(
                input=context,
                version="v1"
        ):
            event = stream["event"]
            if event == "on_chat_model_stream":
                yield ServerSentEvent(
                    event=event,
                    data=stream["data"]["chunk"].content
                )
