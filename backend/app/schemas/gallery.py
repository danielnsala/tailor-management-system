from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import GalleryItemType


class GalleryItemCreate(BaseModel):
    image_url: str = Field(
        min_length=1,
        max_length=500,
    )
    description: str
    item_type: GalleryItemType


class GalleryItemUpdate(BaseModel):
    image_url: str | None = None
    description: str | None = None
    item_type: GalleryItemType | None = None


class GalleryItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    image_url: str
    description: str
    item_type: GalleryItemType
    created_at: datetime