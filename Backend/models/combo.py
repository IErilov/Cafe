from typing import List, TYPE_CHECKING

from sqlalchemy import Integer, String, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

if TYPE_CHECKING:
    from models.menu import MenuItem


class ComboItem(Base):
    __tablename__ = "combo_items"
    __table_args__ = (
        UniqueConstraint("combo_id", "menu_item_id", name="uq_combo_item"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    combo_id: Mapped[int] = mapped_column(
        ForeignKey("combos.id", ondelete="CASCADE"), nullable=False
    )
    menu_item_id: Mapped[int] = mapped_column(
        ForeignKey("menu_items.id", ondelete="CASCADE"), nullable=False
    )
    quantity: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    combo: Mapped["Combo"] = relationship("Combo", back_populates="items")
    menu_item: Mapped["MenuItem"] = relationship("MenuItem")


class Combo(Base):
    __tablename__ = "combos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    price: Mapped[float] = mapped_column(nullable=False)  # или Numeric(10, 2)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    items: Mapped[List["ComboItem"]] = relationship(
        "ComboItem",
        back_populates="combo",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Combo(name='{self.name}', price={self.price})>"