import pytest
import requests
from pydantic import BaseModel


class AccessTokenRequest(BaseModel):
    access_token: str


class User(BaseModel):
    id: int
    first_name: str
    last_name: str


def access_token_required():
    request = {
        "access_token": "test_token"
    }
    AccessTokenRequest(**request)


def users_get_response():
    response = [
        {"id": 121314, "first_name": "Tata", "last_name": "Mouse"},
        {"id": 151617, "first_name": "Milla", "last_name": "Young"}
    ]
    users = [User(**user) for user in response]


def access_token_required():
    request = {}
    with pytest.raises(ValueError):
        AccessTokenRequest(**request)


def access_token_format():
    request = {
        "access_token": "invalid_token_format"
    }
    with pytest.raises(ValueError):
        AccessTokenRequest(**request)


def users_get_success():
    response = [
        {"id": 121314, "first_name": "Tata", "last_name": "Mouse"},
        {"id": 151617, "first_name": "Milla", "last_name": "Young"}
    ]
    users = [User(**user) for user in response]
    assert len(users) == 2
    assert users[0].id == 121314
    assert users[0].first_name == "Tata"
    assert users[0].last_name == "Mouse"


def users_get_no_users():
    response = []
    users = [User(**user) for user in response]
    assert len(users) == 0


def user_format():
    user = {
        "id": "invalid_id_format",
        "first_name": "Tata",
        "last_name": "Mouse"
    }
    with pytest.raises(ValueError):
        User(**user)


def user_name_format():
    user = {
        "id": 121314,
        "first_name": "Anna",
        "last_name": "Mouse"
    }
    with pytest.raises(ValueError):
        User(**user)


def user_lastname_format():
    user = {
        "id": 121314,
        "first_name": "Tata",
        "last_name": "Rise"
    }
    with pytest.raises(ValueError):
        User(**user)


def users_get_one_user():
    response = [{"id": 121314, "first_name": "Tata", "last_name": "Mouse"}]
    users = [User(**user) for user in response]
    assert len(users) == 1
    assert users[0].id == 121314
    assert users[0].first_name == "Tata"
    assert users[0].last_name == "Mouse"


def users_get_max_users():
    response = [{"id": i, "first_name": "User", "last_name": str(i)} for i in range(1000)
]
    users = [User(**user) for user in response]
    assert len(users) == 1000
    assert users[-1].id == 999
    assert users[-1].first_name == "User"
    assert users[-1].last_name == "999"


def users_get_invalid_response():
    response = [{"invalid_attr": "value"}]
    with pytest.raises(ValueError):
        users = [User(**user) for user in response]
