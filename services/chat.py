from models.settings import Setting
from utils.logger import LoguruLogger
from sse_starlette import ServerSentEvent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage
from models.custom_request import QARequest
from models.common import ChatDirection, ChatMessage
from typing import List
from sqlalchemy.orm import Session
from models.db.chatbot import ChatHistory
from models.custom_response import ResMsg
import json
from uuid import uuid4


class ChatService:
    def __init__(self, setting: Setting = None):
        self.setting = setting
        self.logger = LoguruLogger.get_logger()

    async def chat_simple_qa(self, request: QARequest):
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
        chat_history = [
            AIMessage(content=history.context) if history.direction == ChatDirection.LEFT else HumanMessage(content=history.context)
            for history in request.history_list
        ]
        async for stream in executor.astream_events(
                input={
                    "question": request.context,
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

    def update_chat_history(self, db: Session, history_id, history_list: List[ChatMessage], user_id):
        self.logger.info("save history")
        # serialize
        chat_list = [item.json() for item in history_list]
        history = db.query(ChatHistory).filter(ChatHistory.history_id == history_id).first()
        if history:
            history.messages = json.dumps(chat_list, ensure_ascii=False)
        else:
            db.add(ChatHistory(
                history_id=history_id,
                user_id=user_id,
                history_name=chat_list[0]["context"],
                description=chat_list[-1]["context"],
                messages=json.dumps(chat_list, ensure_ascii=False)
            ))
        db.commit()
        return ResMsg()
