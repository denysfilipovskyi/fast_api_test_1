from unittest.mock import AsyncMock, MagicMock

import pytest
from bson import ObjectId
from fastapi.testclient import TestClient

from users_crm.api.dependencies import auth_service, users_service
from users_crm.main import app
from users_crm.services.auth import AuthService
from users_crm.services.users import UsersService


@pytest.fixture
def mock_user_repository_factory():
    mock_repo = AsyncMock()
    mock_repo.find_one.return_value = {
        'id': '507f191e810c19729de860ea',
        'email': 'testuser@example.com',
        'first_name': 'Test',
        'last_name': 'User',
        'role': 'simple mortal',
        'is_active': True,
    }
    mock_repo.add_one.return_value = '507f191e810c19729de860ea'
    return MagicMock(return_value=mock_repo)


@pytest.fixture
def mock_rmq_repository_factory():
    mock_repo = AsyncMock()
    mock_repo.publish.return_value = True
    return MagicMock(return_value=mock_repo)


@pytest.fixture
def valid_object_id():
    return str(ObjectId())


@pytest.fixture
def test_client(mock_user_repository_factory, mock_rmq_repository_factory):
    app.dependency_overrides[users_service] = lambda: UsersService(
        users_repo=mock_user_repository_factory
    )
    app.dependency_overrides[auth_service] = lambda: AuthService(
        users_repo=mock_user_repository_factory,
        msg_broker_repo=mock_rmq_repository_factory
    )

    with TestClient(app) as client:
        yield client

    del app.dependency_overrides[users_service]
    del app.dependency_overrides[auth_service]
