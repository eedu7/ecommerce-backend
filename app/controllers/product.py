from typing import Sequence
from uuid import UUID

from fastapi.responses import JSONResponse
from slugify import slugify

from app.models import DBProduct
from app.repositories import ProductRepository
from app.schemas.requests.product import ProductIn, ProductUpdateIn
from core.controller import BaseController


class ProductController(BaseController[DBProduct]):
    def __init__(self, repository: ProductRepository) -> None:
        super().__init__(DBProduct, repository)
        self.repository: ProductRepository = repository

    async def get_all(self, offset: int = 0, limit: int = 20) -> Sequence[DBProduct]:
        return await self.repository.get_all(offset=offset, limit=limit)

    async def create(self, data: ProductIn) -> DBProduct:
        product = await self.repository.create(
            {**data.model_dump(exclude_none=True), "slug": slugify(data.name)}
        )
        await self.commit()
        return await self.get_by_uid(product.uid)

    async def update(self, uid: UUID, data: ProductUpdateIn) -> DBProduct:
        product = await self.get_by_uid(uid)

        updated = await self.repository.update(
            product, data.model_dump(exclude_none=True)
        )
        await self.commit()
        return updated

    async def delete(self, uid: UUID) -> JSONResponse:
        product = await self.get_by_uid(uid)
        await self.repository.delete(product)
        await self.commit()
        return JSONResponse(
            content={"message": f"Product with uid '{uid}' deleted successfully."}
        )
