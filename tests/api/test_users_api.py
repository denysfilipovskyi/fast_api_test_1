import pytest


@pytest.mark.asyncio
async def test_add_user_already_exist(test_client):
    response = test_client.post(
        '/auth/register', params={
            'email': 'create@example.com',
            'password': 'password',
            'role': 'simple mortal',
            'first_name': 'first name',
        }
    )
    assert response.status_code == 400

    data = response.json()
    assert data['detail'] == 'Email already registered'


def test_update_user_unauthorized(test_client, valid_object_id):

    response = test_client.patch(
        f'/users/{valid_object_id}',
        json={
            'email': 'testuser@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        }
    )

    assert response.status_code == 401


def test_get_user_success(test_client):
    valid_object_id = '507f191e810c19729de860ea'
    response = test_client.get(f'/users/{valid_object_id}')

    expected_response = {
        '_id': valid_object_id,
        'email': 'testuser@example.com',
        'first_name': 'Test',
        'last_name': 'User',
        'role': 'simple mortal',
        'is_active': True,
    }

    assert response.status_code == 200

    response_json = response.json()
    assert response_json['_id'] == expected_response['_id']
    assert response_json['email'] == expected_response['email']
    assert response_json['first_name'] == expected_response['first_name']
    assert response_json['last_name'] == expected_response['last_name']
    assert response_json['role'] == expected_response['role']
    assert response_json['is_active'] == expected_response['is_active']
