from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from xml.etree import ElementTree as ET

# Текстовый элемент
class FlyerTextElement(BaseModel):
    id: str
    type: Literal["text"] = "text"
    x: int
    y: int
    width: int
    height: int
    content: str
    font_family: str = Field(default="Arial, sans-serif", alias="font-family")
    font_size: int = Field(default=16, alias="font-size")
    font_weight: str = Field(default="normal", alias="font-weight")
    font_style: str = Field(default="normal", alias="font-style")
    color: str = "#000000"
    align: str = "left"

# Элемент изображения
class FlyerImageElement(BaseModel):
    id: str
    type: Literal["image"] = "image"
    x: int
    y: int
    width: int
    height: int
    src: str

# Корневая модель flyer
class FlyerXML(BaseModel):
    width: int
    height: int
    background: str = "#ffffff"
    bg_image: Optional[str] = Field(default="", alias="bgImage")
    bg_opacity: int = Field(default=100, alias="bgOpacity")
    elements: List[FlyerTextElement | FlyerImageElement] = []
    class Config:
        populate_by_name = True  # позволяет использовать alias
