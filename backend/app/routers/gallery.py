from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.gallery import (
    GalleryItemCreate,
    GalleryItemUpdate,
    GalleryItemResponse,
)
from app.services.gallery_service import (
    GalleryService,
    DuplicateGalleryImageError,
)

from app.core.dependencies import get_current_admin

router = APIRouter(
    prefix="/gallery",
    tags=["Gallery"],
)


@router.post(
    "/",
    response_model=GalleryItemResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_admin)],
)
def create_gallery_item(
    gallery_create: GalleryItemCreate,
    db: Session = Depends(get_db),
):
    service = GalleryService(db)

    try:
        return service.create_gallery_item(gallery_create)
    except DuplicateGalleryImageError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc


@router.get("/", response_model=list[GalleryItemResponse])
def get_gallery_items(db: Session = Depends(get_db)):
    service = GalleryService(db)
    return service.get_gallery_items()


@router.get("/{item_id}", response_model=GalleryItemResponse)
def get_gallery_item(
    item_id: int,
    db: Session = Depends(get_db),
):
    service = GalleryService(db)
    gallery_item = service.get_gallery_item(item_id)

    if gallery_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gallery item not found",
        )

    return gallery_item


@router.patch("/{item_id}", 
              response_model=GalleryItemResponse,
              dependencies=[Depends(get_current_admin)],)
def update_gallery_item(
    item_id: int,
    gallery_update: GalleryItemUpdate,
    db: Session = Depends(get_db),
):
    service = GalleryService(db)

    try:
        gallery_item = service.update_gallery_item(
            item_id, gallery_update
        )
    except DuplicateGalleryImageError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc

    if gallery_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gallery item not found",
        )

    return gallery_item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(get_current_admin)],)
def delete_gallery_item(
    item_id: int,
    db: Session = Depends(get_db),
):
    service = GalleryService(db)

    if not service.delete_gallery_item(item_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gallery item not found",
        )