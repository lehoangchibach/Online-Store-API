from sqlalchemy import Integer, VARCHAR, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel, TimestampMixin


class CategoryModel(BaseModel, TimestampMixin):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(255), nullable=False, unique=True)
    creator_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
