from sqladmin import ModelView

from models.cafe import Cafe
from models.menu import MenuCategory, MenuItem
from models.combo import Combo, ComboItem
from sqladmin_inline import InlineModelAdmin, ModelViewWithInlines
from User.model import User
from starlette.requests import Request

from wtforms import Form, PasswordField, StringField, IntegerField
from wtforms.validators import DataRequired, Optional
import bcrypt

class CafeAdmin(ModelView, model=Cafe):
    column_list = [Cafe.id, Cafe.name, Cafe.adress]
    column_searchable_list = [Cafe.name]
    column_sortable_list = [Cafe.id, Cafe.name]
    form_columns = [Cafe.name, Cafe.adress]
    icon = "fa-solid fa-utensils"
    name = "Кафе"
    name_plural = "Кафе"

class MenuCategoryAdmin(ModelView, model=MenuCategory):
    column_list = [MenuCategory.id, MenuCategory.name, MenuCategory.slug, MenuCategory.is_active, MenuCategory.cafe]
    column_searchable_list = [MenuCategory.name, MenuCategory.slug]
    form_columns = [MenuCategory.cafe, MenuCategory.name, MenuCategory.slug, MenuCategory.is_active]
    icon = "fa-solid fa-list"
    name = "Категория меню"
    name_plural = "Категории меню"

class MenuItemAdmin(ModelView, model=MenuItem):
    column_list = [MenuItem.id, MenuItem.title, MenuItem.category, MenuItem.parent, MenuItem.order, MenuItem.is_active]
    column_searchable_list = [MenuItem.title]
    form_columns = [MenuItem.category, MenuItem.parent, MenuItem.title, MenuItem.order, MenuItem.price, MenuItem.calories, MenuItem.Proteins, MenuItem.Fats, MenuItem.Carbs, MenuItem.is_active]
    icon = "fa-solid fa-bars"
    name = "Пункт меню"
    name_plural = "Пункты меню"

class ComboItemInline(InlineModelAdmin, model=ComboItem):
    inline_label = "Товары в комбо"
    column_list = [ComboItem.menu_item, ComboItem.quantity]
    column_searchable_list = [ComboItem.menu_item]
    form_columns = [ComboItem.menu_item, ComboItem.quantity]
    can_create = True
    can_delete = True

class ComboAdmin(ModelViewWithInlines, model=Combo):
    column_list = [Combo.id, Combo.name, Combo.price, Combo.is_active]
    column_searchable_list = [Combo.name]
    column_sortable_list = [Combo.id, Combo.name, Combo.price]
    form_columns = [Combo.name, Combo.description, Combo.price, Combo.is_active]
    inlines = [ComboItemInline]  # ключевая строка
    icon = "fa-solid fa-box-open"
    name = "Комбо"
    name_plural = "Комбо"


class ComboItemAdmin(ModelView, model=ComboItem):
    column_list = [
        ComboItem.id,
        ComboItem.combo,
        ComboItem.menu_item,
        ComboItem.quantity,
    ]
    form_columns = [
        ComboItem.combo,
        ComboItem.menu_item,
        ComboItem.quantity,
    ]
    icon = "fa-solid fa-link"
    name = "Состав комбо"
    name_plural = "Состав комбо"

class UserAdmin(ModelView, model=User):
    column_list = [
        User.id, 
        User.uname, 
        User.name, 
        User.sur_name, 
        User.yo
    ]
    column_searchable_list = [User.uname, User.name, User.sur_name]
    column_sortable_list = [User.id, User.uname, User.yo]
    
    icon = "fa-solid fa-users"
    name = "Пользователь"
    name_plural = "Пользователи"

    async def scaffold_form(self, rules: list | None = None) -> type[Form]:
        class UserForm(Form):
            uname = StringField("Имя пользователя (логин)", validators=[DataRequired()])
            password = PasswordField("Новый пароль") 
            name = StringField("Имя", validators=[DataRequired()])
            sub_name = StringField("Отчество", validators=[DataRequired()])
            sur_name = StringField("Фамилия", validators=[DataRequired()])
            yo = IntegerField("Возраст", validators=[DataRequired()])
            mass = IntegerField("Вес", validators=[DataRequired()])
            height = IntegerField("Рост", validators=[DataRequired()])
            desc = StringField("Описание", validators=[Optional()])
            
        return UserForm


    async def on_model_change(self, data: dict, model: User, is_created: bool, request: Request) -> None:
        if "password" in data and data["password"]:
            plain_password = data["password"]
            
            password_bytes = plain_password.encode('utf-8')
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(password_bytes, salt)
            
            model._password_hash = hashed.decode('utf-8')
            
        if "password" in data:
            del data["password"]
