from typing import List, Optional, TYPE_CHECKING

from sqlalchemy import Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

if TYPE_CHECKING:
    from models.cafe import Cafe


class MenuCategory(Base):
    __tablename__ = 'menu_categories'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    cafe_id: Mapped[int] = mapped_column(
        ForeignKey("cafe.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    slug: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    cafe: Mapped["Cafe"] = relationship("Cafe", back_populates="menu_categories")

    items: Mapped[List["MenuItem"]] = relationship(
        "MenuItem",
        back_populates="category",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<MenuCategory(name='{self.name}', slug='{self.slug}')>"


class MenuItem(Base):
    __tablename__ = 'menu_items'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    category_id: Mapped[int] = mapped_column(
        ForeignKey('menu_categories.id', ondelete="CASCADE"), nullable=False
    )
    parent_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey('menu_items.id', ondelete="CASCADE"), nullable=True
    )

    title: Mapped[str] = mapped_column(String(100), nullable=False)
    order: Mapped[str] = mapped_column(String(100), default="NOT ORDER")
    price: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    calories: Mapped[str] = mapped_column(String(20), default="0")
    Proteins: Mapped[int] = mapped_column(Integer, default=0)
    Fats: Mapped[int] = mapped_column(Integer, default=0)
    Carbs: Mapped[int] = mapped_column(Integer, default=0)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    category: Mapped["MenuCategory"] = relationship("MenuCategory", back_populates="items")
    parent: Mapped[Optional["MenuItem"]] = relationship(
        "MenuItem", remote_side=[id], back_populates="children"
    )

    children: Mapped[List["MenuItem"]] = relationship(
        "MenuItem",
        back_populates="parent",
        order_by="MenuItem.order",
    )

    def __repr__(self) -> str:
        return f"<MenuItem(title='{self.title}')>"