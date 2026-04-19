from uuid import UUID

from fastapi.responses import JSONResponse
from slugify.slugify import slugify

from app.models import DBCategory
from app.repositories import CategoryRepository
from app.schemas.requests.category import CategoryIn, CategoryUpdateIn
from core.controller import BaseController


class CategoryController(BaseController[DBCategory]):
    def __init__(
        self,
        repository: CategoryRepository,
    ) -> None:
        super().__init__(DBCategory, repository)
        self.repository: CategoryRepository = repository

    async def create(self, data: CategoryIn) -> DBCategory:
        db_obj = await self.repository.create(
            {**data.model_dump(), "slug": slugify(data.name)}
        )
        await self.commit()
        return db_obj

    async def update(
        self,
        uid: UUID,
        data: CategoryUpdateIn,
    ) -> DBCategory:
        category = await self.get_by_uid(uid)

        updated = await self.repository.update(
            category, data.model_dump(exclude_none=True)
        )

        await self.commit()

        return updated

    async def delete(self, uid: UUID) -> JSONResponse:
        category = await self.get_by_uid(uid)

        await self.repository.delete(category)
        await self.commit()

        return JSONResponse(
            content={"message": f"Category with uid '{uid}' deleted successfully."}
        )
