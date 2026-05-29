import xml.etree.ElementTree as ET
from typing import Dict, Any, List, Tuple
from app.schemas.flyer_models import FlyerXML, FlyerTextElement, FlyerImageElement

# Сервис для работы с XML в формате flyer
class FlyerService:
    
    # Проверка валидности XML
    @staticmethod
    def validate_xml(xml_string: str) -> bool:
        try:
            root = ET.fromstring(xml_string)
            return root.tag == 'flyer'
        except ET.ParseError:
            return False
    
    # Парсинг XML в модель FlyerXML
    @staticmethod
    def parse_xml(xml_string: str) -> FlyerXML:
        root = ET.fromstring(xml_string)
        if root.tag != 'flyer':
            raise ValueError("Invalid XML format: root tag must be 'flyer'")
        # Извлекаем атрибуты корневого элемента
        flyer = FlyerXML(
            width=int(root.get('width', 600)),
            height=int(root.get('height', 850)),
            background=root.get('background', '#ffffff'),
            bg_image=root.get('bgImage', ''),
            bg_opacity=int(root.get('bgOpacity', 100)),
            elements=[])
        # Парсим элементы
        for element in root.findall('element'):
            elem_type = element.get('type')
            if elem_type == 'text':
                text_elem = FlyerTextElement(
                    id=element.get('id', ''),
                    x=int(element.get('x', 0)),
                    y=int(element.get('y', 0)),
                    width=int(element.get('width', 100)),
                    height=int(element.get('height', 50)),
                    content=element.get('content', ''),
                    font_family=element.get('font-family', 'Arial, sans-serif'),
                    font_size=int(element.get('font-size', 16)),
                    font_weight=element.get('font-weight', 'normal'),
                    font_style=element.get('font-style', 'normal'),
                    color=element.get('color', '#000000'),
                    align=element.get('align', 'left'))
                flyer.elements.append(text_elem)
            elif elem_type == 'image':
                img_elem = FlyerImageElement(
                    id=element.get('id', ''),
                    x=int(element.get('x', 0)),
                    y=int(element.get('y', 0)),
                    width=int(element.get('width', 100)),
                    height=int(element.get('height', 100)),
                    src=element.get('src', ''))
                flyer.elements.append(img_elem)
        return flyer
    
    # Преобразование модели в XML строку
    @staticmethod
    def to_xml(flyer: FlyerXML) -> str:
        # Корневой элемент
        root = ET.Element('flyer', {
            'width': str(flyer.width),
            'height': str(flyer.height),
            'background': flyer.background,
            'bgImage': flyer.bg_image or '',
            'bgOpacity': str(flyer.bg_opacity) })
        # Добавляем элементы
        for element in flyer.elements:
            if isinstance(element, FlyerTextElement):
                attrs = {
                    'type': 'text',
                    'id': element.id,
                    'x': str(element.x),
                    'y': str(element.y),
                    'width': str(element.width),
                    'height': str(element.height),
                    'content': element.content,
                    'font-family': element.font_family,
                    'font-size': str(element.font_size),
                    'font-weight': element.font_weight,
                    'font-style': element.font_style,
                    'color': element.color,
                    'align': element.align}
                ET.SubElement(root, 'element', attrs)
            elif isinstance(element, FlyerImageElement):
                attrs = {
                    'type': 'image',
                    'id': element.id,
                    'x': str(element.x),
                    'y': str(element.y),
                    'width': str(element.width),
                    'height': str(element.height),
                    'src': element.src}
                ET.SubElement(root, 'element', attrs)
        # Возвращаем отформатированный XML
        return ET.tostring(root, encoding='unicode', method='xml')
    
    # Извлечение размера страницы из XML
    @staticmethod
    def get_page_size(xml_string: str) -> Tuple[int, int]:
        try:
            root = ET.fromstring(xml_string)
            return ( int(root.get('width', 600)), int(root.get('height', 850)) )
        except:
            return 600, 850
    
    # Подсчет количества элементов
    @staticmethod
    def get_elements_count(xml_string: str) -> int:
        try:
            root = ET.fromstring(xml_string)
            return len(root.findall('element'))
        except:
            return 0
    
    # Генерация пустого шаблона
    @staticmethod
    def generate_empty_template(width: int = 600, height: int = 850, background: str = "#ffffff") -> str:
        return f'''<?xml version="1.0" encoding="UTF-8"?>
<flyer width="{width}" height="{height}" background="{background}" bgImage="" bgOpacity="100">
</flyer>'''

# Создаем экземпляр сервиса
flyer_service = FlyerService()
