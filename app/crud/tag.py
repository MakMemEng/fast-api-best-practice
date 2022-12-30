from fastapi.encoders import jsonable_encoder
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.orm import Session

from app import models, schemas

from .base import CRUDBase


class CRUDTag(CRUDBase[models.Tag, schemas.TagCreate, schemas.TagUpdate, schemas.TagsPagedResponse]):
    def upsert_tags(self, db: Session, tags_in: list[schemas.TagCreate]) -> list[models.Tag]:
        tags_in_list = jsonable_encoder(tags_in)
        insert_stmt = insert(models.Tag).values(tags_in_list)
        insert_stmt = insert_stmt.on_duplicate_key_update(name=insert_stmt.inserted.name)
        db.execute(insert_stmt)

        tag_names = map(lambda x: x.name, tags_in)
        tags = db.query(models.Tag).filter(models.Tag.name.in_(tag_names)).all()

        return tags


tag = CRUDTag(models.Tag, schemas.TagsPagedResponse)