import pytest
from bson import ObjectId
from fastapi import HTTPException
from starlette import status

from users_crm.schemas.users import UserSchemaUpdate
from users_crm.services.users import UsersService


@pytest.mark.asyncio
async def test_get_user_by_id_success(mock_user_repository_factory):
    mock_repo = mock_user_repository_factory.return_value
    mock_repo.find_one.return_value = {
        '_id': ObjectId('507f191e810c19729de860ea'),
        'email': 'testuser@example.com',
        'first_name': 'Test',
        'last_name': 'User',
        'role': 'simple mortal',
        'is_active': True,
    }

    service = UsersService(mock_user_repository_factory)
    user = await service.get_user_by_id('507f191e810c19729de860ea')

    assert user.email == 'testuser@example.com'
    assert user.first_name == 'Test'
    mock_repo.find_one.assert_called_once_with({'_id': ObjectId('507f191e810c19729de860ea')})


@pytest.mark.asyncio
async def test_get_user_by_id_not_found(mock_user_repository_factory):
    mock_repo = mock_user_repository_factory.return_value
    mock_repo.find_one.return_value = None

    service = UsersService(mock_user_repository_factory)

    with pytest.raises(HTTPException) as exc_info:
        await service.get_user_by_id('507f191e810c19729de860ea')

    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    assert exc_info.value.detail == 'User not found'
    mock_repo.find_one.assert_called_once_with({'_id': ObjectId('507f191e810c19729de860ea')})


@pytest.mark.asyncio
async def test_update_user_by_id_success(mock_user_repository_factory):
    mock_repo = mock_user_repository_factory.return_value
    update_data = UserSchemaUpdate(
        **{
            'first_name': 'Updated',
            'last_name': 'User',
            'role': 'simple mortal',
            'is_active': True
        }
    )
    mock_repo.update_one.return_value = {
        '_id': ObjectId('507f191e810c19729de860ea'),
        'email': 'testuser@example.com',
        'first_name': 'Updated',
        'last_name': 'User',
        'role': 'simple mortal',
        'is_active': True,
    }

    service = UsersService(mock_user_repository_factory)
    user = await service.update_user_by_id('507f191e810c19729de860ea', update_data)

    assert user.first_name == 'Updated'
    assert user.last_name == 'User'
    mock_repo.update_one.assert_called_once_with(
        id=ObjectId('507f191e810c19729de860ea'),
        data={
            'first_name': 'Updated',
            'last_name': 'User',
            'role': 'simple mortal',
            'is_active': True
        }
    )


@pytest.mark.asyncio
async def test_update_user_by_id_not_found(mock_user_repository_factory):
    mock_repo = mock_user_repository_factory.return_value
    update_data = UserSchemaUpdate(
        **{
            'first_name': 'Updated',
            'last_name': 'User',
            'email': 'testuser@example.com'
        }
    )
    mock_repo.update_one.return_value = None

    service = UsersService(mock_user_repository_factory)

    with pytest.raises(HTTPException) as exc_info:
        await service.update_user_by_id('507f191e810c19729de860ea', update_data)

    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    assert exc_info.value.detail == 'User not found'


@pytest.mark.asyncio
async def test_delete_user_by_id_success(mock_user_repository_factory):
    mock_repo = mock_user_repository_factory.return_value
    mock_repo.delete.return_value = 1

    service = UsersService(mock_user_repository_factory)
    deleted_count = await service.delete_user_by_id('507f191e810c19729de860ea')

    assert deleted_count == 1
    mock_repo.delete.assert_called_once_with({'_id': ObjectId('507f191e810c19729de860ea')})


@pytest.mark.asyncio
async def test_delete_user_by_id_not_found(mock_user_repository_factory):
    mock_repo = mock_user_repository_factory.return_value
    mock_repo.delete.return_value = 0

    service = UsersService(mock_user_repository_factory)
    deleted_count = await service.delete_user_by_id('507f191e810c19729de860ea')

    assert deleted_count == 0
    mock_repo.delete.assert_called_once_with({'_id': ObjectId('507f191e810c19729de860ea')})
