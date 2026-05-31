from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_, and_
from typing import Optional, List, Dict, Any
from app.models.template import Template
from app.schemas.template import TemplateCreate, TemplateUpdate
from app.services.flyer_service import flyer_service
from sqlalchemy.dialects.postgresql import ARRAY

# Сервис для управления шаблонами
class TemplateService:
    # Предустановленные шаблоны
    PRESET_TEMPLATES = [
        {
            "name": "Рекламная листовка",
            "category": "advertising",
            "tags": ["реклама", "акция", "скидки"],
            "xml_content": '''<?xml version="1.0" encoding="UTF-8"?>
<flyer width="600" height="850" background="#f8f9fa" bgImage="" bgOpacity="100">
  <element type="text" id="t1" x="100" y="100" width="400" height="80" 
           content="СУПЕР АКЦИЯ!" font-family="Arial, sans-serif" font-size="48" 
           font-weight="bold" font-style="normal" color="#dc3545" align="center"/>
  <element type="text" id="t2" x="100" y="200" width="400" height="60" 
           content="Скидки до 50%" font-family="Arial, sans-serif" font-size="32" 
           font-weight="normal" font-style="italic" color="#495057" align="center"/>
</flyer>'''
        },
        {
            "name": "Приглашение",
            "category": "invitation",
            "tags": ["приглашение", "праздник", "мероприятие"],
            "xml_content": '''<?xml version="1.0" encoding="UTF-8"?>
<flyer width="600" height="850" background="#fff5f0" bgImage="" bgOpacity="100">
  <element type="text" id="t1" x="100" y="80" width="400" height="60" 
           content="ВЫ ПРИГЛАШЕНЫ" font-family="Georgia, serif" font-size="36" 
           font-weight="bold" font-style="normal" color="#e67e22" align="center"/>
  <element type="text" id="t2" x="100" y="160" width="400" height="200" 
           content="На вечеринку по случаю Нового года\n22 декабря в 19:00" 
           font-family="Georgia, serif" font-size="24" font-weight="normal" 
           font-style="italic" color="#7f8c8d" align="center"/>
</flyer>'''
        },
        {
            "name": "Объявление",
            "category": "announcement",
            "tags": ["объявление", "информация"],
            "xml_content": '''<?xml version="1.0" encoding="UTF-8"?>
<flyer width="600" height="850" background="#e8f4f8" bgImage="" bgOpacity="100">
  <element type="text" id="t1" x="50" y="50" width="500" height="50" 
           content="ОБЪЯВЛЕНИЕ" font-family="Arial, sans-serif" font-size="32" 
           font-weight="bold" font-style="normal" color="#2980b9" align="center"/>
  <element type="text" id="t2" x="50" y="120" width="500" height="400" 
           content="Пропала собака\nПорода: такса\nОкрас: рыжий\nКличка: Барон\n\nТел.: 8-999-123-45-67" 
           font-family="Arial, sans-serif" font-size="20" font-weight="normal" 
           font-style="normal" color="#2c3e50" align="left"/>
</flyer>'''
        },
        {
            "name": "Меню ресторана",
            "category": "menu",
            "tags": ["ресторан", "меню", "еда"],
            "xml_content": '''<?xml version="1.0" encoding="UTF-8"?>
<flyer width="600" height="850" background="#fff8e7" bgImage="" bgOpacity="100">
  <element type="text" id="t1" x="50" y="50" width="500" height="60" 
           content=" ДОБРО ПОЖАЛОВАТЬ " font-family="Georgia, serif" font-size="28" 
           font-weight="bold" font-style="normal" color="#e67e22" align="center"/>
  <element type="text" id="t2" x="50" y="120" width="500" height="300" 
           content="Специальное меню:\n\n1. Итальянская пицца - 450₽\n2. Цезарь с курицей - 380₽\n3. Том Ям с креветками - 520₽\n4. Чизкейк - 250₽\n\n Кофе в подарок к заказу!" 
           font-family="Arial, sans-serif" font-size="18" font-weight="normal" 
           font-style="normal" color="#2c3e50" align="left"/>
</flyer>'''
        },
        {
            "name": "Афиша концерта",
            "category": "event",
            "tags": ["концерт", "музыка", "мероприятие"],
            "xml_content": '''<?xml version="1.0" encoding="UTF-8"?>
<flyer width="600" height="850" background="#1a1a2e" bgImage="" bgOpacity="100">
  <element type="text" id="t1" x="50" y="100" width="500" height="80" 
           content="ROCK CONCERT" font-family="Impact, sans-serif" font-size="42" 
           font-weight="bold" font-style="normal" color="#e94560" align="center"/>
  <element type="text" id="t2" x="50" y="200" width="500" height="150" 
           content="THE BEST BAND\n\n15 марта в 20:00\n\nКлуб 'Космос'\n\nБилеты: 800-1200₽" 
           font-family="Arial, sans-serif" font-size="20" font-weight="normal" 
           font-style="normal" color="#ffffff" align="center"/>
</flyer>'''
        }
    ]
    
    # Инициализация предустановленных шаблонов при первом запуске
    @staticmethod
    async def initialize_preset_templates(db: AsyncSession) -> int:
        # Проверяем, есть ли уже пресеты
        result = await db.execute(select(Template).where(Template.is_preset == True))
        existing = result.scalars().all()
        if existing:
            return len(existing)
        # Добавляем пресеты
        added = 0
        for preset in TemplateService.PRESET_TEMPLATES:
            template = Template(name=preset["name"], xml_content=preset["xml_content"], is_preset=True, category=preset.get("category"), tags=preset.get("tags", []), usage_count=0)
            db.add(template)
            added += 1
        await db.commit()
        return added
    
    # Получение списка шаблонов с фильтрацией
    @staticmethod
    async def get_templates(db: AsyncSession, user_id: Optional[int] = None, category: Optional[str] = None, tags: Optional[List[str]] = None, include_preset: bool = True, skip: int = 0, limit: int = 50) -> tuple[List[Template], int]:
        conditions = []
        if include_preset:
            if user_id is not None:
                conditions.append(Template.user_id == user_id)
            if category:
                conditions.append(Template.category == category)
            if tags:
                # Поиск по тегам
                for tag in tags:
                    conditions.append(Template.tags.contains([tag]))
        else:
            if user_id is not None:
                conditions.append(and_(Template.user_id == user_id, Template.user_id.isnot(None)))
            if category:
                conditions.append(and_(Template.category == category, Template.user_id.isnot(None)))
            if tags:
                # Поиск по тегам
                for tag in tags:
                    conditions.append(and_(Template.tags.contains([tag]), Template.user_id.isnot(None)))
            if not conditions:
                conditions.append(Template.user_id.isnot(None))
        query = select(Template).where(and_(*conditions) if conditions else True)
        # Подсчет общего количества
        count_query = select(func.count()).select_from(Template).where(and_(*conditions) if conditions else True)
        total_result = await db.execute(count_query)
        total = total_result.scalar()
        # Пагинация и сортировка
        query = query.order_by(Template.usage_count.desc(), Template.created_at.desc())
        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        templates = result.scalars().all()
        return templates, total
    
    # Получение шаблона по ID
    @staticmethod
    async def get_template_by_id(db: AsyncSession, template_id: int) -> Optional[Template]:
        result = await db.execute(select(Template).where(Template.id == template_id))
        return result.scalar_one_or_none()
    
    # Создать новый шаблон
    @staticmethod
    async def create_template(db: AsyncSession, template_data: TemplateCreate, user_id: Optional[int] = None) -> Template:
        from app.models.template import Template
        template = Template(name=template_data.name, xml_content=template_data.xml_content, user_id=user_id, category=template_data.category, tags=template_data.tags, preview_url=template_data.preview_url, is_preset=False, usage_count=0)
        db.add(template)
        await db.commit()
        await db.refresh(template)
        return template
    
    # Обновить шаблон 
    @staticmethod
    async def update_template(db: AsyncSession, template_id: int, template_data: TemplateUpdate, user_id: Optional[int] = None) -> Optional[Template]:
        from app.models.template import Template
        template = await TemplateService.get_template_by_id(db, template_id)
        if not template:
            return None
        # Пресет нельзя обновить
        if template.is_preset:
            return None
        # Проверка владельца
        if template.user_id != user_id:
            return None
        update_data = template_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(template, field, value)
        await db.commit()
        await db.refresh(template)
        return template
    
    # Удалить шаблон (только свои)
    @staticmethod
    async def delete_template(db: AsyncSession, template_id: int, user_id: Optional[int] = None) -> bool:
        from app.models.template import Template
        template = await TemplateService.get_template_by_id(db, template_id)
        if not template:
            return False
        # Нельзя удалить пресет
        if template.is_preset:
            return False
        # Проверка владельца
        if template.user_id != user_id:
            return False
        await db.delete(template)
        await db.commit()
        return True
    
    # Увеличить счетчик использования шаблона
    @staticmethod
    async def increment_usage_count(db: AsyncSession, template_id: int):
        from app.models.template import Template
        template = await TemplateService.get_template_by_id(db, template_id)
        if template:
            template.usage_count += 1
            await db.commit()
    
    # Получить список всех категорий
    @staticmethod
    async def get_categories(db: AsyncSession) -> List[str]:
        from app.models.template import Template
        result = await db.execute(select(Template.category.distinct()).where(Template.category.isnot(None)))
        return [cat for cat in result.scalars().all() if cat]
    
    # Получить популярные теги
    @staticmethod
    async def get_popular_tags(db: AsyncSession, limit: int = 20) -> List[Dict[str, Any]]:
        from app.models.template import Template
        from sqlalchemy import func
        result = await db.execute(select(func.unnest(Template.tags).label('tag'), func.count().label('count')).where(Template.tags.isnot(None)).group_by('tag').order_by(func.count().desc()).limit(limit))
        return [{"tag": row[0], "count": row[1]} for row in result.fetchall()]

# Создаем экземпляр сервиса
template_service = TemplateService()
