from typing import Annotated

from fastapi import APIRouter, Depends

from users_crm.api.dependencies import require_admin_role, users_service, validate_object_id
from users_crm.schemas.users import UserSchema, UserSchemaUpdate
from users_crm.services.users import UsersService

router = APIRouter(
    prefix='/users',
    tags=['Users'],
)


@router.patch('/{user_id}', response_model=UserSchema)
async def update_user(
    user: Annotated[UserSchemaUpdate, Depends()],
    users_service: Annotated[UsersService, Depends(users_service)],
    _=Depends(require_admin_role),
    validated_user_id: str = Depends(validate_object_id)
):
    return await users_service.update_user_by_id(id=validated_user_id, user=user)


@router.get('/{user_id}', response_model=UserSchema)
async def get_user(
    users_service: Annotated[UsersService, Depends(users_service)],
    validated_user_id: str = Depends(validate_object_id)
):
    return await users_service.get_user_by_id(validated_user_id)


@router.delete('/{user_id}', response_model=int)
async def delete_user(
    users_service: Annotated[UsersService, Depends(users_service)],
    validated_user_id: str = Depends(validate_object_id)
):
    return await users_service.delete_user_by_id(validated_user_id)
