from sqlalchemy import Integer, VARCHAR, CHAR
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel, TimestampMixin


class UserModel(BaseModel, TimestampMixin):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(VARCHAR(320), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(CHAR(60), nullable=False)
