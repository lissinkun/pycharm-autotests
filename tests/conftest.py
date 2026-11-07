"""Общая подготовка для API-тестов."""

import pytest
import requests

from clients.users_client import UsersClient
from settings import BASE_URL, TIMEOUT


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture
def api_session():
    session = requests.Session()
    yield session
    session.close()


@pytest.fixture
def users_client(base_url, api_session):
    return UsersClient(base_url=base_url, session=api_session, timeout=TIMEOUT)
