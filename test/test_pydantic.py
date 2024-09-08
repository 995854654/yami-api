from pydantic import BaseModel, field_validator
from langchain_core.documents.base import Document
from typing import Union, Optional


class Document1(BaseModel):
    page_content: str = None


class SummaryDataModel(BaseModel):
    data: Union[Document1] = None


if __name__ == '__main__':
    doc = Document1(page_content="ss")
    s = SummaryDataModel(data=doc)
    print(s)
