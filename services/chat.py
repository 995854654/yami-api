from models.settings import Setting
from utils.logger import LoguruLogger
from sse_starlette import ServerSentEvent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


class ChatService:
    def __init__(self, setting: Setting = None):
        self.setting = setting
        self.logger = LoguruLogger.get_logger()

    async def chat_simple_qa(self, context):
        self.logger.info("开始聊天")
        prompt = ChatPromptTemplate.from_messages([
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{question}"),
        ])
        executor = (
                {
                    "question": lambda x: x["question"],
                    "chat_history": lambda x: x["chat_history"]
                }
                | prompt
                | self.setting.chat_model
        )
        chat_history = []
        async for stream in executor.astream_events(
                input={
                    "question": context,
                    "chat_history": chat_history
                },
                version="v1"
        ):
            event = stream["event"]
            if event == "on_chat_model_stream":
                yield ServerSentEvent(
                    event=event,
                    data=stream["data"]["chunk"].content
                )
