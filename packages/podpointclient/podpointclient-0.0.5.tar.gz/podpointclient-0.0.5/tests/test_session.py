from datetime import datetime, timedelta
from timeit import repeat
from podpointclient.helpers.session import Session
import aiohttp
import asyncio
from aioresponses import aioresponses

from podpointclient.endpoints import API_BASE, API_BASE_URL, API_VERSION, AUTH, SESSIONS

import pytest

EMAIL: str = 'test@example.com'
PASSWORD: str = 'passw0rd!'

@pytest.mark.asyncio
async def test_create_happy_path(aiohttp_client):
    session_response = {
        "sessions": {
            "id": "5678",
            "user_id": "1234"
        }
    }

    with aioresponses() as m:
        m.post(f'{API_BASE_URL}{SESSIONS}', payload=session_response)

        async with aiohttp.ClientSession() as session:
            session = Session(email='test@example.com', password='foo',access_token='1234', session=session)
            assert session.user_id is None
            assert session.session_id is None
           
            assert await session.create() is True
            assert session.user_id == '1234'
            assert session.session_id == '5678'