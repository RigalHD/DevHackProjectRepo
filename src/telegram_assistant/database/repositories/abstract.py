from abc import abstractmethod
from collections.abc import Sequence
from typing import Any, Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from telegram_assistant.database.models.base import BaseModel

AbstractModel = TypeVar("AbstractModel")


class Repository(Generic[AbstractModel]):
    def __init__(self, type_model: type[BaseModel], session: AsyncSession) -> None:
        self.type_model: type[BaseModel] = type_model
        self.session: AsyncSession = session

    async def exists(self, id_: int | str) -> bool:
        return bool(await self.session.get(self.type_model, id_))

    async def get(self, id_: int | str) -> BaseModel | None:
        return await self.session.get(self.type_model, id_)

    async def get_many(self, whereclause: dict) -> Sequence[BaseModel]:
        """:param whereclause: {AbstractModel.column: value}
        """
        stmt = select(self.type_model)
        for key, value in whereclause.items():
            stmt = stmt.where(key == value)
        result = await self.session.scalars(stmt)
        return result.all()

    async def get_all(self) -> Sequence[BaseModel]:
        stmt = select(self.type_model)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    @abstractmethod
    async def create(self, *args: tuple[Any], **kwargs: dict[str, Any]) -> None:
        ...
