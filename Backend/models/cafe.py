from typing import List, TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

if TYPE_CHECKING:
    from models.menu import MenuCategory


class Cafe(Base):
    __tablename__ = "cafe"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    adress: Mapped[str] = mapped_column(String, nullable=False)

    menu_categories: Mapped[List["MenuCategory"]] = relationship(
        "MenuCategory",
        back_populates="cafe",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Cafe(name='{self.name}', adress='{self.adress}')>"