"""
This file is an example for the sake of completeness, meant to be removed.
"""

from sqlalchemy import JSON, Integer
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel, TimestampMixin


class LogModel(BaseModel, TimestampMixin):
    __tablename__ = "log"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    data: Mapped[dict | None] = mapped_column(JSON, nullable=True)
