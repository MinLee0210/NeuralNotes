from typing import Optional
from pydantic import BaseModel
from beanie import Document

class AttributePiece(BaseModel):
    polyph: list[int]
    rythm: list[int]

class ContentPiece(BaseModel):
    name: Optional[int| str]
    bar_pos: list
    content: list[dict]

class DataPiece(Document):
    dataset: Optional[str]
    version: Optional[str]
    content: ContentPiece
    attr_cls: AttributePiece

    class Settings:
        name = 'dataset'