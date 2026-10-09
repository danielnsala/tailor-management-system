from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.gallery_item import GalleryItem
from app.schemas.gallery import GalleryItemCreate, GalleryItemUpdate


class DuplicateGalleryImageError(Exception):
    pass


class GalleryService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_gallery_item(
        self,
        gallery_create: GalleryItemCreate,
    ) -> GalleryItem:

        gallery_item = GalleryItem(
            **gallery_create.model_dump()
        )

        self.db_session.add(gallery_item)

        try:
            self.db_session.commit()
        except IntegrityError:
            self.db_session.rollback()
            raise DuplicateGalleryImageError(
                "An image with this URL already exists"
            )

        self.db_session.refresh(gallery_item)

        return gallery_item

    def get_gallery_items(self) -> list[GalleryItem]:
        return self.db_session.execute(
            select(GalleryItem).order_by(
                GalleryItem.created_at.desc(),
                GalleryItem.id.desc(),
            )
        ).scalars().all()

    def get_gallery_item(
        self,
        item_id: int,
    ) -> GalleryItem | None:

        return self.db_session.get(GalleryItem, item_id)

    def update_gallery_item(
        self,
        item_id: int,
        gallery_update: GalleryItemUpdate,
    ) -> GalleryItem | None:

        gallery_item = self.get_gallery_item(item_id)

        if gallery_item is None:
            return None

        update_data = gallery_update.model_dump(
            exclude_unset=True,
            exclude_none=True,
        )

        for field, value in update_data.items():
            setattr(gallery_item, field, value)

        try:
            self.db_session.commit()
        except IntegrityError:
            self.db_session.rollback()
            raise DuplicateGalleryImageError(
                "An image with this URL already exists"
            )

        self.db_session.refresh(gallery_item)

        return gallery_item

    def delete_gallery_item(
        self,
        item_id: int,
    ) -> bool:

        gallery_item = self.get_gallery_item(item_id)

        if gallery_item is None:
            return False

        self.db_session.delete(gallery_item)
        self.db_session.commit()

        return True