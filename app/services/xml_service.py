import xml.etree.ElementTree as ET
import xmltodict
from typing import Dict, Any

#Проверяет, является ли строка валидным XML
def validate_xml(xml_string: str) -> bool:
    try:
        ET.fromstring(xml_string)
        return True
    except ET.ParseError as e:
        print(f"XML parsing error: {e}")
        return False

#Преобразует XML в словарь Python
def parse_xml_to_dict(xml_string: str) -> Dict[str, Any]:
    try:
        return xmltodict.parse(xml_string)
    except Exception as e:
        raise ValueError(f"Failed to parse XML: {e}")

#Преобразует словарь в XML строку
def dict_to_xml(data: Dict[str, Any]) -> str:
    try:
        return xmltodict.unparse(data, pretty=True)
    except Exception as e:
        raise ValueError(f"Failed to convert dict to XML: {e}")

#Извлекает размер страницы из XML-шаблона
def get_page_size_from_xml(xml_string: str) -> tuple:
    try:
        root = ET.fromstring(xml_string)
        page = root.find('page')
        if page is not None:
            width = int(page.get('width', 800))
            height = int(page.get('height', 600))
            return width, height
    except:
        pass
    return 800, 600