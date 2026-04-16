from uuid import UUID

from fastapi.responses import JSONResponse
from slugify import slugify

from app.models import DBSubCategory
from app.repositories import SubCategoryRepository
from app.schemas.requests.sub_category import SubCategoryIn, SubCategoryUpdateIn
from core.controller import BaseController


class SubCategoryController(BaseController[DBSubCategory]):
    def __init__(
        self,
        repository: SubCategoryRepository,
    ) -> None:
        super().__init__(DBSubCategory, repository)
        self.repository: SubCategoryRepository = repository

    async def create(self, data: SubCategoryIn) -> DBSubCategory:

        db_obj = await self.repository.create(
            {
                "name": data.name,
                "category_uid": data.category_uid,
                "slug": slugify(data.name),
            }
        )
        await self.commit()
        return db_obj

    async def update(self, uid: UUID, data: SubCategoryUpdateIn) -> DBSubCategory:
        sub_category = await self.get_by_uid(uid)
        db_obj = await self.repository.update(
            sub_category, data.model_dump(exclude_none=True)
        )
        await self.commit()
        return db_obj

    async def delete(self, uid: UUID) -> JSONResponse:
        sub_category = await self.get_by_uid(uid)

        await self.repository.delete(sub_category)
        await self.commit()

        return JSONResponse(
            content={"message": f"SubCategory with uid '{uid}' deleted successfully."}
        )
