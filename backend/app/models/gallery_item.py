from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Enum as SQLEnum
from app.models.enums import GalleryItemType

from app.database import Base


class GalleryItem(Base):
    __tablename__ = "gallery_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    image_url: Mapped[str] = mapped_column(
        String(500),
        unique=True,
        nullable=False)

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False)

    item_type: Mapped[GalleryItemType] = mapped_column(
    SQLEnum(GalleryItemType, name="gallery_item_type"),
    nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False)