from sqlalchemy import Integer, VARCHAR, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel, TimestampMixin


class ItemModel(BaseModel, TimestampMixin):
    __tablename__ = "item"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(255), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(VARCHAR(1024), nullable=False)
    creator_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"), nullable=False)
