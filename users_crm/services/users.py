from bson import ObjectId
from fastapi import HTTPException, status

from users_crm.repositories.abstract.nosql import AbstractNoSqlRepository
from users_crm.schemas.users import UserSchema, UserSchemaUpdate


class UsersService:
    def __init__(self, users_repo: AbstractNoSqlRepository):
        self.users_repo: AbstractNoSqlRepository = users_repo()

    async def update_user_by_id(self, id: str, user: UserSchemaUpdate) -> UserSchema:
        user_dict = user.model_dump(by_alias=True)
        data = await self.users_repo.update_one(
            id=ObjectId(id),
            data=user_dict
        )
        if not data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
        return UserSchema(**data)

    async def get_user_by_id(self, id: str) -> UserSchema:
        data = await self.users_repo.find_one({'_id': ObjectId(id)})
        if not data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
        return UserSchema(**data)

    async def delete_user_by_id(self, id: str) -> int:
        return await self.users_repo.delete({'_id': ObjectId(id)})
