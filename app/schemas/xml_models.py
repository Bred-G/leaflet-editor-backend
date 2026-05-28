from pydantic import BaseModel, Field
from typing import List, Optional, Union, Literal
from enum import Enum

class Orientation(str, Enum):
    portrait = "portrait"
    landscape = "landscape"

class UnitType(str, Enum):
    px = "px"
    mm = "mm"
    pt = "pt"

class BackgroundType(str, Enum):
    color = "color"
    gradient = "gradient"
    image = "image"

class GradientType(str, Enum):
    linear = "linear"
    radial = "radial"

class FitType(str, Enum):
    contain = "contain"
    cover = "cover"
    fill = "fill"

class ShapeType(str, Enum):
    rectangle = "rectangle"
    circle = "circle"
    line = "line"
    ellipse = "ellipse"
    polygon = "polygon"

class Position(BaseModel):
    x: int = 0
    y: int = 0

class Size(BaseModel):
    width: Union[int, str] = 100  # может быть "auto"
    height: Union[int, str] = 100

class Point(BaseModel):
    x: int
    y: int

class Color(BaseModel):
    value: str = "#000000"
    opacity: float = 1.0

class GradientStop(BaseModel):
    offset: str  # "0%", "50%", "100%"
    color: str
    opacity: float = 1.0

class TextStyle(BaseModel):
    fontFamily: str = "Arial"
    fontSize: int = 14
    fontWeight: Literal["normal", "bold", "100", "200", "300", "400", "500", "600", "700", "800", "900"] = "normal"
    fontStyle: Literal["normal", "italic", "oblique"] = "normal"
    color: str = "#000000"
    textAlign: Literal["left", "center", "right", "justify"] = "left"
    lineHeight: float = 1.2
    letterSpacing: int = 0
    opacity: float = 1.0

class Shadow(BaseModel):
    blur: int = 0
    offsetX: int = 0
    offsetY: int = 0
    color: str = "rgba(0,0,0,0.3)"

class Stroke(BaseModel):
    width: int = 1
    color: str = "#000000"
    dashArray: Optional[str] = None

class Border(BaseModel):
    radius: int = 0
    width: int = 1
    color: str = "#CCCCCC"

class Fill(BaseModel):
    type: Literal["color", "gradient"] = "color"
    value: Union[str, List[GradientStop]] = "#FFFFFF"
    gradientType: Optional[GradientType] = None
    angle: Optional[int] = None

class BaseElement(BaseModel):
    id: str
    zIndex: int = 0
    position: Position = Field(default_factory=Position)
    size: Optional[Size] = None
    opacity: float = 1.0
    visible: bool = True
    locked: bool = False
    rotate: int = 0

class TextElement(BaseElement):
    type: Literal["text"] = "text"
    content: str
    style: Optional[TextStyle] = None
    shadow: Optional[Shadow] = None
    stroke: Optional[Stroke] = None
    styleRef: Optional[str] = None  # ссылка на глобальный стиль

class ImageElement(BaseElement):
    type: Literal["image"] = "image"
    source: dict  # {type: "url" или "upload", data: ...}
    fit: FitType = FitType.contain
    border: Optional[Border] = None

class ShapeElement(BaseElement):
    type: Literal["shape"] = "shape"
    shapeType: ShapeType
    points: Optional[List[Point]] = None  # для polygon
    fill: Optional[Fill] = None
    stroke: Optional[Stroke] = None

class GroupElement(BaseModel):
    type: Literal["group"] = "group"
    id: str
    zIndex: int = 0
    position: Position = Field(default_factory=Position)
    elements: List[Union[TextElement, ImageElement, ShapeElement]]

class PageBackground(BaseModel):
    type: BackgroundType
    value: str  # цвет или url изображения
    gradientType: Optional[GradientType] = None
    angle: Optional[int] = None
    stops: Optional[List[GradientStop]] = None
    opacity: float = 1.0

class Page(BaseModel):
    width: int = 800
    height: int = 600
    orientation: Orientation = Orientation.portrait
    unit: UnitType = UnitType.px
    background: Optional[PageBackground] = None

class GlobalStyle(BaseModel):
    name: str
    style: TextStyle

class Grid(BaseModel):
    enabled: bool = False
    cellSize: int = 10
    visible: bool = True
    color: str = "#CCCCCC"

class Snap(BaseModel):
    enabled: bool = True
    threshold: int = 5

class Rulers(BaseModel):
    enabled: bool = False
    unit: UnitType = UnitType.px

class Guidelines(BaseModel):
    grid: Grid = Field(default_factory=Grid)
    snap: Snap = Field(default_factory=Snap)
    rulers: Rulers = Field(default_factory=Rulers)

class LeafletTemplate(BaseModel):
    version: str = "1.0"
    page: Page
    styles: Optional[List[GlobalStyle]] = None
    elements: List[Union[TextElement, ImageElement, ShapeElement, GroupElement]]
    guidelines: Optional[Guidelines] = None